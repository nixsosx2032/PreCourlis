import os
import unittest

from qgis.core import QgsVectorLayer
from qgis.PyQt import QtGui

from PreCourlis.core.precourlis_file import PreCourlisFileLine

from .. import DATA_PATH, EXPECTED_PATH, TEMP_PATH, OVERWRITE_EXPECTED, utils

SECTIONS_PATH = os.path.join(DATA_PATH, "input", "profiles_lines.shp")


class TestPreCourlisFileLine(unittest.TestCase):
    def layer(self):
        return QgsVectorLayer(SECTIONS_PATH, "profiles", "ogr")

    def test_add_sedimental_layer(self):
        output_path = os.path.join(TEMP_PATH, "add_sedimental_layer.gml")
        expected_path = os.path.join(EXPECTED_PATH, "add_sedimental_layer.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        layer = QgsVectorLayer(SECTIONS_PATH, "profiles", "ogr")
        assert layer.isValid()

        layer.startEditing()
        PreCourlisFileLine(layer).add_sedimental_layer(
            "Layer1", QtGui.QColor(127, 127, 127, 255), 1
        )

        output = utils.save_as_gml(layer, output_path)
        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()
        self.assertLayersEqual(output, expected)
