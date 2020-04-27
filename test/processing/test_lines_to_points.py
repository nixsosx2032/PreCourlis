import os

from qgis.core import QgsVectorLayer

import processing

from .. import DATA_PATH, EXPECTED_PATH, TEMP_PATH
from . import TestCase, OVERWRITE_EXPECTED

INPUT_PATH = os.path.join(DATA_PATH, "profiles_lines.shp")


class TestLinesToPointsAlgorithm(TestCase):
    def test_algorithm(self):
        output_path = os.path.join(TEMP_PATH, "lines_to_points.gml")
        expected_path = os.path.join(EXPECTED_PATH, "lines_to_points.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:lines_to_points", {"INPUT": INPUT_PATH, "OUTPUT": output_path}
        )
        output = QgsVectorLayer(outputs["OUTPUT"], "output", "ogr")
        assert output.isValid()

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()
        self.assertLayersEqual(output, expected)
