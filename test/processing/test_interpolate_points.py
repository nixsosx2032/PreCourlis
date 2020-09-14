import os

from qgis.core import (
    QgsProcessingUtils,
    QgsVectorLayer,
)

from .. import DATA_PATH, TEMP_PATH, utils
from . import TestCase

SECTIONS_PATH = os.path.join(DATA_PATH, "input", "profiles_points.gml")
AXIS_PATH = os.path.join(DATA_PATH, "input", "axeHydroBief1.shp")
CONSTRAINT_LINES = [
    os.path.join(DATA_PATH, "input", "riveDroiteBief1.shp"),
    os.path.join(DATA_PATH, "input", "riveGaucheBief1.shp"),
]


class TestInterpolatePointsAlgorithm(TestCase):

    ALGORITHM_ID = "precourlis:interpolate_points"
    DEFAULT_PARAMS = {
        "SECTIONS": SECTIONS_PATH,
        "AXIS": AXIS_PATH,
        "CONSTRAINT_LINES": CONSTRAINT_LINES,
        "LONG_STEP": 200,
        "LAT_STEP": 50,
        "ATTR_CROSS_SECTION": "sec_id",
        "OUTPUT": QgsProcessingUtils.generateTempFilename("interpolate_points.shp"),
    }

    def compare_output(self, key, output, expected):
        output = QgsVectorLayer(output, "output", "ogr")
        assert output.isValid()

        output_path = os.path.join(TEMP_PATH, "interpolate_points.gml")
        output = utils.save_as_gml(output, output_path)
        self.compare_layers(output_path, expected)

    def test_algorithm(self):
        self.check_algorithm(
            {
                "OUTPUT": QgsProcessingUtils.generateTempFilename(
                    "interpolate_points.shp"
                ),
            },
            {
                "OUTPUT": "interpolate_points.gml",
            },
        )
