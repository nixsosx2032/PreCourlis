from qgis.core import QgsFeatureRequest
from qgis.PyQt import QtGui


class SectionItem(QtGui.QStandardItem):
    def __init__(self, text, current_f_id, previous_f_id):
        super().__init__(text)
        self.current_f_id = current_f_id
        self.previous_f_id = previous_f_id
        self.next_f_id = None

    def set_next_f_id(self, next_f_id):
        self.next_f_id = next_f_id


class SectionItemModel(QtGui.QStandardItemModel):
    def setLayer(self, layer):
        self.beginResetModel()

        self.clear()
        if layer is None:
            return

        sec_name_index = layer.fields().indexFromName("sec_name")
        request = QgsFeatureRequest()
        request.addOrderBy("sec_id")
        request.setSubsetOfAttributes([sec_name_index])

        previous_f_id = None
        previous_item = None

        for f in layer.getFeatures(request):
            item = SectionItem(
                f.attribute(sec_name_index),
                f.id(),
                previous_f_id,
            )
            if previous_item is not None:
                previous_item.set_next_f_id(f.id())
            self.appendRow(item)

            previous_f_id = f.id()
            previous_item = item

        self.endResetModel()
