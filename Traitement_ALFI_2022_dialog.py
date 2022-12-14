# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Traitement_alfiDialog
                                 A QGIS plugin
 Traitement ALFI 2022
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-07-07
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Marc Yeranosyan
        email                : m.yeranosyan@survey-groupe.fr
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

import os
import qgis
import processing
from qgis.PyQt import *
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget, QApplication, QProgressBar
from qgis.core import QgsProcessingAlgorithm, QgsProject
from qgis.core import QgsVectorLayer
from .profile3 import PROF_Map, PROF_Map2, Map_PROF, Map2_PROF, Zoom_ext
from qgis.utils import iface

from .progre import *

from qgis.core import (
  QgsProcessingContext,
  QgsTaskManager,
  QgsTask,
  QgsProcessingAlgRunnerTask,
  Qgis,
  QgsProcessingFeedback,
  QgsApplication,
  QgsMessageLog)

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Traitement ALFI 2022_dialog_base.ui'))

layers = QgsProject.instance().mapLayers().values()
for l in layers:
    if 'Fusion' in l.name() and 'DET' in l.name():
        l_det = l
    if 'Fusion' in l.name() and 'CTRL' in l.name():
        l_ctrl = l
    if 'Fusion' in l.name() and 'SIG' in l.name():
        l_sig = l

class Traitement_alfiDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Traitement_alfiDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        
        self.preparation.pressed.connect(self.Preparation)
        self.ctrlindiv.pressed.connect(self.CTRLS_INDIV)
        self.ctrldxf.pressed.connect(self.CTRLS_DXF)
        self.renum.pressed.connect(self.RENUM)
        self.export_2.pressed.connect(self.EXPORTT)
        self.prepaffsig.pressed.connect(self.PREPA_SIG)
        self.majprofile.pressed.connect(self.PROFILE)
        self.symbols.pressed.connect(self.styleapp)
        
        
        #profile map view swithing
        self.prof_aff.pressed.connect(self.Prof_Affichage)
        self.prof_aff_normal.pressed.connect(self.Prof_Affichage_normal)
        
        #chargement calques client
        self.centerline_2.pressed.connect(self.Centerline)
        self.install_annexes.pressed.connect(self.Install_Annexes)
        self.markers.pressed.connect(self.Markers)
        self.aerien.pressed.connect(self.Aerien)
        
        #nettoyage
        self.nett_apres_lissage.pressed.connect(self.Nett_Apr_liss)
        self.nett_avant_lissage.pressed.connect(self.Nett_Av_liss)
        
        #Zoom to selected in mapp
        self.zoom.pressed.connect(self.ZoomTo)
        
        
    def Preparation(self):
        f = QgsProcessingFeedback()
        Prog_global(f)
        layers = QgsProject.instance().mapLayers().values()
        for l in layers:
            if 'Fusion' in l.name() and 'DET' in l.name():
                l_det = l
            if 'Fusion' in l.name() and 'CTRL' in l.name():
                l_ctrl = l

        processing.runAndLoadResults("model:01-Preparation", {'FusionCTRL':l_ctrl,
        'FusionDET':l_det,
        'memorypoly':'DET Ligne',
        'native:buffer_1:Buffer 10cm DET':'TEMPORARY_OUTPUT',
        'native:buffer_2:Buffer 10cm CTRL':'TEMPORARY_OUTPUT',
        'native:extractbyattribute_1:VERIF EPOS CTRL':'TEMPORARY_OUTPUT',
        'native:refactorfields_1:Distances et Angles':'TEMPORARY_OUTPUT',
        'qgis:joinattributesbylocation_1:DET':'TEMPORARY_OUTPUT',
        'qgis:refactorfields_4:CTRL':'TEMPORARY_OUTPUT',
        'native:deleteduplicategeometries_2:LOCALISATION ERREURS LIGNE DET':'TEMPORARY_OUTPUT'}, feedback = f)
        
    def CTRLS_INDIV(self):

        f = QgsProcessingFeedback()
        Prog_global(f)
        processing.runAndLoadResults("model:02-Create CTRLS INDIV", {'det2':'DET',
        'qgis:createpointslayerfromtable_4:CTRLs_Cr??es':'TEMPORARY_OUTPUT'}, feedback = f)
        layers = QgsProject.instance().mapLayers().values()
        for l in layers:
            if l.name() == 'DET':
                qgis.utils.iface.setActiveLayer(l)
        
    def CTRLS_DXF(self):
        f = QgsProcessingFeedback()
        Prog_global(f)
        processing.runAndLoadResults("model:02-Create CTRLS_DXF", {'champ':'Text',
        'controletext':'C',
        'ctrlsduterrain':'BALISE-RENF_SURVEY(P)',
        'det':'DET',
        'qgis:createpointslayerfromtable_4:CTRLs_Cr??es':'TEMPORARY_OUTPUT'}, feedback = f)
        
    def RENUM(self):
        f = QgsProcessingFeedback()
        Prog_global(f)
        processing.runAndLoadResults("model:04-Renum", {'CONCERT2dxfCANAENTERRESURVEY':'CANA_ENTERRE_SURVEY(L)',
        'cetligne2':'DET Ligne 2',
        'det':'CTRL',
        'fusiondet':'DET',
        'virtuallayer':'CTRL Ligne 2',
        'native:deleteduplicategeometries_1:LOCALISATION ERREURS LIGNE DET 2':'TEMPORARY_OUTPUT',
        'native:deleteduplicategeometries_2:LOCALISATION ERREURS LIGNE CTRL 2':'TEMPORARY_OUTPUT',
        'native:extractbyattribute_3:VERIF OPERATEURS':'TEMPORARY_OUTPUT',
        'native:refactorfields_3:Qualif_trace_initial':'TEMPORARY_OUTPUT',
        'qgis:refactorfields_1:Fusion DET RENUM':'TEMPORARY_OUTPUT',
        'qgis:refactorfields_4:Fusion CTRL RENUM':'TEMPORARY_OUTPUT',
        'script:0 Profile AL_1:PROFILE DET CANA':'TEMPORARY_OUTPUT',
        'script:0 Profile AL_2:PROFILE DET TN':'TEMPORARY_OUTPUT',
        'script:0 Profile AL_2:PROFILE ETIQUETTES':'TEMPORARY_OUTPUT',
        'script:0 Profile AL_2:PROFILE TABLEAU':'TEMPORARY_OUTPUT'}, feedback = f)

        
    def styleapp(self):
        layers = QgsProject.instance().mapLayers().values()
        for ll in layers:
            if "ETIQUETTES" in ll.name():
                ll.loadNamedStyle('S:/09-Production/CLIENTS/AIR LIQUIDE/21-0178 TOPO 3D ALFI NORD 2021/Travail/Dao/Outils de traitement/Styles/PROFIL_ETIQUETTES.qml')
                ll.triggerRepaint()

    def EXPORTT(self):
        f = QgsProcessingFeedback()
        Prog_global(f)
        processing.runAndLoadResults("model:06-Export", {'CONVERT2dxfAltDetect':'AtlDetect(P)',
        'FusionCTRLModif':'Fusion CTRL RENUM',
        'FusionDETModif':'Fusion DET RENUM',
        'Qualiftraceinitial':'Qualif_trace_initial',
        'native:fieldcalculator_1:Qualif_trace_final':'TEMPORARY_OUTPUT',
        'native:fieldcalculator_13:Fusion_DET_final':'TEMPORARY_OUTPUT',
        'native:fieldcalculator_14:Fusion_CTRL_final':'TEMPORARY_OUTPUT',}, feedback = f)
        
    def PREPA_SIG(self):
    
        layers = QgsProject.instance().mapLayers().values()
        for l in layers:
            if 'Fusion' in l.name() and 'AFF_SIG' in l.name():
                l_aff = l
        f = QgsProcessingFeedback()
        Prog_global(f)
        processing.runAndLoadResults("model:07-Prepa_AFF_SIG", {'Accessoiresannexe13':l_aff,
        'native:refactorfields_2:Fusion_AFF_SIG_prepar??':'TEMPORARY_OUTPUT'}, feedback = f)
    
    def PROFILE(self):
        f = QgsProcessingFeedback()
        Prog_global(f)
        lrs = QgsProject.instance().mapLayers().values()
        for l in lrs:
            if 'DET RENUM' in l.name():
                l.commitChanges()
                l.startEditing()
        processing.runAndLoadResults("model:MAJ Profile 3D", {'DET':'Fusion DET RENUM',
        'script:0 Profile AL_1:PROFILE DET CANA':'TEMPORARY_OUTPUT',
        'script:0 Profile AL_2:PROFILE DET TN':'TEMPORARY_OUTPUT'}, feedback = f)

        
    def Prof_Affichage(self):
        www = PROF_Map()
        PROF_Map2()
        iface.mapCanvas().refresh()
    
    def Prof_Affichage_normal(self):
        www = Map_PROF()
        Map2_PROF()
        iface.mapCanvas().refresh()

    def ZoomTo(self):
        www=Zoom_ext()
        iface.mapCanvas().refresh()

    
    def Centerline(self):
        centerline_l = r"S:\09-Production\CLIENTS\AIR LIQUIDE\21-0178 TOPO 3D ALFI NORD 2021\Travail\Dao\Outils de traitement\SHP_FME\CENTERLINE_AVEC_DN RGF93 pour QualifTrac??.shp"
        vlayer = QgsVectorLayer(centerline_l, "CENTERLINE", "ogr")
        QgsProject.instance().addMapLayer(vlayer)
        vlayer.loadNamedStyle('S:/09-Production/CLIENTS/AIR LIQUIDE/21-0178 TOPO 3D ALFI NORD 2021/Travail/Dao/Outils de traitement/Styles/CENTERLINE.qml')

    def Install_Annexes(self):
        inst_annex_l = r"S:\09-Production\CLIENTS\AIR LIQUIDE\21-0178 TOPO 3D ALFI NORD 2021\Travail\Dao\Outils de traitement\SHP_FME\INSTALLATIONS_ANNEXES.shp"
        vlayer = QgsVectorLayer(inst_annex_l, "INSTALLATION_ANNEXES", "ogr")
        QgsProject.instance().addMapLayer(vlayer)
        vlayer.loadNamedStyle('S:/09-Production/CLIENTS/AIR LIQUIDE/21-0178 TOPO 3D ALFI NORD 2021/Travail/Dao/Outils de traitement/Styles/INSTALL_ANEXES.qml')
        
    def Markers(self):
        mark = r"S:\09-Production\CLIENTS\AIR LIQUIDE\21-0178 TOPO 3D ALFI NORD 2021\Travail\Dao\Outils de traitement\SHP_FME\markers_mars2021_v5_2154.shp"
        vlayer = QgsVectorLayer(mark, "MARKERS", "ogr")
        QgsProject.instance().addMapLayer(vlayer)
        vlayer.loadNamedStyle('S:/09-Production/CLIENTS/AIR LIQUIDE/21-0178 TOPO 3D ALFI NORD 2021/Travail/Dao/Outils de traitement/Styles/MARKERS.qml') 
        
    def Aerien(self):
        aer = r"S:\09-Production\CLIENTS\AIR LIQUIDE\21-0178 TOPO 3D ALFI NORD 2021\Travail\Dao\Outils de traitement\SHP_FME\PARTIES_AERIENNES_A_AT_NOV2020.shp"
        vlayer = QgsVectorLayer(aer, "AERIEN", "ogr")
        QgsProject.instance().addMapLayer(vlayer)
        vlayer.loadNamedStyle('S:/09-Production/CLIENTS/AIR LIQUIDE/21-0178 TOPO 3D ALFI NORD 2021/Travail/Dao/Outils de traitement/Styles/AERIEN.qml')

    def Nett_Apr_liss(self):
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup("Apres lissage")
        for child in group.children():
            if "Ligne 2" in child.name():
                pass
            else:
                QgsProject.instance().removeMapLayer(child.layerId())
                
                
    def Nett_Av_liss(self):
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup("Avant lissage")
        for child in group.children():
            if "Ligne" in child.name():
                pass
            else:
                QgsProject.instance().removeMapLayer(child.layerId())