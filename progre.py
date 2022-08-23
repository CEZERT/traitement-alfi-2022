import os
import os
import processing
import qgis
from qgis.PyQt import *
from qgis.PyQt.QtWidgets import QProgressBar
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.core import QgsProcessingAlgorithm, QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import (
  QgsProcessingContext,
  QgsTaskManager,
  QgsTask,
  QgsProcessingAlgRunnerTask,
  Qgis,
  QgsProcessingFeedback,
  QgsApplication,
  QgsMessageLog,
)
from qgis.utils import iface

def Prog_global(f):
    progressbar = QProgressBar()
    qgis.utils.iface.messageBar().clearWidgets()
    progressMessageBar = qgis.utils.iface.messageBar()
    progressMessageBar.pushWidget(progressbar)

    

    # Processing feedback
    def progress_changed(progress):
        progressbar.setValue(progress)
        return progress




    f.progressChanged.connect(progress_changed)


    # Clear the message bar when done
    #qgis.utils.iface.messageBar().clearWidgets()
