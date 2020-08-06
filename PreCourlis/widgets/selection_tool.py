from qgis.PyQt import QtCore, QtWidgets

import numpy as np


class SelectionTool(QtCore.QObject):
    def __init__(self, canvas, graph):
        super().__init__(canvas)
        self.canvas = canvas
        self.graph = graph
        self.selection_model = None
        self.section = None
        self.xdata = None
        self.ydata = None
        self.column = None
        self.line = None
        self.previous_point_index = None

    def activate(self):
        self.cidpress = self.canvas.mpl_connect("button_press_event", self.on_press)

    def deactivate(self):
        self.canvas.mpl_disconnect(self.cidpress)

    def set_selection_model(self, model):
        self.selection_model = model
        self.selection_model.selectionChanged.connect(self.selection_changed)

    def set_section(self, section):
        self.section = section

    def set_data(self, xdata, ydata, column):
        self.xdata = xdata
        self.ydata = ydata
        self.column = column

    def selection_changed(self, selected, deselected):
        self.refresh_selection()

    def refresh_selection(self, draw=True):
        if self.line is not None:
            self.line.remove()
            self.line = None

        xdata = []
        ydata = []
        section = self.section
        for index in self.selection_model.selection().indexes():
            if index.column() == 1:
                xdata.append(section.distances[index.row()])
                ydata.append(section.z[index.row()])
            if index.column() > 1:
                xdata.append(section.distances[index.row()])
                ydata.append(section.layers_elev[index.column() - 2][index.row()])

        (self.line,) = self.graph.plot(xdata, ydata, "bo", zorder=0,)

        if draw:
            self.canvas.draw()

    def on_press(self, event):
        if event.button != 1:
            return

        # Search for the closest point
        d = np.sqrt(
            (self.xdata - event.xdata) ** 2.0 + (self.ydata - event.ydata) ** 2.0
        )
        ind = np.argmin(d)
        if ind is None:
            return

        if (
            QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ShiftModifier
            and self.previous_point_index is not None
        ):
            selection = QtCore.QItemSelection(
                self.selection_model.model().index(
                    self.previous_point_index, self.column
                ),
                self.selection_model.model().index(ind, self.column),
            )
        else:
            selection = self.selection_model.model().index(ind, self.column)

        self.previous_point_index = ind

        if QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ControlModifier:
            self.selection_model.select(selection, QtCore.QItemSelectionModel.Toggle)
        else:
            self.selection_model.select(
                selection, QtCore.QItemSelectionModel.ClearAndSelect
            )

        self.refresh_selection()
