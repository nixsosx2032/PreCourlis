import unittest

from qgis.testing.mocked import get_iface

from PreCourlis.PreCourlis import PreCourlisPlugin

iface = get_iface()


class PreCourlisPluginTest(unittest.TestCase):
    def test_plugin(self):
        plugin = PreCourlisPlugin(iface)
        plugin.initGui()
        plugin.unload()
