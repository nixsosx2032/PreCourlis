from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsLineString,
    QgsPoint,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QCoreApplication

from PreCourlis.core.precourlis_file import PreCourlisFileLine


class PointsToLinesAlgorithm(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr("Input"), [QgsProcessing.TypeVectorPoint],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output layer")),
            True,
        )

    def line_feature_from_points(self, point_features):
        points = []
        for point_feature in point_features:
            point = point_feature.geometry().constGet()
            points.append(QgsPoint(x=point.x(), y=point.y(), z=point.z(),))
        line = QgsGeometry(QgsLineString(points))

        line_feature = QgsFeature()
        line_feature.setAttributes(
            [
                point_features[0].attribute("sec_id"),
                point_features[0].attribute("sec_name"),
                point_features[0].attribute("sec_id"),
                ",".join([str(id_ + 1) for id_ in range(0, len(points))]),
                ",".join(
                    [str(line.lineLocatePoint(f.geometry())) for f in point_features]
                ),
                ",".join([str(f.attribute("p_z")) for f in point_features]),
            ]
        )
        line_feature.setGeometry(line)
        return line_feature

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            PreCourlisFileLine.base_fields(),
            QgsWkbTypes.LineString,
            source.sourceCrs(),
        )
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        sec_id = None
        point_features = []
        for current, point_feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            if sec_id is not None and point_feature.attribute("sec_id") != sec_id:
                sink.addFeature(
                    self.line_feature_from_points(point_features),
                    QgsFeatureSink.FastInsert,
                )
                sec_id = None
                point_features = []

            sec_id = point_feature.attribute("sec_id")
            point_features.append(point_feature)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        if sec_id is not None:
            sink.addFeature(
                self.line_feature_from_points(point_features), QgsFeatureSink.FastInsert
            )
            sec_id = None

        return {self.OUTPUT: dest_id}

    def name(self):
        return "points_to_lines"

    def displayName(self):
        return self.tr("Points to lines")

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return "Convert"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return PointsToLinesAlgorithm()
