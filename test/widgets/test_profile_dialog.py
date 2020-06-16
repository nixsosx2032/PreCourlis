import unittest

from PreCourlis.widgets.profile_dialog import ProfileDialog


class TestProfileDialog(unittest.TestCase):
    """Test dialog works."""

    def create_dialog(self):
        return ProfileDialog(None)

    def test_init(self):
        """Test we can click OK."""
        self.dialog = self.create_dialog()
