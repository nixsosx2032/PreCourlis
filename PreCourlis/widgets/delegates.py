from qgis.PyQt import QtCore, QtWidgets


class FloatDelegate(QtWidgets.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setDecimals(3)
        editor.setSingleStep(0.001)
        editor.setAccelerated(True)
        return editor

    def setEditorData(self, editor, index):
        if not editor:
            return
        value = index.model().data(index, QtCore.Qt.EditRole)
        print("setEditorData", value)
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        if not editor:
            return
        print("setModelData", index.row(), index.column(), editor.value())
        model.setData(index, editor.value(), QtCore.Qt.EditRole)
