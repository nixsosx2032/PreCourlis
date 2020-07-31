from mock import Mock
import unittest

from qgis.core import QgsFeatureRequest, QgsVectorLayer

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.widgets.graph_widget import GraphWidget

from .. import PROFILE_LINES_PATH


class TestProfileDialog(unittest.TestCase):
    """Test dialog works."""

    @classmethod
    def setUpClass(cls):
        super(TestProfileDialog, cls).setUpClass()
        cls.layer = QgsVectorLayer(PROFILE_LINES_PATH, "profiles_lines", "ogr")
        assert cls.layer.isValid()

    def create_widget(self):
        request = QgsFeatureRequest()
        request.setLimit(1)
        feature = next(self.layer.getFeatures(request))

        section = PreCourlisFileLine(self.layer).section_from_feature(feature)
        section.feature = feature

        widget = GraphWidget(None)
        widget.set_sections(
            layer=self.layer,
            feature=feature,
            previous_section=None,
            current_section=section,
            next_section=None,
        )
        return widget

    def test_init(self):
        self.create_widget()

    def test_set_current_point_index(self):
        widget = self.create_widget()
        widget.set_current_point_index(0)
        widget.set_current_point_index(1)

    def test_line_picker(self):
        widget = self.create_widget()

        mousevent = Mock()
        mousevent.xdata = widget.current_section.distances[2] + 10
        mousevent.ydata = widget.current_section.z[2] + 10

        widget.line_picker(widget.current_section_line, mousevent)
