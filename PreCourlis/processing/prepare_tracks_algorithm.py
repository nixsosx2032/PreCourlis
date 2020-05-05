import math

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QCoreApplication, QVariant

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.core.utils import qgslinestring_angle


class PrepareTracksAlgorithm(QgsProcessingAlgorithm):
    """
    This algorithm construct a PreCourlis structured line layer from any line layer:
        - Construct line layer with "PreCourlis" fields.
        - Reverse geometry if needed (depending on axis direction)
        - Populate attributes:
            - sec_id
            - sec_name
            - sec_pos
    """

    TRACKS = "TRACKS"
    AXIS = "AXIS"
    FIRST_POS = "FIRST_POS"
    NAME_FIELD = "NAME_FIELD"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.TRACKS, self.tr("Tracks"), [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.AXIS, self.tr("Axis"), [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.FIRST_POS,
                self.tr("Abscissa of first section"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.NAME_FIELD,
                self.tr("Name field"),
                parentLayerParameterName=self.TRACKS,
                optional=True,
                type=QgsProcessingParameterField.String,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Prepared tracks")),
            True,
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.TRACKS, context)
        axis = self.parameterAsSource(parameters, self.AXIS, context)
        self.first_pos = self.parameterAsDouble(parameters, self.FIRST_POS, context)
        self.name_field = self.parameterAsString(parameters, self.NAME_FIELD, context)
        self.axis = next(axis.getFeatures())
        self.name_field_index = source.fields().indexFromName(self.name_field)

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

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            intersection = feature.geometry().intersection(self.axis.geometry())
            assert not intersection.isNull()

            sec_pos = self.axis.geometry().lineLocatePoint(intersection)

            # Take only the first parts (QgsMultiLineString => QgsLineString)
            axis_line = next(self.axis.geometry().constParts())
            track_line = next(feature.geometry().constParts())

            intersection_point = intersection.constGet()
            track_angle = qgslinestring_angle(track_line, intersection_point) * (
                180 / math.pi
            )
            axis_angle = qgslinestring_angle(axis_line, intersection_point) * (
                180 / math.pi
            )
            d_angle = (track_angle - axis_angle) % 360

            out = QgsFeature()
            out.setAttributes(
                [
                    None,
                    feature.attribute(self.name_field_index)
                    if self.name_field
                    else "P_{:04.3f}".format(self.first_pos + sec_pos),
                    self.first_pos + sec_pos,
                    # intersection_point.x(),
                    # intersection_point.y(),
                    QVariant(),
                    QVariant(),
                    QVariant(),
                ]
            )
            if d_angle < 180:
                out.setGeometry(QgsGeometry(track_line.reversed()))
            else:
                out.setGeometry(QgsGeometry(feature.geometry()))

            # Add a feature in the sink
            sink.addFeature(out, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def name(self):
        return "prepare_tracks"

    def displayName(self):
        return self.tr("Prepare tracks")

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return "Import"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return PrepareTracksAlgorithm()
