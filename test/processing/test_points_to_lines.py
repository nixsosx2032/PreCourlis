import os

from qgis.core import QgsVectorLayer

import processing

from .. import DATA_PATH, EXPECTED_PATH, TEMP_PATH, OVERWRITE_EXPECTED
from . import TestCase


class TestPointsToLinesAlgorithm(TestCase):
    def test_algorithm(self):
        output_path = os.path.join(TEMP_PATH, "points_to_lines.gml")
        expected_path = os.path.join(EXPECTED_PATH, "points_to_lines.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:points_to_lines",
            {
                "INPUT": os.path.join(DATA_PATH, "input", "profiles_points.gml"),
                "OUTPUT": output_path,
            },
        )
        output = QgsVectorLayer(outputs["OUTPUT"], "output", "ogr")
        assert output.isValid()

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()

        self.assertLayersEqual(expected, output)
