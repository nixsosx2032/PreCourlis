from .. import PROFILE_LINES_PATH
from . import TestCase


class TestLinesToPointsAlgorithm(TestCase):

    ALGORITHM_ID = "precourlis:lines_to_points"
    DEFAULT_PARAMS = {
        "INPUT": PROFILE_LINES_PATH,
    }

    def test_algorithm(self):
        self.check_algorithm({}, {"OUTPUT": "lines_to_points.gml"})
