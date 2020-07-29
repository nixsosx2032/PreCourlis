import math

from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsLineString,
    QgsPoint,
    QgsRasterLayer,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QVariant

from PreCourlis.core import is_null, Point, Reach, Section
from PreCourlis.core.utils import qgslinestring_angle, color_to_hex
from qgis._core import QgsCoordinateReferenceSystem


class PreCourlisFileBase:
    def __init__(self, layer: QgsVectorLayer):
        self._layer = layer  # Layer is supposed to be the unique storage

    @staticmethod
    def section_fields():
        fields = QgsFields()
        # Section fields
        fields.append(QgsField("sec_id", QVariant.Int))
        fields.append(QgsField("sec_name", QVariant.String))
        fields.append(QgsField("abs_long", QVariant.Double))
        fields.append(QgsField("axis_x", QVariant.Double))
        fields.append(QgsField("axis_y", QVariant.Double))
        fields.append(QgsField("layers", QVariant.String))
        return fields

    @staticmethod
    def create_layer(self, name, source=None, crs_id=None, type_="LineString"):
        if source is None:
            source = "{}?index=yes".format(type_)
        layer = QgsVectorLayer(source, name, "memory")
        if crs_id is not None:
            crs = QgsCoordinateReferenceSystem()
            crs.createFromString(crs_id)
            layer.setCrs(crs)

        pr = layer.dataProvider()
        assert pr.addAttributes(self.basefields())
        layer.updateFields()

        return layer


class PreCourlisFileLine(PreCourlisFileBase):
    @staticmethod
    def base_fields():
        fields = PreCourlisFileBase.section_fields()
        # Point fields
        fields.append(QgsField("p_id", QVariant.String))
        fields.append(QgsField("p_pos", QVariant.String))
        fields.append(QgsField("p_z", QVariant.String))
        return fields

    @staticmethod
    def create_layer(self, name, source=None, crs_id=None):
        return super().create_layer(self, name, source, crs_id, "LineString")

    def import_tracks(
        self,
        name: str,
        axis: QgsVectorLayer,
        tracks: QgsVectorLayer,
        first_pos: int,
        name_field: str,
        step: int,
        dem: QgsRasterLayer,
    ):
        """"
        Construct standard line layer from tracks:
            - Construct a standard reach line layer
            - Reverse geometry if needed (depending on axis direction)
            - Populate attributes:
                - sec_id
                - sec_name
                - abs_long
        """
        if self._layer is None:
            self._layer = self.create_layer(name, tracks.crs().authid())

        axis = next(axis.getFeatures())

        pr = self._layer.dataProvider()

        id_ = 0
        name_field_index = tracks.fields().indexFromName(name_field)
        for track in tracks.getFeatures():

            intersection = track.geometry().intersection(axis.geometry())
            assert not intersection.isNull()

            abs_long = axis.geometry().lineLocatePoint(intersection)

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
                    else "P_{:.3}".format(abs_long),
                    first_pos + abs_long,
                    intersection_point.x(),
                    intersection_point.y(),
                    "",
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

        self._layer.reload()

    def get_sections(self):
        for f in self._layer.getFeatures():
            yield self.section_from_feature(f)

    def section_from_feature(self, f):
        section = Section(
            my_id=f.attribute("sec_id"),
            name=f.attribute("sec_name"),
            pk=f.attribute("abs_long"),
        )
        section.axis = [f.attribute("axis_x"), f.attribute("axis_y")]

        def split_attribute(v, length):
            if is_null(v):
                return [None] * length
            return v.split(",")

        # Take only the first parts (QgsMultiLineString => QgsLineString)
        line = next(f.geometry().constParts())
        points = line.points()
        section.set_points(
            [
                Point(x=p[0].x(), y=p[0].y(), z=p[1], d=p[2],)
                for p in zip(
                    points,
                    split_attribute(f.attribute("p_z"), len(points)),
                    split_attribute(f.attribute("p_pos"), len(points)),
                )
            ]
        )
        section.set_layers(
            self.layers(),
            [
                split_attribute(f.attribute(layer), len(points))
                for layer in self.layers()
            ],
        )

        return section

    @staticmethod
    def feature_from_section(section):
        points = section.get_points()
        f = QgsFeature()
        f.setAttributes(
            [
                section.id,
                section.name,
                section.pk,
                section.axis[0],
                section.axis[1],
                "",
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
        return f

    def add_section(self, section):
        self._layer.dataProvider().addFeature(self.feature_from_section(section))
        self.reload()

    """
    def sections(self):
        return OrderedDict([(s.id, s) for s in self.get_section()])
    """

    def get_reach(self):
        reach = Reach(
            my_id=0, name=self._layer.name(), crs_id=self._layer.crs().authid(),
        )
        for section in self.get_sections():
            reach.add_section(section)
        return reach

    def set_reach(self, reach):
        for section in reach.values():
            self.add_section(section)
        self._layer.reload()

    def layers(self, feature=None):
        if feature is None:
            request = QgsFeatureRequest()
            request.setLimit(1)
            feature = next(self._layer.getFeatures(request))
        value = feature.attribute("layers")
        if is_null(value) or value == "":
            return []
        return value.split(",")

    def layer_color(self, layer):
        return self._layer.customProperty("PreCoulis_{}_Color".format(layer))

    def set_layer_color(self, layer, color):
        self._layer.setCustomProperty(
            "PreCoulis_{}_Color".format(layer), color_to_hex(color)
        )

    def add_sedimental_layer(self, name, thickness=0):
        layers = self.layers()
        if name in layers:
            raise KeyError("Layer {} already exists".format(name))

        field_name = name
        self._layer.beginEditCommand("Add sedimental layer {}".format(name))

        # Add new attribute
        self._layer.addAttribute(QgsField(field_name, QVariant.String))
        self._layer.updateFields()

        # Update layers list and set value of new attribute
        source_field_name = "p_z"
        if len(layers) > 0:
            source_field_name = layers[-1]
        layers.append(name)
        layers_list = ",".join(layers)
        layers_field_index = self._layer.fields().indexFromName("layers")
        source_field_index = self._layer.fields().indexFromName(source_field_name)
        dest_field_index = self._layer.fields().indexFromName(field_name)
        for f in self._layer.getFeatures():
            self._layer.changeAttributeValue(f.id(), layers_field_index, layers_list)
            value = f.attribute(source_field_index)
            if not is_null(value):
                values = value.split(",")
                value = ",".join([str(float(v) - thickness) for v in values])
            self._layer.changeAttributeValue(f.id(), dest_field_index, value)

        self._layer.endEditCommand()

    def delete_sedimental_layer(self, name):
        self._layer.beginEditCommand("Remove sedimental layer {}".format(name))

        # Remove attribute
        field_index = self._layer.fields().indexFromName(name)
        self._layer.deleteAttribute(field_index)

        # Update layers list
        layers = self.layers()
        print(layers)
        layers.pop(layers.index(name))
        print(layers)
        layers_list = ",".join(layers)
        layers_field_index = self._layer.fields().indexFromName("layers")
        for f in self._layer.getFeatures():
            self._layer.changeAttributeValue(f.id(), layers_field_index, layers_list)

        self._layer.endEditCommand()


class PreCourlisFilePoint(PreCourlisFileBase):
    @staticmethod
    def base_fields():
        fields = PreCourlisFileBase.section_fields()
        # Point fields
        fields.append(QgsField("p_id", QVariant.Int))
        fields.append(QgsField("p_pos", QVariant.Double))
        fields.append(QgsField("p_z", QVariant.Double))
        return fields

    @staticmethod
    def create_layer(self, name, source, crs_id):
        return super().create_layer(name, source, crs_id, "Point")

    def add_reach(self):
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
                self._layer.dataProvider().addFeature(f)
        self._layer.reload()

    def get_reach(self):
        reach = Reach(
            my_id=0, name=self._layer.name(), crs_id=self._layer.crs().authid(),
        )

        section = None
        points = []
        for f in self._layer.getFeatures():
            if section is not None:
                if f.attribute("sec_id") != section.id:
                    reach.add_section(section.set_points(points))
                    section = None
                    points = []

            if section is None:
                section = Section(
                    my_id=f.attribute("sec_id"),
                    pk=f.attribute("abs_long"),
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
