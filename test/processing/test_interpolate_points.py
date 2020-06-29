import os

from qgis.core import (
    QgsProcessingUtils,
    QgsVectorLayer,
)

import processing

from .. import DATA_PATH, EXPECTED_PATH, TEMP_PATH, OVERWRITE_EXPECTED, utils
from . import TestCase

SECTIONS_PATH = os.path.join(DATA_PATH, "input", "profiles_points.shp")
AXIS_PATH = os.path.join(DATA_PATH, "input", "axeHydroBief1.shp")
CONSTRAINT_LINES = [
    os.path.join(DATA_PATH, "input", "riveDroiteBief1.shp"),
    os.path.join(DATA_PATH, "input", "riveGaucheBief1.shp"),
]


class TestInterpolatePointsAlgorithm(TestCase):
    def test_algorithm(self):
        output_path = os.path.join(TEMP_PATH, "interpolate_points.gml")
        expected_path = os.path.join(EXPECTED_PATH, "interpolate_points.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:interpolate_points",
            {
                "SECTIONS": SECTIONS_PATH,
                "AXIS": AXIS_PATH,
                "CONSTRAINT_LINES": CONSTRAINT_LINES,
                "LONG_STEP": 200,
                "LAT_STEP": 50,
                "ATTR_CROSS_SECTION": "sec_id",
                "OUTPUT": QgsProcessingUtils.generateTempFilename(
                    "interpolate_points.shp"
                ),
            },
        )
        output = QgsVectorLayer(outputs["OUTPUT"], "output", "ogr")
        assert output.isValid()

        output = utils.save_as_gml(output, output_path)

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()
        self.assertLayersEqual(output, expected)
