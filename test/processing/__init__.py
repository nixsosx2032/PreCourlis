from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsApplication
from qgis.testing import TestCase  # noqa
from processing import Processing

from PreCourlis.processing.precourlis_provider import PreCourlisProvider

QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
Processing.initialize()
provider = PreCourlisProvider()
QgsApplication.processingRegistry().addProvider(provider)
