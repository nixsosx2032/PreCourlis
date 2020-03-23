from qgis.core import QgsProviderRegistry


class TestQGIS():
    """Test the QGIS Environment"""

    def test_qgis_environment(self):
        """QGIS environment has the expected providers"""

        r = QgsProviderRegistry.instance()
        assert 'gdal' in r.providerList()
        assert 'ogr' in r.providerList()
        # self.assertIn('postgres', r.providerList())
