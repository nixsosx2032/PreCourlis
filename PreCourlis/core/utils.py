import math

from qgis.core import QgsLineString, QgsPoint


def color_to_hex(color):
    def to_hex(v):
        return hex(v)[2:].zfill(2)

    return "#{}{}{}".format(
        to_hex(color.red()), to_hex(color.green()), to_hex(color.blue()),
    )


def vector_angle(p1, p2):
    """
    Calculate vector angle.
    """
    dx = p2.x() - p1.x()
    dy = p2.y() - p1.y()
    return math.atan2(dy, dx)


def qgslinestring_angle(linestring: QgsLineString, point: QgsPoint):
    """
    Calculate angle of a QgsLineString at specified QgsPoint.
    """

    distance, closest_point, vertex_id, left_of = linestring.closestSegment(point)
    """
    print(
        distance,
        closest_point,
        linestring.vertexNumberFromVertexId(vertex_id),
        left_of
    )
    """
    p1 = linestring.pointN(linestring.vertexNumberFromVertexId(vertex_id) - 1)
    p2 = linestring.pointN(linestring.vertexNumberFromVertexId(vertex_id))
    return vector_angle(p1, p2)
