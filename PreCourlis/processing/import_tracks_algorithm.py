from qgis.core import (
    QgsApplication,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterField,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterVectorDestination,
)
from qgis.PyQt.QtCore import QCoreApplication
import processing


class ImportTracksAlgorithm(QgsProcessingAlgorithm):

    TRACKS = "TRACKS"
    AXIS = "AXIS"
    FIRST_POS = "FIRST_POS"
    NAME_FIELD = "NAME_FIELD"
    DISTANCE = "DISTANCE"
    DEM = "DEM"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.TRACKS,
                self.tr("Tracks"),
                types=[QgsProcessing.TypeVectorLine],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.AXIS,
                self.tr("Axis"),
                types=[QgsProcessing.TypeVectorLine],
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.FIRST_POS,
                self.tr("Position of first section"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.NAME_FIELD,
                self.tr("Name field"),
                optional=True,
                type=QgsProcessingParameterField.String,
                parentLayerParameterName=self.TRACKS,
                allowMultiple=False,
                defaultValue=None,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DISTANCE,
                self.tr("Maximum distance between two points"),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=100,
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.DEM, self.tr("Digital Elevation Model"), defaultValue=None
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr("Reach"),
                type=QgsProcessing.TypeVectorAnyGeometry,
                createByDefault=True,
                defaultValue=None,
            )
        )

    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(9, model_feedback)
        results = {}
        outputs = {}

        tracks = self.parameterAsSource(parameters, self.TRACKS, context)

        # Import tracks
        alg_params = {
            "TRACKS": parameters[self.TRACKS],
            "AXIS": parameters[self.AXIS],
            "FIRST_POS": parameters[self.FIRST_POS],
            "NAME_FIELD": parameters[self.NAME_FIELD],
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["PrepareTracks"] = processing.run(
            "precourlis:prepare_tracks",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["PrepareTracks"]["OUTPUT"]

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # addautoincrementalfield
        alg_params = {
            "INPUT": current,
            "FIELD_NAME": "sec_index",
            "START": 1,
            "GROUP_FIELDS": [],
            "SORT_EXPRESSION": '"sec_pos"',
            "SORT_ASCENDING": True,
            "SORT_NULLS_FIRST": False,
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["AddAutoincrementalField"] = processing.run(
            "native:addautoincrementalfield",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["AddAutoincrementalField"]["OUTPUT"]

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # fieldcalculator
        alg_params = {
            "INPUT": current,
            "FIELD_NAME": "sec_id",
            "FIELD_TYPE": 0,
            "FIELD_LENGTH": 10,
            "FIELD_PRECISION": 3,
            "NEW_FIELD": False,
            "FORMULA": ' "sec_index" ',
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["FieldCalculator"] = processing.run(
            "qgis:fieldcalculator",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["FieldCalculator"]["OUTPUT"]

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # v.to.points
        v_to_points = QgsApplication.processingRegistry().createAlgorithmById(
            "grass7:v.to.points"
        )
        alg_params = {
            "-i": True,
            "-t": False,
            "dmax": parameters[self.DISTANCE],
            "input": current,
            "type": [1],
            "use": 1,
            "output": v_to_points.parameterDefinition(
                "output"
            ).generateTemporaryDestination(),
        }
        outputs["Vtopoints"] = processing.run(
            "grass7:v.to.points",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["Vtopoints"]["output"]

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # AddZField
        alg_params = {
            "INPUT": current,
            "FIELD_NAME": "z",
            "FIELD_TYPE": 1,
            "FIELD_LENGTH": 10,
            "FIELD_PRECISION": 2,
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["AddZField"] = processing.run(
            "qgis:addfieldtoattributestable",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["AddZField"]["OUTPUT"]

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # v.what.rast
        v_what_raster = QgsApplication.processingRegistry().createAlgorithmById(
            "grass7:v.what.rast"
        )
        alg_params = {
            "-i": False,
            "column": "z",
            "map": current,
            "raster": parameters[self.DEM],
            "type": 0,
            "where": "",
            "output": v_what_raster.parameterDefinition(
                "output"
            ).generateTemporaryDestination(),
        }
        outputs["Vwhatrast"] = processing.run(
            "grass7:v.what.rast",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["Vwhatrast"]["output"]

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # fieldcalculator
        alg_params = {
            "INPUT": current,
            "FIELD_NAME": "p_z",
            "FIELD_TYPE": 0,
            "FIELD_LENGTH": 10,
            "FIELD_PRECISION": 3,
            "NEW_FIELD": False,
            "FORMULA": ' "z" ',
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["FieldCalculator"] = processing.run(
            "qgis:fieldcalculator",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["FieldCalculator"]["OUTPUT"]

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # assignprojection
        alg_params = {
            "INPUT": current,
            "CRS": tracks.sourceCrs(),
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        }
        outputs["AssignProjection"] = processing.run(
            "native:assignprojection",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["AssignProjection"]["OUTPUT"]

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # point_to_lines
        alg_params = {
            "INPUT": current,
            "OUTPUT": parameters[self.OUTPUT],
        }
        outputs["PointsToLines"] = processing.run(
            "precourlis:points_to_lines",
            alg_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        current = outputs["PointsToLines"]["OUTPUT"]

        results["OUTPUT"] = current
        return results

    def name(self):
        return "import_tracks"

    def displayName(self):
        return self.tr("Import tracks")

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return "Import"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ImportTracksAlgorithm()
