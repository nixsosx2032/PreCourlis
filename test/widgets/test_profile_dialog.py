import unittest

from qgis.core import QgsProject, QgsVectorLayer
from qgis.utils import iface

from PreCourlis.widgets.profile_dialog import ProfileDialog

from .. import PROFILE_LINES_PATH


class TestProfileDialog(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        layer = QgsVectorLayer(PROFILE_LINES_PATH, "profiles_lines", "ogr")
        assert layer.isValid()
        QgsProject.instance().addMapLayer(layer)
        iface.activeLayer.return_value = layer

    def tearDown(self):
        QgsProject.instance().clear()
        iface.activeLayer.return_value = None

    def create_dialog(self):
        return ProfileDialog(None)

    def test_init(self):
        """Test we can click OK."""
        self.dialog = self.create_dialog()
