import os

from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
    QgsProcessingParameterVectorLayer,
)

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.lib.mascaret.mascaretgeo_file import MascaretGeoFile
from PreCourlis.processing.precourlis_algorithm import PreCourlisAlgorithm


class ExportMascaretAlgorithm(PreCourlisAlgorithm):
    """
    This algorithm export a PreCourlis structured line layer to a .georef or .geo file.
    """

    INPUT = "INPUT"
    REACH_NAME = "REACH_NAME"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input"),
                types=[QgsProcessing.TypeVectorLine],
                defaultValue=None,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.REACH_NAME,
                self.tr("Reach name (default to input layer name)"),
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr("Output file"),
                fileFilter="Georef file (*.georef);;Geo file (*.geo)",
            )
        )

    def checkParameterValues(self, parameters, context):
        ok, msg = super().checkParameterValues(parameters, context)
        if ok:
            input_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
            reach_name = (
                self.parameterAsString(parameters, self.REACH_NAME, context)
                or input_layer.name()
            )
            if " " in reach_name:
                return False, self.tr("Reach name cannot contain spaces")
        return ok, msg

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        reach_name = (
            self.parameterAsString(parameters, self.REACH_NAME, context)
            or input_layer.name()
        )
        output_path = self.parameterAsString(parameters, self.OUTPUT, context)

        precourlis_file = PreCourlisFileLine(input_layer)
        reach = precourlis_file.get_reach(reach_name)

        output_file = MascaretGeoFile(output_path, mode="write")
        output_file.has_ref = "ref" in os.path.splitext(output_path)[1][1:]
        output_file.add_reach(reach)
        output_file.save(output_path)

        return {self.OUTPUT: output_path}

    def name(self):
        return "export_mascaret"

    def displayName(self):
        return self.tr("Export Mascaret")

    def group(self):
        return self.tr("Export")

    def groupId(self):
        return "Export"

    def createInstance(self):
        return ExportMascaretAlgorithm()
