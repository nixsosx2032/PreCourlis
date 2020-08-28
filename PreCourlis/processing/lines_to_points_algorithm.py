from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QCoreApplication, QVariant

from PreCourlis.core.precourlis_file import PreCourlisFilePoint


class LinesToPointsAlgorithm(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output layer")),
            True,
        )

    def to_float(self, value):
        if value == "NULL":
            return QVariant()
        return value

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            PreCourlisFilePoint.base_fields(),
            QgsWkbTypes.PointZ,
            source.sourceCrs(),
        )
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        for current, line_feature in enumerate(features):

            # Take only the first parts (QgsMultiLineString => QgsLineString)
            line = next(line_feature.geometry().constParts())
            for point, p_id, abs_lat, zfond in zip(
                line.points(),
                line_feature.attribute("p_id").split(","),
                line_feature.attribute("abs_lat").split(","),
                line_feature.attribute("zfond").split(","),
            ):
                point_feature = QgsFeature()
                point_feature.setAttributes(
                    [
                        line_feature.attribute("sec_id"),
                        line_feature.attribute("sec_name"),
                        line_feature.attribute("abs_long"),
                        line_feature.attribute("axis_x"),
                        line_feature.attribute("axis_y"),
                        "",
                        int(p_id),
                        self.to_float(abs_lat),
                        self.to_float(point.x()),
                        self.to_float(point.y()),
                        self.to_float(zfond),
                    ]
                )
                if zfond != "NULL":
                    point.addZValue(float(zfond))
                point_feature.setGeometry(QgsGeometry(point))
                sink.addFeature(point_feature, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def name(self):
        return "lines_to_points"

    def displayName(self):
        return self.tr("Lines to points")

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return "Convert"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return LinesToPointsAlgorithm()
