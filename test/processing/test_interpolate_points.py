import os

from qgis.core import (
    QgsProcessingUtils,
    QgsProject,
    QgsVectorFileWriter,
    QgsVectorLayer,
)

import processing

from .. import DATA_PATH, EXPECTED_PATH, TEMP_PATH
from . import TestCase, OVERWRITE_EXPECTED

SECTIONS_PATH = os.path.join(DATA_PATH, "input", "profiles_points.shp")
AXIS_PATH = os.path.join(DATA_PATH, "input", "axeHydroBief1.shp")


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

        transform_context = QgsProject.instance().transformContext()
        save_options = QgsVectorFileWriter.SaveVectorOptions()
        save_options.driverName = QgsVectorFileWriter.driverForExtension("gml")
        save_options.fileEncoding = "UTF-8"
        QgsVectorFileWriter.writeAsVectorFormatV2(
            output, output_path, transform_context, save_options,
        )

        output = QgsVectorLayer(output_path, "output", "ogr")
        assert output.isValid()

        expected = QgsVectorLayer(expected_path, "expected", "ogr")
        assert expected.isValid()
        self.assertLayersEqual(output, expected)
