import os
import unittest

from qgis.core import QgsVectorLayer
from qgis.PyQt import QtGui

from PreCourlis.core.precourlis_file import PreCourlisFileLine

from .. import PROFILE_LINES_PATH, EXPECTED_PATH, TEMP_PATH, OVERWRITE_EXPECTED, utils


class TestPreCourlisFileLine(unittest.TestCase):
    def create_file(self):
        layer = QgsVectorLayer(PROFILE_LINES_PATH, "profiles", "ogr")
        assert layer.isValid()
        return PreCourlisFileLine(layer)

    def test_add_sedimental_layer(self):
        output_path = os.path.join(TEMP_PATH, "add_sedimental_layer.gml")
        expected_path = os.path.join(EXPECTED_PATH, "add_sedimental_layer.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        file = self.create_file()
        file.layer().startEditing()
        file.add_sedimental_layer("Layer2", 1)

        output = utils.save_as_gml(file.layer(), output_path)
        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()
        self.assertLayersEqual(output, expected)

    def test_delete_sedimental_layer(self):
        output_path = os.path.join(TEMP_PATH, "remove_sedimental_layer.gml")
        expected_path = os.path.join(EXPECTED_PATH, "remove_sedimental_layer.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        file = self.create_file()
        file.layer().startEditing()
        file.delete_sedimental_layer("Layer1")

        output = utils.save_as_gml(file.layer(), output_path)
        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()
        self.assertLayersEqual(output, expected)

    def test_layer_color(self):
        file = self.create_file()
        assert file.layer_color("zfond") == "#ff0000"
        file.set_layer_color("Layer1", QtGui.QColor("#7f7f7f"))
        assert file.layer_color("Layer1") == "#7f7f7f"
