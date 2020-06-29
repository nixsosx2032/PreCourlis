import os

# import qgis libs so that ve set the correct sip api version
import qgis  # pylint: disable=W0611  # NOQA

from qgis.testing import start_app

QGIS_APP = start_app()

DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
EXPECTED_PATH = os.path.join(os.path.dirname(__file__), "data", "expected")
TEMP_PATH = "/tmp"

OVERWRITE_EXPECTED = os.environ.get("OVERWRITE_EXPECTED", False)
