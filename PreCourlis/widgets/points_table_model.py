from qgis.PyQt import QtCore


class PointsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.section = None
        self.property_list = []

    def set_section(self, section):
        self.beginResetModel()
        self.section = section
        self.property_list = ["distances", "z"]
        self.endResetModel()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if self.section is None:
            return 0
        return len(getattr(self.section, self.property_list[0]))

    def columnCount(self, parent=QtCore.QModelIndex()):
        if self.section is None:
            return 0
        return len(self.property_list)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.property_list[section]
            if orientation == QtCore.Qt.Vertical:
                return section

    def data(self, index, role=QtCore.Qt.DisplayRole):
        prop = getattr(self.section, self.property_list[index.column()])
        if role == QtCore.Qt.DisplayRole:
            return str(round(prop[index.row()], 3))
        if role == QtCore.Qt.EditRole:
            return prop[index.row()]
