import os

from qgis.core import QgsVectorLayer

import processing

from .. import (
    DATA_PATH,
    PROFILE_LINES_PATH,
    EXPECTED_PATH,
    TEMP_PATH,
    OVERWRITE_EXPECTED,
)
from . import TestCase

AXIS_PATH = os.path.join(DATA_PATH, "input", "axeHydroBief1.shp")
CONSTRAINT_LINES = [
    os.path.join(DATA_PATH, "input", "riveDroiteBief1.shp"),
    os.path.join(DATA_PATH, "input", "riveGaucheBief1.shp"),
]


class TestInterpolateLinesAlgorithm(TestCase):
    def test_algorithm(self):
        output_path = os.path.join(TEMP_PATH, "interpolate_lines.gml")
        expected_path = os.path.join(EXPECTED_PATH, "interpolate_lines.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:interpolate_lines",
            {
                "SECTIONS": PROFILE_LINES_PATH,
                "AXIS": AXIS_PATH,
                "CONSTRAINT_LINES": CONSTRAINT_LINES,
                "LONG_STEP": 200,
                "LAT_STEP": 50,
                "ATTR_CROSS_SECTION": "sec_id",
                "OUTPUT": output_path,
            },
        )
        output = QgsVectorLayer(outputs["OUTPUT"], "output", "ogr")
        assert output.isValid()

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()

        self.assertLayersEqual(expected, output)
