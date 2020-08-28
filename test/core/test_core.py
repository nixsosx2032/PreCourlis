import unittest
import logging

from qgis.PyQt.QtCore import QVariant

from PreCourlis.core import Point, Section, Reach

LOG = logging.getLogger(__name__)


class TestPoint(unittest.TestCase):
    def test_init(self):
        p = Point(0, 0, 0, 0)
        assert p.x == 0.0
        assert p.y == 0.0
        assert p.z == 0.0
        assert p.d == 0.0

        p = Point(0, 0, QVariant(), 0)
        assert p.z is None

    def test_eq(self):
        assert Point(0.0, 0.0, 0.0, 0.0) == Point(0.0, 0.0, 0.0, 0.0)
        assert Point(0.0, 0.0, 0.0, 0.0) != Point(1.0, 0.0, 0.0, 0.0)


class TestSection(unittest.TestCase):
    def test_set_get_points(self):
        points = [Point(v, v, v, v) for v in range(0, 10)]

        section = Section(
            my_id=0,
            pk=0.0,
            name="test_section",
        )
        section.set_points(points)
        assert section.get_points() == points


class TestReach(unittest.TestCase):
    def get_sections(self):
        return [
            Section(
                my_id=s,
                pk=float(s),
                name="test_section_{}".format(s),
            ).set_points([Point(v, v, v, v) for v in range(0, 10)])
            for s in range(0, 10)
        ]

    def test_eq(self):
        r1 = Reach(0, "test_reach")
        r1.set_sections(self.get_sections())

        r2 = Reach(0, "test_reach")
        r2.set_sections(self.get_sections())
        assert r1 == r2

        for section in r2.sections.values():
            section.x[0] = 3.0
            break
        assert r1 != r2

    def test_point_layer(self):
        r1 = Reach(0, "test_reach", crs_id="EPSG:2154")
        r1.set_sections(self.get_sections())
        layer = r1.to_point_layer()
        r2 = Reach.from_point_layer(layer)
        assert r1 == r2

    def test_line_layer(self):
        r1 = Reach(0, "test_reach", crs_id="EPSG:2154")
        r1.set_sections(self.get_sections())
        layer = r1.to_line_layer()
        r2 = Reach.from_line_layer(layer)
        assert r1 == r2
