from collections import OrderedDict
import numpy as np

from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsLineString,
    QgsPoint,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QVariant

from PreCourlis.lib.mascaret.mascaret_file import (
    Section as SectionBase,
    Reach as ReachBase,
)

TEMP_FOLDER = "/tmp/PreCourlis"


def to_float(v):
    if v is None:
        return None
    if isinstance(v, QVariant) and v.isNull():
        return None
    return float(v)


class Point:
    def __init__(self, x, y, z, d):
        self.x = to_float(x)
        self.y = to_float(y)
        self.z = to_float(z)
        self.d = to_float(d)

    def __eq__(self, other):
        return other.__dict__ == self.__dict__

    def __repr__(self):
        return "Point(d={d}, x={x}, y={y}, z={z})".format(**self.__dict__)


class Section(SectionBase):
    def __eq__(self, other):
        if len(other.__dict__) != len(self.__dict__):
            return False
        for key, value in self.__dict__.items():
            if isinstance(value, np.ndarray):
                if not np.array_equal(value, other.__dict__[key]):
                    return False
            else:
                if value != other.__dict__[key]:
                    return False
        return True

    def get_points(self):
        return [Point(*p) for p in zip(self.x, self.y, self.z, self.distances,)]

    def set_points(self, points):
        self.x = np.array([p.x for p in points])
        self.y = np.array([p.y for p in points])
        self.z = np.array([p.z for p in points])
        self.distances = np.array([p.d for p in points])
        self.nb_points = len(points)
        return self


class Reach(ReachBase):
    def __init__(self, *args, **kwargs):
        self.crs_id = kwargs.pop("crs_id", None)
        super().__init__(*args, **kwargs)

    def __eq__(self, other):
        return other.__dict__ == self.__dict__

    def get_sections(self):
        return self.sections.values()

    def set_sections(self, sections):
        self.sections = OrderedDict([(section.id, section) for section in sections])
        self.nsections = len(sections)
        return self

    def to_point_layer(self):
        source = "Point?index=yes&crs={}".format(self.crs_id)
        layer = QgsVectorLayer(source, self.name, "memory")
        pr = layer.dataProvider()

        fields = QgsFields()

        # Section fields
        fields.append(QgsField("sec_id", QVariant.Int))
        fields.append(QgsField("sec_name", QVariant.String))
        fields.append(QgsField("sec_pos", QVariant.Double))

        # Point fields
        fields.append(QgsField("p_id", QVariant.Int))
        fields.append(QgsField("p_pos", QVariant.Double))
        fields.append(QgsField("p_z", QVariant.Double))

        assert pr.addAttributes(fields)

        f = QgsFeature()
        for section in self.sections.values():
            for index, point in enumerate(section.get_points()):
                f.setAttributes(
                    [section.id, section.name, section.pk, index, point.d, point.z]
                )
                if str(point.z) == "NULL":
                    f.setGeometry(QgsGeometry(QgsPoint(point.x, point.y,)))
                else:
                    f.setGeometry(QgsGeometry(QgsPoint(point.x, point.y, point.z,)))
                pr.addFeature(f)

        layer.reload()

        return layer

    @staticmethod
    def from_point_layer(layer: QgsVectorLayer):
        reach = Reach(my_id=0, name=layer.name(), crs_id=layer.crs().authid(),)

        section = None
        points = []
        for f in layer.getFeatures():
            if section is not None:
                if f.attribute("sec_id") != section.id:
                    reach.add_section(section.set_points(points))
                    section = None
                    points = []

            if section is None:
                section = Section(
                    my_id=f.attribute("sec_id"),
                    pk=f.attribute("sec_pos"),
                    name=f.attribute("sec_name"),
                )

            points.append(
                Point(
                    x=f.geometry().constGet().x(),
                    y=f.geometry().constGet().y(),
                    z=f.attribute("p_z"),
                    d=f.attribute("p_pos"),
                )
            )
        if section is not None:
            reach.add_section(section.set_points(points))

        return reach

    def to_line_layer(self):
        source = "LineString?index=yes&crs={}".format(self.crs_id)
        layer = QgsVectorLayer(source, self.name, "memory")
        pr = layer.dataProvider()

        fields = QgsFields()

        # Section fields
        fields.append(QgsField("sec_id", QVariant.Int))
        fields.append(QgsField("sec_name", QVariant.String))
        fields.append(QgsField("sec_pos", QVariant.Double))

        # Point fields
        fields.append(QgsField("p_id", QVariant.String))
        fields.append(QgsField("p_pos", QVariant.String))
        fields.append(QgsField("p_z", QVariant.String))

        assert pr.addAttributes(fields)

        for section in self.sections.values():
            points = section.get_points()
            f = QgsFeature()
            f.setAttributes(
                [
                    section.id,
                    section.name,
                    section.pk,
                    ",".join([str(i) for i in range(0, len(points))]),
                    ",".join([str(p.d) for p in points]),
                    ",".join([str(p.z) for p in points]),
                ]
            )
            f.setGeometry(
                QgsGeometry(
                    QgsLineString(
                        [
                            QgsPoint(point.x, point.y,)
                            if str(point.z) == "NULL"
                            else QgsPoint(point.x, point.y, point.z,)
                            for point in points
                        ]
                    )
                )
            )
            pr.addFeature(f)

        layer.reload()

        return layer

    @staticmethod
    def from_line_layer(layer: QgsVectorLayer):
        reach = Reach(my_id=0, name=layer.name(), crs_id=layer.crs().authid(),)

        section = None
        for f in layer.getFeatures():

            section = Section(
                my_id=f.attribute("sec_id"),
                name=f.attribute("sec_name"),
                pk=f.attribute("sec_pos"),
            )

            # Take only the first parts (QgsMultiLineString => QgsLineString)
            line = next(f.geometry().constParts())

            section.set_points(
                [
                    Point(x=p[0].x(), y=p[0].y(), z=p[1], d=p[2],)
                    for p in zip(
                        line.points(),
                        f.attribute("p_z").split(","),
                        f.attribute("p_pos").split(","),
                    )
                ]
            )

            reach.add_section(section)

        return reach
