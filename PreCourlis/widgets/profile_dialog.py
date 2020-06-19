from pkg_resources import resource_filename

from qgis.core import (
    QgsFeatureRequest,
    QgsMapLayer,
    QgsProject,
    QgsWkbTypes,
)
from qgis.PyQt import QtCore, QtGui, QtWidgets, uic
from qgis.utils import iface

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.widgets.points_table_model import PointsTableModel

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    resource_filename("PreCourlis", "ui/profile_dialog_base.ui")
)


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
            item = SectionItem(f.attribute(sec_name_index), f.id(), previous_f_id,)
            if previous_item is not None:
                previous_item.set_next_f_id(f.id())
            self.appendRow(item)

            previous_f_id = f.id()
            previous_item = item

        self.endResetModel()


class ProfileDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ProfileDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.sectionItemModel = SectionItemModel(self)
        self.pointsTableModel = PointsTableModel(self)

        self.init_layer_combo_box()
        self.init_sections_combo_box()
        self.init_points_table_view()

        self.layer_changed(self.layer())

    def init_layer_combo_box(self):
        def accept_layer(layer):
            if layer.type() != QgsMapLayer.VectorLayer:
                return False
            if layer.geometryType() != QgsWkbTypes.LineGeometry:
                return False
            if layer.fields().indexFromName("sec_id") == -1:
                return False
            return True

        excluded_layers = []
        for layer in QgsProject.instance().mapLayers().values():
            if not accept_layer(layer):
                excluded_layers.append(layer)
        self.layerComboBox.setExceptedLayerList(excluded_layers)

        # Select active layer
        layer = iface.activeLayer()
        if layer not in excluded_layers:
            self.layerComboBox.setLayer(layer)

        self.layerComboBox.layerChanged.connect(self.layer_changed)

    def init_sections_combo_box(self):
        self.sectionComboBox.setModel(self.sectionItemModel)
        self.sectionComboBox.currentIndexChanged.connect(self.section_changed)
        self.previousSectionButton.clicked.connect(self.previous_section)
        self.nextSectionButton.clicked.connect(self.next_section)

    def init_points_table_view(self):
        self.pointsTableView.setModel(self.pointsTableModel)
        self.pointsTableView.selectionModel().currentRowChanged.connect(
            self.current_row_changed
        )

    def layer(self):
        return self.layerComboBox.currentLayer()

    def layer_changed(self, layer):
        self.sectionItemModel.setLayer(layer)
        self.sectionComboBox.setCurrentIndex(0)

    def section_from_feature_id(self, f_id):
        if f_id is None:
            return None
        f = self.layer().getFeature(f_id)
        section = PreCourlisFileLine.section_from_feature(f)
        section.feature = f
        return section

    def section_changed(self, index):
        if index == -1:
            self.graphWidget.clear()
            return

        item = self.sectionItemModel.item(index)

        self.layer().selectByIds([item.current_f_id])

        current_section = self.section_from_feature_id(item.current_f_id)

        self.pointsTableModel.set_section(current_section)

        self.graphWidget.set_sections(
            self.section_from_feature_id(item.previous_f_id),
            current_section,
            self.section_from_feature_id(item.next_f_id),
        )

    def previous_section(self):
        if self.sectionComboBox.currentIndex() < 1:
            return
        self.sectionComboBox.setCurrentIndex(self.sectionComboBox.currentIndex() - 1)

    def next_section(self):
        if self.sectionComboBox.currentIndex() > self.sectionItemModel.rowCount() - 2:
            return
        self.sectionComboBox.setCurrentIndex(self.sectionComboBox.currentIndex() + 1)

    def current_row_changed(self, current, previous):
        position = self.pointsTableModel.data(
            self.pointsTableModel.index(current.row(), 0), QtCore.Qt.EditRole,
        )
        self.graphWidget.set_position(position)
