import os
import filecmp

import processing

from .. import DATA_PATH, EXPECTED_PATH, TEMP_PATH, OVERWRITE_EXPECTED
from . import TestCase

INPUT_PATH = os.path.join(DATA_PATH, "input", "profiles_lines.shp")


class TestExportGeorefAlgorithm(TestCase):
    def _test_export(self, ext):
        output_path = os.path.join(TEMP_PATH, "export_georef.{}".format(ext))
        expected_path = os.path.join(EXPECTED_PATH, "export_georef.{}".format(ext))

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:export_mascaret", {"INPUT": INPUT_PATH, "OUTPUT": output_path},
        )
        assert os.path.isfile(outputs["OUTPUT"])

        assert filecmp.cmp(expected_path, output_path)

    def test_export_georefc(self):
        self._test_export("georef")

    def test_export_geoc(self):
        self._test_export("geo")
