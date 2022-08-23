from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import *
from qgis.utils import iface

mapp = QgsMapCanvas()
mapp2 = iface.mapCanvas()
mapp.setCanvasColor(Qt.white)
mapp.enableAntiAliasing(True)


root = QgsProject.instance().layerTreeRoot()
bridge = QgsLayerTreeMapCanvasBridge(root, mapp)
mapp.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:2154'))
    
#layers = QgsProject.instance().mapLayers().values()

def Zoom_ext():
    layers = QgsProject.instance().mapLayers().values()
    for l in layers:
        if 'DET RENUM' in l.name():
            box = l.boundingBoxOfSelected()
    mapp.zoomToFeatureExtent(box)
    mapp.show()

def PROF_Map():
    layers = QgsProject.instance().mapLayers().values()
    for l in layers:
        if 'Distances' in l.name():
            l_map = l.extent()
    mapp.zoomToFeatureExtent(l_map)
    mapp.show()

def PROF_Map2():
    layers = QgsProject.instance().mapLayers().values()
    for l in layers:
        if 'PROFILE DET' in l.name():
            l_pr = l.extent()
    mapp2.setExtent(l_pr)
    
def Map_PROF():
    layers = QgsProject.instance().mapLayers().values()
    for l in layers:
        if 'PROFILE DET' in l.name():
            l_map = l.extent()
    mapp.zoomToFeatureExtent(l_map)
    mapp.show()

def Map2_PROF():
    layers = QgsProject.instance().mapLayers().values()
    selectedcrs="EPSG:2154"
    target_crs = QgsCoordinateReferenceSystem()
    target_crs.createFromUserInput(selectedcrs)
    for l in layers:
        if 'Distances' in l.name():
            l_pr = l.extent()
    mapp2.setDestinationCrs(target_crs)
    mapp2.setExtent(l_pr)