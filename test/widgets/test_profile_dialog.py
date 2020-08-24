from mock import patch, call
import unittest

from qgis.core import QgsProject, QgsVectorLayer
from qgis.utils import iface
from qgis.PyQt import QtCore, QtGui

from PreCourlis.widgets.profile_dialog import ProfileDialog

from .. import PROFILE_LINES_PATH


class TestProfileDialog(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        self.layer = QgsVectorLayer(PROFILE_LINES_PATH, "profiles_lines", "ogr")
        assert self.layer.isValid()
        QgsProject.instance().addMapLayer(self.layer)
        iface.activeLayer.return_value = self.layer

    def tearDown(self):
        QgsProject.instance().clear()
        iface.activeLayer.return_value = None

    def create_dialog(self):
        return ProfileDialog(None)

    def test_init(self):
        """Test we can click OK."""
        self.dialog = self.create_dialog()

    def test_previous_section(self):
        self.dialog = self.create_dialog()

        with patch.object(self.dialog, "set_section") as set_section_mock:
            self.dialog.sectionComboBox.setCurrentText("P1")
            self.dialog.previous_section()
            assert self.dialog.sectionComboBox.currentText() == "P1"
            set_section_mock.assert_not_called()

        with patch.object(self.dialog, "set_section") as set_section_mock:
            self.dialog.sectionComboBox.setCurrentText("P2")
            self.dialog.previous_section()
            assert self.dialog.sectionComboBox.currentText() == "P1"
            assert set_section_mock.call_args_list == [call(1), call(0)]

    def test_next_section(self):
        self.dialog = self.create_dialog()

        with patch.object(self.dialog, "set_section") as set_section_mock:
            self.dialog.sectionComboBox.setCurrentText("P1")
            self.dialog.next_section()
            assert self.dialog.sectionComboBox.currentText() == "P2"
            assert set_section_mock.call_args_list == [call(1)]

        with patch.object(self.dialog, "set_section") as set_section_mock:
            self.dialog.sectionComboBox.setCurrentText("P6")
            self.dialog.next_section()
            assert self.dialog.sectionComboBox.currentText() == "P6"
            assert set_section_mock.call_args_list == [call(5)]

    def test_data_changed(self):
        self.dialog = self.create_dialog()

        with patch.object(self.dialog, "update_feature") as update_feature_mock:
            with patch.object(self.dialog.graphWidget.selection_tool, "editing", True):
                self.dialog.data_changed(None, None, None)
            update_feature_mock.assert_called_once_with(
                "Profile dialog graph translation"
            )

        with patch.object(self.dialog, "update_feature") as update_feature_mock:
            with patch.object(self.dialog, "interpolation", True):
                self.dialog.data_changed(None, None, None)
            update_feature_mock.assert_called_once_with("Profile dialog interpolation")

        with patch.object(self.dialog, "update_feature") as update_feature_mock:
            self.dialog.data_changed(None, None, None)
            update_feature_mock.assert_called_once_with("Profile dialog table edit")

    def test_update_feature(self):
        self.dialog = self.create_dialog()
        self.dialog.update_feature("test")

    def test_add_layer(self):
        self.dialog = self.create_dialog()
        assert self.dialog.current_section.name == "P1"
        self.dialog.addLayerNameLineEdit.setText("new_layer")
        self.dialog.add_layer()

    def test_apply_layer(self):
        self.dialog = self.create_dialog()
        self.dialog.sedimentalLayerComboBox.setCurrentText("Layer1")
        self.dialog.addLayerNameLineEdit.setText("new_layer")
        self.dialog.selected_color = QtGui.QColor("#7f7f7f")
        self.dialog.apply_layer()

    def test_delete_layer(self):
        self.dialog = self.create_dialog()
        self.dialog.sedimentalLayerComboBox.setCurrentText("Layer1")
        self.dialog.delete_layer()

    def test_apply_interpolation(self):
        self.dialog = self.create_dialog()
        self.dialog.leftSpinBox.setValue(-0.5)
        self.dialog.leftSpinBox.setValue(-0.6)
        model = self.dialog.pointsTableModel
        self.dialog.pointsTableView.selectionModel().select(
            QtCore.QItemSelection(model.index(1, 1), model.index(4, 2)),
            QtCore.QItemSelectionModel.ClearAndSelect,
        )
        self.dialog.apply_interpolation()
