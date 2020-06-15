from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsLineString,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsFeatureRequest,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QCoreApplication

from PreCourlis.core.precourlis_file import PreCourlisFileLine


class PointsToLinesAlgorithm(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    AXIS = "AXIS"
    GROUP_FIELD = "GROUP_FIELD"
    ORDER_FIELD = "ORDER_FIELD"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr("Input"), [QgsProcessing.TypeVectorPoint],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.AXIS,
                self.tr(
                    "Axis (needed to calculate axis_x and axis_y if not already set in source)"
                ),
                types=[QgsProcessing.TypeVectorLine],
                defaultValue=None,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.GROUP_FIELD,
                self.tr("Group by field"),
                optional=True,
                parentLayerParameterName=self.INPUT,
                allowMultiple=False,
                defaultValue="sec_id",
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ORDER_FIELD,
                self.tr("Order by field"),
                optional=True,
                parentLayerParameterName=self.INPUT,
                allowMultiple=False,
                defaultValue="p_id",
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output layer")),
            True,
        )

    def line_feature_from_points(self, point_features, sec_id):
        points = [
            point_feature.geometry().constGet().clone()
            for point_feature in point_features
        ]
        line = QgsGeometry(QgsLineString(points))

        # Take only the first parts (QgsMultiLineString => QgsLineString)
        intersection_point = None
        if self.axis:
            intersection = line.intersection(self.axis.geometry())
            intersection_point = intersection.constGet()

        line_feature = QgsFeature()
        line_feature.setAttributes(
            [
                point_features[0].attribute("sec_id") or sec_id,
                (
                    point_features[0].attribute("sec_name")
                    or "P_{:04.3f}".format(point_features[0].attribute("sec_pos"))
                ),
                point_features[0].attribute("sec_pos"),
                intersection_point.x()
                if self.axis
                else point_features[0].attribute("axis_x"),
                intersection_point.y()
                if self.axis
                else point_features[0].attribute("axis_y"),
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
        axis = self.parameterAsSource(parameters, self.AXIS, context)
        group_field = self.parameterAsString(parameters, self.GROUP_FIELD, context)
        order_field = self.parameterAsString(parameters, self.ORDER_FIELD, context)

        self.axis = next(axis.getFeatures()) if axis else None

        request = QgsFeatureRequest()
        request.addOrderBy('"{}"'.format(group_field), True, True)

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
        features = source.getFeatures(request)

        group = None
        point_features = []
        sec_id = 0
        for current, point_feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            if group is not None and point_feature.attribute(group_field) != group:
                sec_id += 1
                sink.addFeature(
                    self.line_feature_from_points(
                        sorted(point_features, key=lambda f: f.attribute(order_field)),
                        sec_id,
                    ),
                    QgsFeatureSink.FastInsert,
                )
                group = None
                point_features = []

            group = point_feature.attribute(group_field)
            point_features.append(point_feature)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        if group is not None:
            sec_id += 1
            sink.addFeature(
                self.line_feature_from_points(point_features, sec_id),
                QgsFeatureSink.FastInsert,
            )
            group = None

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
