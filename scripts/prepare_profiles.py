#!/usr/bin/python3

import os
import sys
from shutil import copyfile

from qgis.core import QgsApplication, QgsVectorLayer
import processing
from processing import Processing

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from PreCourlis.core.precourlis_file import PreCourlisFileLine
from PreCourlis.processing.precourlis_provider import PreCourlisProvider
from test import processing as processing_test  # noqa
from test import DATA_PATH

precourlis_provider = PreCourlisProvider()
QgsApplication.processingRegistry().addProvider(precourlis_provider)
Processing.initialize()

GEOREF_PATH = os.path.join(DATA_PATH, "input", "test.georef")

AXIS_PATH = os.path.join(DATA_PATH, "input", "axeHydroBief1.shp")
TRACKS_PATH = os.path.join(DATA_PATH, "input", "tracesBief1.shp")
DEM_PATH = os.path.join(DATA_PATH, "input", "cas2Mnt.asc")

PROFILE_LINES_PATH = os.path.join(DATA_PATH, "input", "profiles_lines.geojson")
PROFILE_POINTS_PATH = os.path.join(DATA_PATH, "input", "profiles_points.gml")

EXAMPLES_FOLDER = os.environ.get("EXAMPLES_FOLDER", None)
if EXAMPLES_FOLDER is None:
    print("Set value of EXAMPLES_FOLDER environment variable and restart")
    exit(1)

copyfile(os.path.join(EXAMPLES_FOLDER, "cas0/test_fic_geo2d_masc_with_name.georef"), GEOREF_PATH)

processing.run(
    "qgis:assignprojection", {
        'INPUT': os.path.join(EXAMPLES_FOLDER, "cas1/tracesBief1.shp"),
        'CRS': 'EPSG:27563',
        "OUTPUT": TRACKS_PATH,
    }
)

processing.run(
    "qgis:assignprojection", {
        'INPUT': os.path.join(EXAMPLES_FOLDER, "cas1/axeHydroBief1.shp"),
        'CRS': 'EPSG:27563',
        "OUTPUT": AXIS_PATH,
    }
)

processing.run(
    "qgis:assignprojection", {
        'INPUT': os.path.join(EXAMPLES_FOLDER, "cas1/riveDroiteBief1.shp"),
        'CRS': 'EPSG:27563',
        "OUTPUT": os.path.join(DATA_PATH, "input", "riveDroiteBief1.shp"),
    }
)

processing.run(
    "qgis:assignprojection", {
        'INPUT': os.path.join(EXAMPLES_FOLDER, "cas1/riveGaucheBief1.shp"),
        'CRS': 'EPSG:27563',
        "OUTPUT": os.path.join(DATA_PATH, "input", "riveGaucheBief1.shp"),
    }
)

copyfile(os.path.join(EXAMPLES_FOLDER, "cas1/cas2Mnt.asc"), DEM_PATH)

processing.run(
    "precourlis:import_tracks",
    {
        "TRACKS": TRACKS_PATH,
        "AXIS": AXIS_PATH,
        "FIRST_POS": 0.0,
        "NAME_FIELD": "nom_profil",
        "DISTANCE": 100.0,
        "DEM": DEM_PATH,
        "OUTPUT": PROFILE_LINES_PATH,
    },
)
layer = QgsVectorLayer(PROFILE_LINES_PATH, "profile_lines", "ogr")
assert layer.isValid()

copyfile(PROFILE_LINES_PATH, os.path.join(DATA_PATH, "input", "profiles_lines_zero_layers.geojson"))

layer.startEditing()
PreCourlisFileLine(layer).add_sedimental_layer("Layer1", "zfond", -1)
layer.commitChanges()

processing.run(
    "precourlis:lines_to_points",
    {
        "INPUT": PROFILE_LINES_PATH,
        "OUTPUT": PROFILE_POINTS_PATH,
    },
)
