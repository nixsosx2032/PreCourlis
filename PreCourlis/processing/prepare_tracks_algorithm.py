import math

from qgis.core import (
    QgsProcessing,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QVariant

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.core.utils import qgslinestring_angle
from PreCourlis.processing.precourlis_algorithm import PreCourlisAlgorithm


class PrepareTracksAlgorithm(PreCourlisAlgorithm):
    """
    This algorithm construct a PreCourlis structured line layer from any line layer:
        - Construct line layer with "PreCourlis" fields.
        - Reverse geometry if needed (depending on axis direction)
        - Populate attributes:
            - sec_id
            - sec_name
            - abs_long
    """

    TRACKS = "TRACKS"
    AXIS = "AXIS"
    NAME_FIELD = "NAME_FIELD"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.TRACKS,
                self.tr("Tracks"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.AXIS,
                self.tr("Axis"),
                [QgsProcessing.TypeVectorLine],
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
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Prepared")),
            True,
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.TRACKS, context)
        axis = self.parameterAsSource(parameters, self.AXIS, context)
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

            abs_long = self.axis.geometry().lineLocatePoint(intersection)

            # Take only the first parts (QgsMultiLineString => QgsLineString)
            axis_line = next(self.axis.geometry().constParts()).clone()
            track_line = next(feature.geometry().constParts()).clone()

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
                    # sec_id
                    None,
                    # sec_name
                    feature.attribute(self.name_field_index)
                    if self.name_field
                    else None,
                    # abs_long
                    abs_long,
                    # axis_x
                    intersection_point.x(),
                    # axis_y
                    intersection_point.y(),
                    # layers
                    "",
                    # p_id
                    QVariant(),
                    # topo_bat
                    "B",
                    # abs_lat
                    QVariant(),
                    # zfond
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
        return self.tr("Import")

    def groupId(self):
        return "Import"

    def createInstance(self):
        return PrepareTracksAlgorithm()
