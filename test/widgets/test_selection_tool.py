from mock import Mock, patch

from qgis.PyQt import QtCore

from PreCourlis.widgets.points_table_model import PointsTableModel

from test.widgets.test_graph_widget import TestGraphWidgetBase


class TestSelectionTool(TestGraphWidgetBase):
    def create_tool(self):
        self.widget = self.create_widget()
        self.section = self.widget.current_section
        tool = self.widget.selection_tool

        self.model = PointsTableModel(self.widget)
        self.model.set_section(self.section)
        tool.set_selection_model(QtCore.QItemSelectionModel(self.model, self.widget))

        tool.set_data(
            self.section.distances,
            [self.section.z] + list(self.section.layers_elev),
            1,
        )

        return tool

    def event(self, row):
        event = Mock()
        event.button = 1
        event.xdata = self.section.distances[row] + 10
        event.ydata = self.section.z[row] + 10
        event.x = 0
        event.y = 0
        return event

    def start_editing(self, tool):
        tool.selection_model.select(
            self.model.index(1, 1),
            QtCore.QItemSelectionModel.ClearAndSelect,
        )
        tool.refresh_selection()
        tool.start_edit(self.section.distances[1], self.section.z[1])

    def test_deactivate(self):
        tool = self.create_tool()
        tool.deactivate()

    def test_start_edit(self):
        tool = self.create_tool()
        self.start_editing(tool)

    def test_finish_edit(self):
        tool = self.create_tool()
        self.start_editing(tool)
        tool.finish_edit(self.section.distances[1] + 3, self.section.z[1] + 3)

    def test_motion_refresh(self):
        tool = self.create_tool()
        self.start_editing(tool)
        tool.motion_refresh(False)
        tool.motion_refresh(True)

    def test_on_press(self):
        tool = self.create_tool()
        tool.on_press(self.event(2))
        indexes = tool.selection_model.selection().indexes()
        assert len(indexes) == 1
        assert indexes[0].row() == 2
        assert indexes[0].column() == 1

    def test_on_press_layer(self):
        tool = self.create_tool()
        tool.column = 2
        tool.on_press(self.event(2))
        indexes = tool.selection_model.selection().indexes()
        assert len(indexes) == 1
        assert indexes[0].row() == 2
        assert indexes[0].column() == 2

    @patch(
        "PreCourlis.widgets.selection_tool.QtWidgets.QApplication.keyboardModifiers",
        return_value=QtCore.Qt.ControlModifier,
    )
    def test_on_press_ctrl(self, key_mod_mock):
        tool = self.create_tool()
        tool.on_press(self.event(2))
        tool.on_press(self.event(3))
        indexes = tool.selection_model.selection().indexes()
        assert len(indexes) == 2

    @patch(
        "PreCourlis.widgets.selection_tool.QtWidgets.QApplication.keyboardModifiers",
        return_value=QtCore.Qt.ShiftModifier,
    )
    def test_on_press_shift(self, key_mod_mock):
        tool = self.create_tool()
        tool.on_press(self.event(2))
        tool.on_press(self.event(4))
        indexes = tool.selection_model.selection().indexes()
        assert len(indexes) == 3

    def test_on_motion(self):
        tool = self.create_tool()
        self.start_editing(tool)

        event = Mock()
        event.button = 1
        event.xdata = tool.editing_start[0]
        event.ydata = tool.editing_start[1] + 3
        event.x = 0
        event.y = 0

        tool.on_motion(event)

    def test_on_release(self):
        tool = self.create_tool()
        self.start_editing(tool)

        event = Mock()
        event.button = 1
        event.xdata = tool.editing_start[0]
        event.ydata = tool.editing_start[1] + 3
        event.x = 0
        event.y = 0

        tool.on_release(event)
