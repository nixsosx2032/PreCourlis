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
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu

from processing import execAlgorithmDialog

from PreCourlis.core import Reach
from PreCourlis.processing.precourlis_provider import PreCourlisProvider

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
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "PreCourlisPlugin_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.provider = None
        self.actions = []
        self.menu = self.tr(u"&PreCourlis")

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

        self.action = QAction(
            QIcon(":/plugins/PreCourlis/icon.png"),
            "PreCourlis",
            self.iface.mainWindow(),
        )

        # self.actionBief = QAction("&Bief", self.iface.mainWindow())
        self.actionGeoRef = QAction(
            "Importer un fichier .georef", self.iface.mainWindow()
        )
        self.actionVisuProfils = QAction(
            "Visualiser les profils", self.iface.mainWindow()
        )
        self.actionInterpProfils = QAction(
            "Interpoler des profils", self.iface.mainWindow()
        )
        self.actionConverTrace = QAction(
            "Convertir les traces en profils", self.iface.mainWindow()
        )
        self.actionProjZ = QAction(
            "Projeter un semis de point sur les profils", self.iface.mainWindow()
        )
        self.actionProjRive = QAction("Projeter les berges", self.iface.mainWindow())
        self.actionAbout = QAction(
            QIcon(":/plugins/precourlis/icon.png"), "A propos", self.iface.mainWindow()
        )

        self.actionAddBief = QAction("Ajouter un bief", self.iface.mainWindow())
        self.actionRenaBief = QAction("Renommer un bief", self.iface.mainWindow())
        self.actionDelBief = QAction("Supprimmer un bief", self.iface.mainWindow())
        self.actionAddLayer = QAction(
            "Ajouter une couche vectorielle", self.iface.mainWindow()
        )

        self.menuBief = QMenu(self.iface.mainWindow())
        self.menuBief.setTitle("&Biefs")

        self.menuBief.addAction(self.actionAddBief)
        self.menuBief.addAction(self.actionRenaBief)
        self.menuBief.addAction(self.actionDelBief)
        self.menuBief.addAction(self.actionAddLayer)

        self.menuToolBar = QMenu(self.iface.mainWindow())
        self.menuToolBar.addAction(self.actionGeoRef)
        self.menuToolBar.addAction(self.actionVisuProfils)
        self.menuToolBar.addAction(self.actionConverTrace)
        self.menuToolBar.addAction(self.actionProjZ)
        self.menuToolBar.addAction(self.actionProjRive)
        self.menuToolBar.addAction(self.actionInterpProfils)
        self.menuToolBar.addAction(self.actionAbout)

        self.action.setMenu(self.menuToolBar)

        self.iface.addToolBarIcon(self.action)

        # self.iface.addPluginToMenu("&PreCourlis", self.actionBief)
        self.iface.addPluginToMenu("&PreCourlis", self.actionGeoRef)
        self.iface.addPluginToMenu("&PreCourlis", self.actionVisuProfils)
        self.iface.addPluginToMenu("&PreCourlis", self.actionConverTrace)
        self.iface.addPluginToMenu("&PreCourlis", self.actionProjZ)
        self.iface.addPluginToMenu("&PreCourlis", self.actionProjRive)
        self.iface.addPluginToMenu("&PreCourlis", self.actionInterpProfils)
        self.iface.addPluginToMenu("&PreCourlis", self.actionAbout)

        """
        self.actionAddBief.triggered.connect(self.ajoutBief)
        self.actionAddLayer.triggered.connect(self.ajoutLayer)
        """
        self.actionGeoRef.triggered.connect(self.import_georef)
        self.actionConverTrace.triggered.connect(self.import_tracks)
        """
        self.actionVisuProfils.triggered.connect(self.openEditor)
        self.actionProjZ.triggered.connect(self.projZProfil)
        self.actionProjRive.triggered.connect(self.projAxeBerge)
        self.actionInterpProfils.triggered.connect(self.interpProfils)
        """

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        QgsApplication.processingRegistry().removeProvider(self.provider)

        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u"&PreCourlis"), action)
            self.iface.removeToolBarIcon(action)

        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&PreCourlis", self.action)
        self.iface.removePluginMenu("&PreCourlis", self.actionGeoRef)
        self.iface.removePluginMenu("&PreCourlis", self.actionVisuProfils)
        self.iface.removePluginMenu("&PreCourlis", self.actionInterpProfils)
        self.iface.removePluginMenu("&PreCourlis", self.actionConverTrace)
        self.iface.removePluginMenu("&PreCourlis", self.actionProjZ)
        self.iface.removePluginMenu("&PreCourlis", self.actionProjRive)
        self.iface.removePluginMenu("&PreCourlis", self.actionAbout)

        self.iface.removeToolBarIcon(self.action)

    def import_georef(self):
        execAlgorithmDialog(
            "precourlis:import_georef", {"CRS": QgsProject.instance().crs().authid()}
        )

    def import_tracks(self):
        execAlgorithmDialog("precourlis:import_tracks", {})

    def convertirTrace(self):
        from qgis.core import (
            QgsVectorLayer,
            QgsRasterLayer,
            QgsProject,
            QgsCoordinateReferenceSystem,
        )
        from PreCourlis.core.reach_from_tracks import reach_from_tracks

        data_path = "/home/amorvan/dev/edf_precourlis/PreCourlis/test/data"
        crs = QgsCoordinateReferenceSystem.fromEpsgId(27563)

        tracks = QgsVectorLayer(
            os.path.join(data_path, "cas1", "tracesBief1.shp"), "tracks", "ogr"
        )
        tracks.setCrs(crs)
        assert tracks.isValid()

        dem = QgsRasterLayer(
            os.path.join(data_path, "cas1", "cas2Mnt.asc"), "dem", "gdal"
        )
        dem.setCrs(crs)
        assert dem.isValid()

        axis = QgsVectorLayer(
            os.path.join(data_path, "cas1", "axeHydroBief1.shp"), "axis", "ogr"
        )
        axis.setCrs(crs)
        assert axis.isValid()

        reach = reach_from_tracks(
            name="test",
            tracks=tracks,
            dem=dem,
            axis=axis,
            name_field=None,
            step=100,
            first_pos=0,
        )

        assert isinstance(reach, Reach)

        QgsProject.instance().addMapLayer(reach.to_point_layer())
        QgsProject.instance().addMapLayer(reach.to_line_layer())
