import unittest

from qgis.core import QgsFeatureRequest, QgsVectorLayer
from qgis.PyQt import QtCore

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.widgets.graph_widget import GraphWidget
from PreCourlis.widgets.points_table_model import PointsTableModel

from .. import PROFILE_LINES_PATH


class TestGraphWidgetBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestGraphWidgetBase, cls).setUpClass()
        cls.layer = QgsVectorLayer(PROFILE_LINES_PATH, "profiles_lines", "ogr")
        assert cls.layer.isValid()

    def create_widget(self):
        request = QgsFeatureRequest()
        request.setLimit(1)
        feature = next(self.layer.getFeatures(request))

        section = PreCourlisFileLine(self.layer).section_from_feature(feature)
        section.feature = feature

        widget = GraphWidget(None)

        model = PointsTableModel(widget)
        model.set_section(section)
        sel_model = QtCore.QItemSelectionModel(model, widget)
        widget.set_selection_model(sel_model)

        widget.set_sections(
            layer=self.layer,
            feature=feature,
            previous_section=None,
            current_section=section,
            next_section=None,
        )
        return widget


class TestGraphWidget(TestGraphWidgetBase):
    def test_init(self):
        self.create_widget()
