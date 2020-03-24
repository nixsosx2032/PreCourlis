import os
import logging
import math
from builtins import int

from qgis.core import (
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
)
from qgis.PyQt.QtCore import QVariant

import processing

from PreCourlis.core import Reach, TEMP_FOLDER
from PreCourlis.core.utils import qgslinestring_angle

LOG = logging.getLogger(__name__)


def line_layer_from_tracks(
    name: str,
    tracks: QgsVectorLayer,
    axis: QgsVectorLayer,
    first_pos: float,
    name_field: str,
):
    """"
    Construct standard line layer from tracks:
        - Construct a standard reach line layer
        - Reverse geometry if needed (depending on axis direction)
        - Populate attributes:
            - sec_id
            - sec_name
            - sec_pos
    """

    axis = next(axis.getFeatures())

    reach = Reach(0, name=name, crs_id=tracks.crs().authid(),)
    layer = reach.to_line_layer()
    pr = layer.dataProvider()

    id_ = 0
    name_field_index = tracks.fields().indexFromName(name_field)
    for track in tracks.getFeatures():

        intersection = track.geometry().intersection(axis.geometry())
        assert not intersection.isNull()

        sec_pos = axis.geometry().lineLocatePoint(intersection)

        # Take only the first parts (QgsMultiLineString => QgsLineString)
        axis_line = next(axis.geometry().constParts())
        track_line = next(track.geometry().constParts())

        intersection_point = intersection.constGet()
        track_angle = qgslinestring_angle(track_line, intersection_point) * (
            180 / math.pi
        )
        axis_angle = qgslinestring_angle(axis_line, intersection_point) * (
            180 / math.pi
        )
        d_angle = (track_angle - axis_angle) % 360

        feature = QgsFeature()
        feature.setAttributes(
            [
                id_,
                track.attribute(name_field_index)
                if name_field
                else "P_{:.3}".format(sec_pos),
                first_pos + sec_pos,
                # intersection_point.x(),
                # intersection_point.y(),
                QVariant(),
                QVariant(),
                QVariant(),
            ]
        )
        if d_angle < 180:
            feature.setGeometry(QgsGeometry(track_line.reversed()))
        else:
            feature.setGeometry(QgsGeometry(track.geometry()))

        pr.addFeature(feature)
        id_ += 1

    layer.reload()

    return layer


def reach_from_tracks(
    name: str,
    tracks: QgsVectorLayer,
    dem: QgsRasterLayer,
    axis: QgsVectorLayer,
    step: int,
    first_pos: int,
    name_field: str,
):

    os.makedirs(TEMP_FOLDER, exist_ok=True)

    line_layer = line_layer_from_tracks(name, tracks, axis, first_pos, name_field)

    # v.to.points
    outputs = processing.run(
        "grass7:v.to.points",
        {
            "input": line_layer,
            "type": [0, 1, 2, 3, 5],
            "use": 1,
            "dmax": step,
            "-i": True,
            "-t": False,
            "output": os.path.join(TEMP_FOLDER, "to_points.shp"),
        },
    )
    to_points = QgsVectorLayer(outputs["output"], "to_points", "ogr")
    assert to_points.isValid()

    # v.what.rast
    outputs = processing.run(
        "grass7:v.what.rast",
        {
            "-i": False,
            "column": "z",
            "map": to_points,
            "raster": dem,
            "type": 0,
            "where": "",
            "output": os.path.join(TEMP_FOLDER, "set_attribute_z.shp"),
        },
    )
    set_attribute_z = QgsVectorLayer(outputs["output"], "set_attribute_z", "ogr")
    assert set_attribute_z.isValid()

    layer = set_attribute_z
    layer.setName(name)

    return Reach.from_point_layer(layer)
