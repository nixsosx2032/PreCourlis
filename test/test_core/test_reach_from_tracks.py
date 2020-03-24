import logging
import os
import unittest

from qgis.core import QgsRasterLayer, QgsVectorLayer
from processing import Processing

from PreCourlis.core.reach_from_tracks import (
    line_layer_from_tracks,
    reach_from_tracks,
)

from .. import DATA_PATH
from ..utils import cached_property  # functools.cached_property in Python 3.8

LOG = logging.getLogger(__name__)

AXIS_PATH = os.path.join(DATA_PATH, "cas1", "axeHydroBief1.shp")
TRACKS_PATH = os.path.join(DATA_PATH, "cas1", "tracesBief1.shp")
DEM_PATH = os.path.join(DATA_PATH, "cas1", "cas2Mnt.asc")


class TestReachFromTracks(unittest.TestCase):
    @cached_property()
    def axis(self):
        assert os.path.exists(AXIS_PATH)
        layer = QgsVectorLayer(AXIS_PATH, "axis", "ogr")
        assert layer.isValid()
        return layer

    @cached_property()
    def tracks(self):
        assert os.path.exists(TRACKS_PATH)
        layer = QgsVectorLayer(TRACKS_PATH, "tracks", "ogr")
        assert layer.isValid()
        return layer

    @cached_property()
    def dem(self):
        assert os.path.exists(DEM_PATH)
        layer = QgsRasterLayer(DEM_PATH, "dem", "gdal")
        assert layer.isValid()
        return layer

    def test_line_layer_from_tracks(self):
        line_layer = line_layer_from_tracks(
            name="test",
            tracks=self.tracks,
            axis=self.axis,
            name_field="nom_profil",
            first_pos=0.0,
        )
        assert line_layer.featureCount() == self.tracks.featureCount()

    def test_reach_from_tracks(self):
        Processing.initialize()
        reach_from_tracks(
            name="test",
            axis=self.axis,
            tracks=self.tracks,
            name_field=None,
            first_pos=0.0,
            step=100.0,
            dem=self.dem,
        )
