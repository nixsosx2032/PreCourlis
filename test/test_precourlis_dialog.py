# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'matthieu.secher@edf.fr'
__date__ = '2020-03-13'
__copyright__ = 'Copyright 2020, EDF Hydro, DeltaCAD, Camptocamp'

import unittest

from PyQt5.QtWidgets import QDialogButtonBox, QDialog

from PreCourlis.widgets.PreCourlis_dialog import PreCourlisPluginDialog


class TestPreCourlisPluginDialog():
    """Test dialog works."""

    def create_dialog(self):
        return PreCourlisPluginDialog(None)

    def test_dialog_ok(self):
        """Test we can click OK."""
        self.dialog = self.create_dialog()
        button = self.dialog.button_box.button(QDialogButtonBox.Ok)
        button.click()
        result = self.dialog.result()
        assert result == QDialog.Accepted

    def test_dialog_cancel(self):
        """Test we can click cancel."""
        self.dialog = self.create_dialog()
        button = self.dialog.button_box.button(QDialogButtonBox.Cancel)
        button.click()
        result = self.dialog.result()
        assert result == QDialog.Rejected
