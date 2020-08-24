import unittest

from qgis.core import QgsFeatureRequest, QgsVectorLayer
from qgis.PyQt import QtCore

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.widgets.points_table_model import PointsTableModel

from .. import PROFILE_LINES_PATH


class TestPointsTableModel(unittest.TestCase):
    """Test dialog works."""

    @classmethod
    def setUpClass(cls):
        super(TestPointsTableModel, cls).setUpClass()
        cls.layer = QgsVectorLayer(PROFILE_LINES_PATH, "profiles_lines", "ogr")
        assert cls.layer.isValid()

    def section(self):
        request = QgsFeatureRequest()
        request.setLimit(1)
        feature = next(self.layer.getFeatures(request))
        return PreCourlisFileLine(self.layer).section_from_feature(feature)

    def test_init(self):
        PointsTableModel(None)

    def test_set_section(self):
        model = PointsTableModel(None)
        model.set_section(self.section())

    def test_rowCount(self):
        model = PointsTableModel(None)
        model.set_section(self.section())
        assert model.rowCount() == 9

    def test_columnCount(self):
        model = PointsTableModel(None)
        model.set_section(self.section())
        assert model.columnCount() == 3

    def test_headerData(self):
        model = PointsTableModel(None)
        model.set_section(self.section())
        assert model.headerData(0, QtCore.Qt.Horizontal) == "abs_lat"
        assert model.headerData(1, QtCore.Qt.Horizontal) == "zfond"
        assert model.headerData(2, QtCore.Qt.Horizontal) == "Layer1"
        assert model.headerData(0, QtCore.Qt.Vertical) == "0"

    def test_flags(self):
        model = PointsTableModel(None)
        model.set_section(self.section())

        assert model.flags(model.index(0, 0)) == (
            QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        )

        assert model.flags(model.index(0, 1)) == (
            QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsEditable
        )

    def test_data(self):
        section = self.section()

        model = PointsTableModel(None)
        model.set_section(section)

        assert model.data(model.index(1, 0), QtCore.Qt.DisplayRole) == str(
            round(section.distances[1], 3)
        )
        assert model.data(model.index(1, 1), QtCore.Qt.DisplayRole) == str(
            round(section.z[1], 3)
        )
        assert model.data(model.index(1, 2), QtCore.Qt.DisplayRole) == str(
            round(section.layers_elev[0][1], 3)
        )

        assert model.data(model.index(1, 0), QtCore.Qt.EditRole) == section.distances[1]
        assert model.data(model.index(1, 1), QtCore.Qt.EditRole) == section.z[1]
        assert (
            model.data(model.index(1, 2), QtCore.Qt.EditRole)
            == section.layers_elev[0][1]
        )

    def test_setData(self):
        section = self.section()

        model = PointsTableModel(None)
        model.set_section(section)

        assert model.setData(model.index(1, 1), 10.0, QtCore.Qt.EditRole)
        assert section.z[1] == 10.0

        assert model.setData(model.index(1, 2), 10.0, QtCore.Qt.EditRole)
        assert section.layers_elev[0][1] == 10.0
