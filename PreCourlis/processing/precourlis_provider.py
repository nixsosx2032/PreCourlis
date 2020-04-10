from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from PreCourlis.processing.import_georef_algorithm import ImportGeorefAlgorithm
from PreCourlis.processing.import_tracks_algorithm import ImportTracksAlgorithm
from PreCourlis.processing.points_to_lines_algorithm import PointsToLinesAlgorithm
from PreCourlis.processing.prepare_tracks_algorithm import PrepareTracksAlgorithm


class PreCourlisProvider(QgsProcessingProvider):
    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(ImportGeorefAlgorithm())
        self.addAlgorithm(ImportTracksAlgorithm())
        self.addAlgorithm(PointsToLinesAlgorithm())
        self.addAlgorithm(PrepareTracksAlgorithm())

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return "precourlis"

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr("PreCourlis")

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QIcon(":/plugins/PreCourlis/icon.png")

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
