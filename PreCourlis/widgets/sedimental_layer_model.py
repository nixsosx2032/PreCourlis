from qgis.PyQt import QtCore

from PreCourlis.core.precourlis_file import PreCourlisFileLine


class SedimentalLayerModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file = None

    def setLayer(self, layer):
        self.beginResetModel()
        self.file = PreCourlisFileLine(layer)
        self.endResetModel()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if self.file is None:
            return 0
        if self.file.layer() is None:
            return 0
        return len(self.file.layers()) + 1

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if index.row() == 0:
                if index.column() == 0:
                    return "zfond"
            layers = self.file.layers()
            if index.row() - 1 < len(layers):
                layer = self.file.layers()[index.row() - 1]
                if index.column() == 0:
                    return layer
