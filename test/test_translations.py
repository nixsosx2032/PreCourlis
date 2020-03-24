import os

from PyQt5.QtCore import QCoreApplication, QTranslator


class TestSafeTranslations:
    """Test translations work."""

    def setUp(self):
        """Runs before each test."""
        if "LANG" in iter(os.environ.keys()):
            os.environ.__delitem__("LANG")

    def tearDown(self):
        """Runs after each test."""
        if "LANG" in iter(os.environ.keys()):
            os.environ.__delitem__("LANG")

    # @pytest.mark.skip(reason="no way of currently testing this")
    def tes_qgis_translations(self):
        """Test that translations work."""
        parent_path = os.path.join(__file__, os.path.pardir, os.path.pardir)
        dir_path = os.path.abspath(parent_path)
        file_path = os.path.join(dir_path, "i18n", "af.qm")
        translator = QTranslator()
        translator.load(file_path)
        QCoreApplication.installTranslator(translator)

        expected_message = "Goeie more"
        real_message = QCoreApplication.translate("@default", "Good morning")
        self.assertEqual(real_message, expected_message)
