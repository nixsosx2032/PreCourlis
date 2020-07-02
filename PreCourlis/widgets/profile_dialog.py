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
from PreCourlis.widgets.delegates import FloatDelegate
from PreCourlis.widgets.points_table_model import PointsTableModel
from PreCourlis.widgets.sedimental_layer_model import SedimentalLayerModel

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

        self.file = None
        self.current_section = None
        self.selected_color = None
        self.splitter.setSizes([200, 400])

        self.sectionItemModel = SectionItemModel(self)
        self.pointsTableModel = PointsTableModel(self)
        self.pointsTableModel.dataChanged.connect(self.data_changed)
        self.sedimentalLayerModel = SedimentalLayerModel(self)

        self.init_layer_combo_box()
        self.init_sections_combo_box()
        self.init_points_table_view()
        self.init_edition_panel()

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
        self.pointsTableView.setItemDelegate(FloatDelegate(self))
        self.pointsTableView.setModel(self.pointsTableModel)
        self.pointsTableView.selectionModel().currentRowChanged.connect(
            self.current_row_changed
        )

    def init_edition_panel(self):
        self.sedimentalLayerComboBox.setModel(self.sedimentalLayerModel)
        self.sedimentalLayerComboBox.currentIndexChanged.connect(
            self.sedimental_layer_changed
        )
        self.addLayerColorButton.clicked.connect(self.add_layer_select_color)
        self.addLayerButton.clicked.connect(self.add_layer)
        self.applyLayerButton.clicked.connect(self.apply_layer)
        self.deleteLayerButton.clicked.connect(self.delete_layer)

    def layer(self):
        return self.layerComboBox.currentLayer()

    def layer_changed(self, layer):
        self.file = PreCourlisFileLine(layer)
        self.sectionItemModel.setLayer(layer)
        self.sectionComboBox.setCurrentIndex(0)
        self.sedimentalLayerModel.setLayer(layer)
        self.sedimentalLayerComboBox.setCurrentIndex(0)

    def section_from_feature_id(self, f_id):
        if f_id is None:
            return None
        f = self.layer().getFeature(f_id)
        section = self.file.section_from_feature(f)
        section.feature = f
        return section

    def section_changed(self, index):
        if index == -1:
            self.graphWidget.clear()
            return

        item = self.sectionItemModel.item(index)

        # Select current feature in vector layer
        self.layer().selectByIds([item.current_f_id])

        self.current_section = self.section_from_feature_id(item.current_f_id)

        self.pointsTableModel.set_section(self.current_section)

        self.graphWidget.set_sections(
            self.layer(),
            self.layer().getFeature(item.current_f_id),
            self.section_from_feature_id(item.previous_f_id),
            self.current_section,
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

    def data_changed(self, topLeft, bottomRight, roles):
        self.graphWidget.refresh_current_section()

    def sedimental_layer(self):
        return self.sedimentalLayerComboBox.currentText()

    def sedimental_layer_changed(self, index):
        layer = self.sedimental_layer()
        self.addLayerNameLineEdit.setText(layer)
        if index == 0:
            self.set_new_layer_color("#ff0000")
        else:
            self.set_new_layer_color(self.file.layer_color(layer))

    def add_layer_select_color(self):
        self.set_new_layer_color(
            QtWidgets.QColorDialog.getColor(
                self.selected_color or QtGui.QColor("#7f7f7f")
            )
        )

    def set_new_layer_color(self, color):
        stylesheet = ""
        if color is not None:
            if isinstance(color, str):
                color = QtGui.QColor(color)
            stylesheet = "background-color: rgba({}, {}, {}, 1);".format(
                color.red(), color.green(), color.blue(),
            )
        self.selected_color = color
        self.addLayerColorButton.setStyleSheet(stylesheet)

    def add_layer(self):
        name = self.addLayerNameLineEdit.text()

        self.layer().startEditing()
        self.file.add_sedimental_layer(name)
        self.layer.set_layer_color(name, self.selected_color)

        self.section_changed(self.sectionComboBox.currentIndex())

    def apply_layer(self):
        self.file.set_layer_color(self.sedimental_layer(), self.selected_color)
        self.graphWidget.refresh()

    def delete_layer(self):
        self.layer().startEditing()
        layer = self.sedimental_layer()
        self.sedimentalLayerComboBox.setCurrentIndex(
            self.sedimentalLayerComboBox.currentIndex() - 1
        )
        self.file.delete_sedimental_layer(layer)
        self.section_changed(self.sectionComboBox.currentIndex())
