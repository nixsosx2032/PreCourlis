import os
import subprocess
from pkg_resources import resource_filename

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorDestination,
    QgsProcessingUtils,
)
from qgis.PyQt.QtCore import QCoreApplication, QVariant

import processing

from PreCourlis.core.precourlis_file import PreCourlisFileLine

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
            "PreCourlis",
            "lib/TatooineMesher/.venv/lib/python3.6/site-packages",
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
    CONSTRAINT_LINES = "CONSTRAINT_LINES"
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
            QgsProcessingParameterMultipleLayers(
                self.CONSTRAINT_LINES,
                self.tr("Contraint lines"),
                layerType=QgsProcessing.TypeVectorLine,
                defaultValue=None,
                optional=True,
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
                self.LAT_STEP,
                self.tr("Lateral space step (in m)"),
                defaultValue=None,
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

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        outputs = {}

        sections = self.parameterAsSource(parameters, self.SECTIONS, context)

        # Prefix layer fields by "Z" for TatooineMesher
        file = PreCourlisFileLine(sections)
        alg_params = {
            "INPUT": parameters[self.SECTIONS],
            "FIELDS_MAPPING": [
                {"name": "sec_id", "type": QVariant.Int, "expression": '"sec_id"'}
            ]
            + [
                {
                    "name": "Z{}".format(layer),
                    "type": QVariant.Double,
                    "expression": '"{}"'.format(layer),
                }
                for layer in file.layers()
            ],
            "OUTPUT": QgsProcessingUtils.generateTempFilename("tatooine_input.shp"),
        }
        outputs["RefactorFields"] = processing.run(
            "qgis:refactorfields",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        tatooine_input = outputs["RefactorFields"]["OUTPUT"]

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        axis_path = self.parameterAsCompatibleSourceLayerPath(
            parameters,
            self.AXIS,
            context,
            compatibleFormats=["shp"],
        )
        constraint_lines = self.parameterAsLayerList(
            parameters,
            self.CONSTRAINT_LINES,
            context,
        )
        long_step = self.parameterAsString(parameters, self.LONG_STEP, context)
        lat_step = self.parameterAsString(parameters, self.LAT_STEP, context)
        attr_cross_sections = self.parameterAsString(
            parameters, self.ATTR_CROSS_SECTION, context
        )
        output_path = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        # Merge constraint lines files
        if constraint_lines:
            outputs["MergeContraints"] = processing.run(
                "native:mergevectorlayers",
                {
                    "LAYERS": parameters[self.CONSTRAINT_LINES],
                    "CRS": sections.sourceCrs(),
                    "OUTPUT": QgsProcessingUtils.generateTempFilename(
                        "constraint_lines.shp"
                    ),
                },
            )
            constraint_lines = outputs["MergeContraints"]["OUTPUT"]

        command = [
            PYTHON_INTERPRETER,
            PYTHON_SCRIPT,
            "-v",
        ]
        if constraint_lines:
            command += [
                "--infile_constraint_lines",
                constraint_lines,
            ]
        command += [
            "--long_step",
            long_step,
            "--lat_step",
            lat_step,
            "--attr_cross_sections",
            attr_cross_sections,
            axis_path,
            tatooine_input,
            output_path,
        ]

        feedback.pushCommandInfo(" ".join(command))

        env = {key: value for key, value in os.environ.items()}
        env["PYTHONPATH"] = os.pathsep.join([env.get("PYTHONPATH", ""), PYTHONPATH])

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
            {"INPUT": output_path, "CRS": sections.sourceCrs()},
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
