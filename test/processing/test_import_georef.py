import os

from qgis.core import QgsVectorLayer

import processing

from .. import DATA_PATH, EXPECTED_PATH, TEMP_PATH, OVERWRITE_EXPECTED
from . import TestCase

GEOREF_PATH = os.path.join(DATA_PATH, "input", "test.georef")


class TestImportGeorefAlgorithm(TestCase):
    def test_algorithm(self):
        output_path = os.path.join(TEMP_PATH, "import_georef.gml")
        expected_path = os.path.join(EXPECTED_PATH, "import_georef.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:import_georef",
            {"INPUT": GEOREF_PATH, "CRS": "EPSG:2154", "OUTPUT": output_path},
        )
        output = QgsVectorLayer(outputs["OUTPUT"], "output", "ogr")
        assert output.isValid()

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()

        self.assertLayersEqual(expected, output)
