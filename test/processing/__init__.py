from unittest import TestCase as TestCaseBase

from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsApplication
from processing import Processing

from PreCourlis.processing.precourlis_provider import PreCourlisProvider

QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
Processing.initialize()


class TestCase(TestCaseBase):
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()
        cls.precourlis_provider = PreCourlisProvider()
        assert QgsApplication.processingRegistry().addProvider(cls.precourlis_provider)

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls).tearDownClass()
        QgsApplication.processingRegistry().removeProvider(cls.precourlis_provider)
