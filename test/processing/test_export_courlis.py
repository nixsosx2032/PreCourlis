from .. import PROFILE_LINES_PATH
from . import TestCase


class TestExportGeorefAlgorithm(TestCase):

    ALGORITHM_ID = "precourlis:export_courlis"
    DEFAULT_PARAMS = {"INPUT": PROFILE_LINES_PATH}

    def compare_output(self, key, output, expected):
        self.compare_files(output, expected)

    def test_export_georefc(self):
        self.check_algorithm({}, {"OUTPUT": "export_georef.georefC"})

    def test_export_geoc(self):
        self.check_algorithm({}, {"OUTPUT": "export_georef.geoC"})
