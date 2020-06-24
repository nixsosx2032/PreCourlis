from qgis.PyQt import QtCore

from PreCourlis.core import is_null


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

    def flags(self, index):
        if index.isValid():
            if index.column() >= 1:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
                print(True)
            else:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        prop = getattr(self.section, self.property_list[index.column()])
        if role == QtCore.Qt.DisplayRole:
            v = prop[index.row()]
            return str(round(v, 3)) if v is not None else None
        if role == QtCore.Qt.EditRole:
            return prop[index.row()]

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:
            prop = getattr(self.section, self.property_list[index.column()])
            prop[index.row()] = value if not is_null(value) else None
            print("setData", index.row(), index.column(), value, prop[index.row()])
        return False
