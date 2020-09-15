# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PreCourlisPlugin
                                 A QGIS plugin
 Creation de profils pour Courlis
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-03-13
        git sha              : $Format:%H$
        copyright            : (C) 2020 by EDF Hydro, DeltaCAD, Camptocamp
        email                : matthieu.secher@edf.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os.path

from qgis.core import QgsApplication, QgsProject
from qgis.PyQt.QtCore import (
    Qt,
    QLocale,
    QSettings,
    QTranslator,
    qVersion,
    QCoreApplication,
)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu

from processing import execAlgorithmDialog

from PreCourlis.processing.precourlis_provider import PreCourlisProvider
from PreCourlis.widgets.profile_dialog import ProfileDialog

# Initialize Qt resources from file resources.py
from PreCourlis.ui import resources_rc  # noqa


class PreCourlisPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale", QLocale().name())[0:2]
        locale_path = os.path.join(self.plugin_dir, "i18n", "{}.qm".format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.action = None
        self.actions = []
        self.menu = self.tr(u"&PreCourlis")
        self.profile_dialog = None
        self.provider = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("PreCourlisPlugin", message)

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = PreCourlisProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.initProcessing()

        self.menuToolBar = QMenu(self.iface.mainWindow())
        self.add_action("Importer un fichier .georef", self.import_georef)
        self.add_action("Visualiser les profils", self.open_editor)
        self.add_action("Convertir les traces en profils", self.import_tracks)
        # self.add_action("Projeter un semis de point sur les profils", self.projZProfil)
        # self.add_action("Projeter les berges", self.projAxeBerge)
        self.add_action("Interpoler des profils", self.interpolate_profiles)
        # self.add_action("A propos", slot, QIcon(":/plugins/precourlis/icon.png"))
        self.add_action("Exporter un fichier de géométrie Courlis", self.export_courlis)
        self.add_action(
            "Exporter un fichier de géométrie Mascaret", self.export_mascaret
        )

        """
        self.actionBief = QAction("&Bief", self.iface.mainWindow())
        self.actionAddBief = QAction("Ajouter un bief", self.iface.mainWindow())
        self.actionRenaBief = QAction("Renommer un bief", self.iface.mainWindow())
        self.actionDelBief = QAction("Supprimmer un bief", self.iface.mainWindow())
        self.actionAddLayer = QAction(
            "Ajouter une couche vectorielle", self.iface.mainWindow()
        )

        self.actionAddBief.triggered.connect(self.ajoutBief)
        self.actionAddLayer.triggered.connect(self.ajoutLayer)

        self.menuBief = QMenu(self.iface.mainWindow())
        self.menuBief.setTitle("&Biefs")
        self.menuBief.addAction(self.actionAddBief)
        self.menuBief.addAction(self.actionRenaBief)
        self.menuBief.addAction(self.actionDelBief)
        self.menuBief.addAction(self.actionAddLayer)
        """

        # Add toolbar icon
        self.action = QAction(
            QIcon(":/plugins/PreCourlis/icon.png"),
            "PreCourlis",
            self.iface.mainWindow(),
        )
        self.action.setMenu(self.menuToolBar)
        self.iface.addToolBarIcon(self.action)

    def add_action(self, text, slot, icon=None):
        action = QAction(self.iface.mainWindow())
        action.setText(text)
        if icon is not None:
            action.setIcon(icon)
        action.triggered.connect(slot)
        self.menuToolBar.addAction(action)
        self.iface.addPluginToMenu("&PreCourlis", action)
        self.actions.append(action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        QgsApplication.processingRegistry().removeProvider(self.provider)

        # Remove the plugin menu item and icon
        for action in self.actions:
            self.iface.removePluginMenu("&PreCourlis", action)
            self.iface.removeToolBarIcon(action)

        self.iface.removePluginMenu("&PreCourlis", self.action)
        self.iface.removeToolBarIcon(self.action)

        if self.profile_dialog is not None:
            self.profile_dialog.deleteLater()

    def import_georef(self):
        execAlgorithmDialog(
            "precourlis:import_georef", {"CRS": QgsProject.instance().crs().authid()}
        )

    def import_tracks(self):
        execAlgorithmDialog("precourlis:import_tracks", {})

    def open_editor(self):
        if self.profile_dialog is None:
            self.profile_dialog = ProfileDialog(self.iface.mainWindow())
            self.profile_dialog.setAttribute(Qt.WA_DeleteOnClose)
            self.profile_dialog.destroyed.connect(self.profile_dialog_destroyed)
        self.profile_dialog.show()

    def profile_dialog_destroyed(self):
        self.profile_dialog.graphWidget.close_figure()
        self.profile_dialog = None

    def interpolate_profiles(self):
        execAlgorithmDialog("precourlis:interpolate_lines", {})

    def export_courlis(self):
        execAlgorithmDialog("precourlis:export_courlis")

    def export_mascaret(self):
        execAlgorithmDialog("precourlis:export_mascaret")
