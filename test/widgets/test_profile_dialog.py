import os
import unittest
from unittest.mock import patch

from qgis.core import QgsProject, QgsVectorLayer
from qgis.testing.mocked import get_iface as get_iface_base

from PreCourlis.widgets.profile_dialog import ProfileDialog

from .. import DATA_PATH

PROFILES_PATH = os.path.join(DATA_PATH, "input", "profiles_lines.shp")


def get_iface():
    project = QgsProject.instance()
    layer = QgsVectorLayer(PROFILES_PATH, "profiles_lines", "ogr")
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
