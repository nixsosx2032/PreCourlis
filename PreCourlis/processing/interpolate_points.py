import os
import subprocess
from pkg_resources import resource_filename

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
)
from qgis.PyQt.QtCore import QCoreApplication

import processing

PYTHON_INTERPRETER = "python3"
ENCODING = "utf-8"

if os.name == "nt":
    PYTHON_INTERPRETER = "pythonw.exe"
    ENCODING = "cp1252"

PYTHON_SCRIPT = resource_filename(
    "PreCourlis", "lib/TatooineMesher/cli/densify_cross_sections.py"
)
PYTHONPATH = os.pathsep.join(
    [
        resource_filename("PreCourlis", "lib/TatooineMesher"),
        resource_filename(
            "PreCourlis", "lib/TatooineMesher/.venv/lib/python3.6/site-packages",
        ),
    ]
)


class ParameterShapefileDestination(QgsProcessingParameterVectorDestination):
    def supportedOutputVectorLayerExtensions(self):
        return ["shp"]

    def defaultFileExtension(self):
        return "shp"


class InterpolatePointsAlgorithm(QgsProcessingAlgorithm):

    SECTIONS = "SECTIONS"
    AXIS = "AXIS"
    LONG_STEP = "LONG_STEP"
    LAT_STEP = "LAT_STEP"
    ATTR_CROSS_SECTION = "ATTR_CROSS_SECTION"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.SECTIONS,
                self.tr("Sections"),
                types=[QgsProcessing.TypeVectorPoint],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.AXIS,
                self.tr("Axis"),
                types=[QgsProcessing.TypeVectorLine],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.LONG_STEP,
                self.tr("Longitudinal space step (in m)"),
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.LAT_STEP, self.tr("Lateral space step (in m)"), defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ATTR_CROSS_SECTION,
                self.tr("Attribute to identify cross-sections"),
                parentLayerParameterName=self.SECTIONS,
                defaultValue=None,
            )
        )
        self.addParameter(ParameterShapefileDestination(self.OUTPUT, self.tr("Output")))

    def processAlgorithm(self, parameters, context, feedback):
        section = self.parameterAsSource(parameters, self.SECTIONS, context)

        sections_path = self.parameterAsCompatibleSourceLayerPath(
            parameters, self.SECTIONS, context, compatibleFormats=["shp"],
        )
        axis_path = self.parameterAsCompatibleSourceLayerPath(
            parameters, self.AXIS, context, compatibleFormats=["shp"],
        )
        long_step = self.parameterAsString(parameters, self.LONG_STEP, context)
        lat_step = self.parameterAsString(parameters, self.LAT_STEP, context)
        attr_cross_sections = self.parameterAsString(
            parameters, self.ATTR_CROSS_SECTION, context
        )
        output_path = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        command = [
            PYTHON_INTERPRETER,
            PYTHON_SCRIPT,
            "-v",
            "--long_step",
            long_step,
            "--lat_step",
            lat_step,
            "--attr_cross_sections",
            attr_cross_sections,
            axis_path,
            sections_path,
            output_path,
        ]

        feedback.pushCommandInfo(" ".join(command))

        env = {key: value for key, value in os.environ.items()}
        env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], PYTHONPATH])

        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            env=env,
            encoding=ENCODING,
        ) as proc:
            while proc.poll() is None:
                for line in iter(proc.stdout.readline, ""):
                    feedback.pushConsoleInfo(line.strip())
            for line in iter(proc.stdout.readline, ""):
                feedback.pushConsoleInfo(line.strip())
            if proc.returncode != 0:
                raise QgsProcessingException(
                    "Failed to execute command {}".format(" ".join(command))
                )

        processing.run(
            "qgis:definecurrentprojection",
            {"INPUT": output_path, "CRS": section.sourceCrs()},
        )

        return {self.OUTPUT: output_path}

    def name(self):
        return "interpolate_points"

    def displayName(self):
        return self.tr("Interpolate points")

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return "Interpolate"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return InterpolatePointsAlgorithm()
