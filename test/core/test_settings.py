import unittest


class TestSettings(unittest.TestCase):
    def test_default_elevation(self):
        from PreCourlis.core.settings import settings
        print(type(settings.default_elevation), type(1.0))
        settings.default_elevation = 1.0
        assert settings.default_elevation == 1.0

        del settings.default_elevation
        assert settings.default_elevation == -999999.0
