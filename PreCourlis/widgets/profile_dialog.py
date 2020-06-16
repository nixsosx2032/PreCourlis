from pkg_resources import resource_filename

from qgis.core import (
    QgsFeatureRequest,
    QgsMapLayer,
    QgsProject,
    QgsWkbTypes,
)
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.utils import iface

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(
    resource_filename("PreCourlis", "ui/profile_dialog_base.ui")
)


class ProfileComboxModel(QtGui.QStandardItemModel):
    def setLayer(self, layer):
        self.clear()
        if layer is None:
            return

        sec_name_index = layer.fields().indexFromName("sec_name")
        request = QgsFeatureRequest()
        request.addOrderBy("sec_id")
        request.setSubsetOfAttributes([sec_name_index])
        for f in layer.getFeatures(request):
            item = QtGui.QStandardItem(f.attribute(sec_name_index))
            self.appendRow(item)


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

        self.profileComboBoxModel = ProfileComboxModel(self)

        self.init_layer_combo_box()
        self.init_profiles_combo_box()

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

    def init_profiles_combo_box(self):
        self.profileComboBox.setModel(self.profileComboBoxModel)

    def layer_changed(self, layer):
        self.profileComboBoxModel.setLayer(layer)

    def layer(self):
        return self.layerComboBox.currentLayer()
