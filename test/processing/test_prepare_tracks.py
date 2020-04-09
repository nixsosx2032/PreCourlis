import os
import unittest

from qgis.core import QgsProcessing
import processing

from PreCourlis.processing.prepare_tracks_algorithm import PrepareTracksAlgorithm

from .. import DATA_PATH

AXIS_PATH = os.path.join(DATA_PATH, "cas1", "axeHydroBief1.shp")
TRACKS_PATH = os.path.join(DATA_PATH, "cas1", "tracesBief1.shp")
DEM_PATH = os.path.join(DATA_PATH, "cas1", "cas2Mnt.asc")


class TestImportTracksAlgorithm(unittest.TestCase):
    def test_algorithm(self):
        alg = PrepareTracksAlgorithm().create()
        outputs = processing.run(
            alg,
            {
                "TRACKS": TRACKS_PATH,
                "AXIS": AXIS_PATH,
                "FIRST_POS": 0.0,
                "NAME_FIELD": "nom_profil",
                "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
            },
        )
        layer = outputs["OUTPUT"]
        assert layer.featureCount() == 6
