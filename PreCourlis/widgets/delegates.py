from qgis.PyQt import QtCore, QtWidgets


class FloatDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setDecimals(3)
        editor.setSingleStep(0.001)
        editor.setAccelerated(True)
        editor.valueChanged.connect(self.value_changed)
        return editor

    def setEditorData(self, editor, index):
        if not editor:
            return
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        if not editor:
            return
        model.setData(index, editor.value(), QtCore.Qt.EditRole)

    def value_changed(self, value):
        """Update the model on each valueChanged signals"""
        self.commitData.emit(self.sender())
