import unittest
from unittest.mock import patch

from qgis.core import QgsProject, QgsVectorLayer
from qgis.testing.mocked import get_iface as get_iface_base

from PreCourlis.widgets.profile_dialog import ProfileDialog

from .. import PROFILE_LINES_PATH


def get_iface():
    layer = QgsVectorLayer(PROFILE_LINES_PATH, "profiles_lines", "ogr")
    assert layer.isValid()

    project = QgsProject.instance()
    project.addMapLayer(layer)

    iface = get_iface_base()
    iface.activeLayer.return_value = layer
    return iface


class TestProfileDialog(unittest.TestCase):
    """Test dialog works."""

    def create_dialog(self):
        return ProfileDialog(None)

    @patch("PreCourlis.widgets.profile_dialog.iface", get_iface())
    def test_init(self):
        """Test we can click OK."""
        self.dialog = self.create_dialog()
