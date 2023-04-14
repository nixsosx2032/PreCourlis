import unittest
from unittest.mock import patch, PropertyMock


class TestSettingsDialog(unittest.TestCase):
    """Test dialog works."""

    def create_dialog(self):
        from PreCourlis.widgets.settings_dialog import SettingsDialog
        return SettingsDialog(None)

    def test_setDefaultElevation(self):
        self.dialog = self.create_dialog()

        self.dialog.setDefaultElevation(9.0)
        assert self.dialog.defaultElevation() == 9.0

    def test_loadSettings(self):
        self.dialog = self.create_dialog()

        with patch.multiple(
            "PreCourlis.widgets.settings_dialog.settings",
            default_elevation="9.0",
        ):
            self.dialog.loadSetting()
        assert self.dialog.defaultElevation() == 9.0

