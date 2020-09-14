from qgis.PyQt import QtCore, QtWidgets

import numpy as np


class SelectionTool:
    def __init__(self, canvas, graph):
        self.canvas = canvas
        self.graph = graph
        self.selection_model = None
        self.xdata = None
        self.ydatas = None
        self.column = None
        self.line = None
        self.previous_point_index = None
        self.editing = False
        self.editing_start = None

    def activate(self):
        self.cidpress = self.canvas.mpl_connect("button_press_event", self.on_press)
        self.cidmotion = self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.cidrelease = self.canvas.mpl_connect(
            "button_release_event", self.on_release
        )

    def deactivate(self):
        self.canvas.mpl_disconnect(self.cidpress)
        self.canvas.mpl_disconnect(self.cidmotion)
        self.canvas.mpl_disconnect(self.cidrelease)

    def set_selection_model(self, model):
        self.selection_model = model
        self.selection_model.selectionChanged.connect(self.selection_changed)

    def set_data(self, xdata, ydatas, column):
        self.xdata = xdata
        self.ydatas = ydatas
        self.column = column
        self.refresh_selection(draw=False)

    def selection_changed(self, selected, deselected):
        self.refresh_selection()

    def refresh_selection(self, dy=0, draw=True):
        if self.line is not None:
            # May already have been removed by clear
            if self.line in self.graph.lines:
                self.line.remove()
            self.line = None

        xdata = []
        ydata = []
        for index in self.selection_model.selection().indexes():
            xdata.append(self.xdata[index.row()])
            ydata.append(self.ydatas[index.column() - 1][index.row()] + dy)

        if self.line is None:
            (self.line,) = self.graph.plot(
                xdata,
                ydata,
                marker="o",
                markerfacecolor=None,
                markeredgecolor="tab:blue",
                fillstyle="none",
                linestyle="none",
                markersize=10,
                zorder=0,
                picker=10,
            )
        else:
            self.line.set_xdata(xdata)
            self.line.set_ydata(ydata)

        if draw:
            self.canvas.draw()

    def start_edit(self, x, y):
        # Start editing by translation
        self.editing = True
        self.editing_start = x, y
        self.motion_refresh(True)

    def motion_refresh(self, draw=True):
        if draw:
            self.line.set_animated(True)
            self.canvas.draw()
            self.background = self.canvas.copy_from_bbox(self.graph.bbox)
            self.graph.draw_artist(self.line)
            self.canvas.blit(self.graph.bbox)
        else:
            self.canvas.restore_region(self.background)
            self.graph.draw_artist(self.line)
            self.canvas.blit(self.graph.bbox)

    def finish_edit(self, x, y):
        dy = y - self.editing_start[1]
        for index in self.selection_model.selection().indexes():
            self.ydatas[index.column() - 1][index.row()] += dy
        self.canvas.editing_finished.emit()
        self.stop_editing()

    def stop_editing(self):
        self.editing = False
        self.line.set_animated(False)
        self.background = None
        self.refresh_selection()

    def on_press(self, event):
        if self.editing:
            self.stop_editing()

        if event.button != 1:
            return

        if event.xdata is None or event.ydata is None:
            return

        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if (
            not modifiers & QtCore.Qt.ShiftModifier
            and not modifiers & QtCore.Qt.ControlModifier
            and self.line is not None
        ):
            ok, points = self.line.contains(event)
            del points
            if ok:
                self.start_edit(event.xdata, event.ydata)
                return

        # Search for the closest
        d = np.sqrt(
            (self.xdata - event.xdata) ** 2.0
            + (self.ydatas[self.column - 1] - event.ydata) ** 2.0
        )
        ind = np.argmin(d)
        if ind is None:
            return

        # Define considered points
        if (
            modifiers & QtCore.Qt.ShiftModifier
            and not modifiers & QtCore.Qt.ControlModifier
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

        # Alter selection
        if QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ControlModifier:
            selection = self.selection_model.model().index(ind, self.column)
            self.selection_model.select(selection, QtCore.QItemSelectionModel.Toggle)
        else:
            self.selection_model.select(
                selection, QtCore.QItemSelectionModel.ClearAndSelect
            )

        self.refresh_selection()

    def on_motion(self, event):
        if event.button != 1:
            return

        if event.xdata is None or event.ydata is None:
            return

        if self.editing:
            dy = event.ydata - self.editing_start[1]
            bounds = self.graph.dataLim.bounds
            self.refresh_selection(dy, False)
            self.motion_refresh(self.graph.dataLim.bounds != bounds)

    def on_release(self, event):
        if event.button != 1:
            return

        if event.xdata is None or event.ydata is None:
            return

        if self.editing:
            self.finish_edit(event.xdata, event.ydata)
