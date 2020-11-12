from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsProcessing,
    QgsProcessingFeatureSource,
    QgsProcessingParameterDistance,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QVariant

from PreCourlis.processing.precourlis_algorithm import PreCourlisFeatureBasedAlgorithm


class PointsAlongLinesAlgorithm(PreCourlisFeatureBasedAlgorithm):
    """
    Adapted version of QgsPointsAlongGeometryAlgorithm,
    which add a feature for last point of input geometry.
    """

    DISTANCE = "DISTANCE"

    def initParameters(self, config):
        self.addParameter(
            QgsProcessingParameterDistance(
                self.DISTANCE,
                self.tr("Distance"),
                defaultValue=1.0,
                parentParameterName="INPUT",
                optional=False,
                minValue=0,
            )
        )

    def outputName(self):
        return self.tr("Interpolated points")

    def inputLayerTypes(self):
        return [QgsProcessing.TypeVectorLine, QgsProcessing.TypeVectorPolygon]

    def outputLayerType(self):
        return QgsProcessing.TypeVectorPoint

    def outputWkbType(self, inputType):
        out = QgsWkbTypes.Point
        if QgsWkbTypes.hasZ(inputType):
            out = QgsWkbTypes.addZ(out)
        if QgsWkbTypes.hasM(inputType):
            out = QgsWkbTypes.addM(out)
        return out

    def outputFields(self, inputFields):
        output = inputFields
        output.append(QgsField("distance", QVariant.Double))
        return output

    def sourceFlags(self):
        # skip geometry checks - this algorithm doesn't care about invalid geometries
        return QgsProcessingFeatureSource.FlagSkipGeometryValidityChecks

    def sinkFlags(self):
        return QgsFeatureSink.RegeneratePrimaryKey

    def prepareAlgorithm(self, parameters, context, feedback):
        self.distance = self.parameterAsDouble(parameters, self.DISTANCE, context)
        return True

    def _create_point(self, source_feature, distance):
        f = QgsFeature()
        f.setGeometry(source_feature.geometry().interpolate(distance))
        attr = source_feature.attributes()
        attr.append(distance)
        f.setAttributes(attr)
        return f

    def processFeature(self, feature, context, feedback):
        totalLength = feature.geometry().length()

        currentDistance = 0
        out = []
        while currentDistance < totalLength:
            out.append(self._create_point(feature, currentDistance))
            currentDistance += self.distance

            # better check here -- a ridiculously small distance might take forever
            if feedback.isCanceled():
                break

        out.append(self._create_point(feature, totalLength))
        return out

    def name(self):
        return "pointsalonglines"

    def displayName(self):
        return self.tr("Points along lines")

    def group(self):
        return self.tr("Interpolate")

    def groupId(self):
        return "Interpolate"

    def createInstance(self):
        return PointsAlongLinesAlgorithm()
