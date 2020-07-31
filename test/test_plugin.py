import unittest

from qgis.utils import iface

from PreCourlis.PreCourlis import PreCourlisPlugin


class PreCourlisPluginTest(unittest.TestCase):
    def test_plugin(self):
        plugin = PreCourlisPlugin(iface)
        plugin.initGui()
        plugin.unload()
