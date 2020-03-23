import pytest

# import qgis libs so that ve set the correct sip api version
import qgis   # pylint: disable=W0611  # NOQA

from qgis.testing import start_app
from qgis.testing.mocked import get_iface
from qgis import utils

utils.iface = get_iface()

@pytest.fixture
def qgis_app():
    QGIS_APP = start_app()
    yield QGIS_APP
