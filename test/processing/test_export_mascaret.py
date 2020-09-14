import os
import filecmp

from .. import PROFILE_LINES_PATH
from . import TestCase


class TestExportGeorefAlgorithm(TestCase):

    ALGORITHM_ID = "precourlis:export_mascaret"
    DEFAULT_PARAMS = {"INPUT": PROFILE_LINES_PATH}

    def compare_output(self, key, output, expected):
        assert os.path.isfile(output)
        assert filecmp.cmp(expected, output)

    def test_export_georef(self):
        self.check_algorithm({}, {"OUTPUT": "export_georef.georef"})

    def test_export_geo(self):
        self.check_algorithm({}, {"OUTPUT": "export_georef.geo"})
