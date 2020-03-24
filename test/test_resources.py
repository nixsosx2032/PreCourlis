import unittest

from PyQt5.QtGui import QIcon


class TestPreCourlisPluginResources(unittest.TestCase):
    """Test rerources work."""

    def test_icon_png(self):
        """Test we can click OK."""
        path = ":/plugins/PreCourlisPlugin/icon.png"
        icon = QIcon(path)
        assert icon.isNull() is False
