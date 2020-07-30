import os

from qgis.core import QgsVectorLayer

import processing

from .. import DATA_PATH, EXPECTED_PATH, TEMP_PATH, OVERWRITE_EXPECTED
from . import TestCase

AXIS_PATH = os.path.join(DATA_PATH, "input", "axeHydroBief1.shp")
TRACKS_PATH = os.path.join(DATA_PATH, "input", "tracesBief1.shp")
DEM_PATH = os.path.join(DATA_PATH, "input", "cas2Mnt.asc")


class TestImportTracksAlgorithm(TestCase):
    def test_algorithm(self):
        output_path = os.path.join(TEMP_PATH, "import_tracks.gml")
        expected_path = os.path.join(EXPECTED_PATH, "import_tracks.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:import_tracks",
            {
                "TRACKS": TRACKS_PATH,
                "AXIS": AXIS_PATH,
                "FIRST_SECTION_ABS_LONG": 0.0,
                "NAME_FIELD": "nom_profil",
                "DISTANCE": 100.0,
                "DEM": DEM_PATH,
                "OUTPUT": output_path,
            },
        )
        output = QgsVectorLayer(outputs["OUTPUT"], "output", "ogr")
        assert output.isValid()

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()
        self.assertLayersEqual(output, expected)

    def test_strict_distance(self):
        output_path = os.path.join(TEMP_PATH, "import_tracks_strict_distance.gml")
        expected_path = os.path.join(EXPECTED_PATH, "import_tracks_strict_distance.gml")

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:import_tracks",
            {
                "TRACKS": TRACKS_PATH,
                "AXIS": AXIS_PATH,
                "FIRST_SECTION_ABS_LONG": 0.0,
                "NAME_FIELD": "nom_profil",
                "DISTANCE": 100.0,
                "STRICT_DISTANCE": True,
                "DEM": DEM_PATH,
                "OUTPUT": output_path,
            },
        )
        output = QgsVectorLayer(outputs["OUTPUT"], "output", "ogr")
        assert output.isValid()

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()

        self.assertLayersEqual(expected, output)

    def test_first_axis_point_abs_long(self):
        output_path = os.path.join(
            TEMP_PATH, "import_tracks_first_axis_point_abs_long.gml"
        )
        expected_path = os.path.join(
            EXPECTED_PATH, "import_tracks_first_axis_point_abs_long.gml"
        )

        if OVERWRITE_EXPECTED:
            output_path = expected_path

        outputs = processing.run(
            "precourlis:import_tracks",
            {
                "TRACKS": TRACKS_PATH,
                "AXIS": AXIS_PATH,
                "FIRST_AXIS_POINT_ABS_LONG": 0.0,
                "NAME_FIELD": "nom_profil",
                "DISTANCE": 100.0,
                "STRICT_DISTANCE": True,
                "DEM": DEM_PATH,
                "OUTPUT": output_path,
            },
        )
        output = QgsVectorLayer(outputs["OUTPUT"], "output", "ogr")
        assert output.isValid()

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()

        self.assertLayersEqual(expected, output)
