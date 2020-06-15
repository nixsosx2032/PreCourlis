from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterVectorLayer,
)
from qgis.PyQt.QtCore import QCoreApplication

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.lib.mascaret.mascaretgeo_file import MascaretGeoFile


class ExportGeorefAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm export a PreCourlis structured line layer to a .georef file.
    """

    INPUT = "INPUT"
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
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr("Output file"),
                fileFilter=(
                    "Geo file (*.geo)"
                    ";;GeoC file (*.geoC)"
                    ";; Georef file (*.georef)"
                    ";;GeorefC file (*.georefC)"
                ),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        output_path = self.parameterAsString(parameters, self.OUTPUT, context)

        precourlis_file = PreCourlisFileLine(input_layer)

        output_file = MascaretGeoFile(output_path, mode="read", load_file=False,)

        output_file.add_reach(precourlis_file.get_reach())

        output_file.save(output_path)

        return {self.OUTPUT: output_path}

    def name(self):
        return "export_georef"

    def displayName(self):
        return self.tr("Export Georef")

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return "Export"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ExportGeorefAlgorithm()
