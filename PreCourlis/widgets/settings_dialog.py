import os
from pkg_resources import resource_filename

from qgis.PyQt import QtWidgets, uic

from PreCourlis.core.settings import settings

FORM_CLASS, _ = uic.loadUiType(resource_filename("PreCourlis", "ui/settings_dialog.ui"))


class SettingsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)
        self.setupUi(self)
        self.defaultElevationQgsDoubleSpinBox.setMinimum(
            settings.get_spin_box_min()
        )
        self.defaultElevationQgsDoubleSpinBox.setClearValue(
            settings.get_spin_box_min(),
            self.tr('Not set')
        )
        self.loadSetting()

    def accept(self, *args, **kwargs):
        self.saveSettings()
        super().accept(*args, **kwargs)

    def defaultElevation(self):
        return self.defaultElevationQgsDoubleSpinBox.value()

    def setDefaultElevation(self, value):
        self.defaultElevationQgsDoubleSpinBox.setValue(value)

    def loadSetting(self):
        self.setDefaultElevation(settings.default_elevation)

    def saveSettings(self):
        settings.default_elevation = self.defaultElevation()
