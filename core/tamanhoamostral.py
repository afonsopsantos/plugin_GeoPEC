# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoPEC - Software científico para avaliação da acurácia posicional em 
   dados cartográficos
 GeoPEC - Scientific software for assessing positional accuracy in 
   spatial data

 A QGIS plugin [Generated by Plugin Builder]

Tamanho amostral: Definição do tamanho amostral pelas normas ISO 2859, 
  ET-CQDG (Brasil), NBR 13.133 (Brasil), ASPRS (2015), Portugal e 
  amostragem probabilística. 
Sample size: Definition of sample size according to ISO 2859, 
  ET-CQDG (Brazil), NBR 13.133 (Brazil), ASPRS (2015), Portugal standard
  and probabilistic sampling.

  autores: Afonso P. Santos; João Vítor A. Gonçalves; Luis Philippe Ventura
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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.core import *
from osgeo import gdal
# Initialize Qt resources from file resources.py
from ..resources import *
import processing
# Import the code for the dialog
from ..gui.tamanhoamostral_dialog import tamanhoamostralDialog
import os.path
import math

#Importando as funções usadas
from ..functions.amostral import *

class tamanhoamostral:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
    #################################
              
        # Pega o caminho do diretório onde o arquivo atual está localizado
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Sobe um nível na hierarquia de diretórios para chegar à pasta principal
        self.plugin_dir = os.path.dirname(current_dir)
        
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.plugin_dir,'i18n','pec_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
    #################################
                
        # Save reference to the QGIS interface
        self.iface = iface 
        self.dlg = tamanhoamostralDialog()
        
        #Configurando métodos para não aparecer janelas de erro mais de uma vez
        self.first_start = True
        self.connections_made = False

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
        return QCoreApplication.translate('tamanhoamostral', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        pass


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.mainWindow().menuBar().removeAction(self.menu.menuAction())
        del self.menu
        # remove the toolbar
        del self.toolbar


    def asprs2015 (self):   
        """ Método que calcula o tamanho amostral da janela da norma ASPRS 2015"""
        area = self.dlg.lineEdit_22.text()
        try:
            n2d,nva,vva,n3d = fAsprs(area)
            self.dlg.label_130.setText(str(n2d))
            self.dlg.label_131.setText(str(n3d))
            self.dlg.label_132.setText(str(nva))
            self.dlg.label_133.setText(str(vva))
        except:
            self.dlg.label_130.setText('Resultado')
            self.dlg.label_131.setText('Resultado')
            self.dlg.label_132.setText('Resultado')
            self.dlg.label_133.setText('Resultado')
            self.dlg.lineEdit_22.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')
        pass


    def nbr1994 (self): 
        """ Método que calcula o tamanho amostral da janela da norma NBR13133 de 1994"""
        valor = self.dlg.lineEdit_18.text()
        try:
            pontos = fNbr13133_94 (valor)
            self.dlg.label_128.setText(str(pontos))
        except:
            self.dlg.label_128.setText('Resultado')
            self.dlg.lineEdit_18.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')
            pass


    def nbr2021 (self):    
        """ Método que calcula o tamanho amostral da janela da norma NBR13133 de 2021"""      
        valor = self.dlg.lineEdit_20.text()
        try:
            pontos = fNbr13133_21 (valor)
            self.dlg.label_129.setText(str(pontos)) 
        except:      
            self.dlg.label_129.setText('Resultado')
            self.dlg.lineEdit_20.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')      
            pass

   
    def amostProbInf(self):
        """ Método que calcula o tamanho amostral da janela de amostragem probabilística com população infinita"""  
        desv = self.dlg.lineEdit_11.text()
        erro = self.dlg.lineEdit_12.text()
        index = self.dlg.comboBox_5.currentIndex() 
        try:  
            amostra = fPopInfinita (desv,erro, index)
            self.dlg.label_126.setText(str(amostra))
        except: 
            self.dlg.label_126.setText('Resultado')
            self.dlg.lineEdit_11.setText('')
            self.dlg.lineEdit_12.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')    
            pass
            

    def amostProbFin(self):    
        """ Método que calcula o tamanho amostral da janela de amostragem probabilística com população finita"""
        pop = self.dlg.lineEdit_14.text()
        desv = self.dlg.lineEdit_15.text()
        erro = self.dlg.lineEdit_16.text()
        index = self.dlg.comboBox_6.currentIndex()  
        try:     
            amostra = fPopFinita(pop,desv,erro, index)
            self.dlg.label_127.setText(str(amostra))
        except: 
            self.dlg.label_127.setText('Resultado')
            self.dlg.lineEdit_14.setText('')
            self.dlg.lineEdit_15.setText('')
            self.dlg.lineEdit_16.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')   
            pass


    def etAmostEspacial(self):
        """ Método que calcula o número de células da janela de amostragem espacial da ET-CQDG""" 
        area = self.dlg.lineEdit.text()
        escala = self.dlg.comboBox.currentText()
        try:      
            celulas = fCelulas(area,escala)
            self.dlg.label_119.setText(str(celulas)) 
        except:   
            self.dlg.label_119.setText('Resultado')
            self.dlg.lineEdit.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')  
            pass       
            
        
    def iso2859_1(self):    
        """ Método que calcula o tamanho amostral Lote a Lote da ET-CQDG"""
        amost = self.dlg.lineEdit_3.text()
        index01 = self.dlg.comboBox_2.currentIndex()
        index02 = self.dlg.comboBox_3.currentIndex()   
        try:      
            letra, ac, amostra  = fIso2859_1(amost, index01, index02)          
            self.dlg.label_120.setText(letra)
            self.dlg.label_121.setText(str(amostra))
            self.dlg.label_122.setText(str(ac))        
        except:         
            self.dlg.label_120.setText('Resultado')
            self.dlg.label_121.setText('Resultado')
            self.dlg.label_122.setText('Resultado')
            self.dlg.lineEdit_3.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')   
            pass  
   

    def iso2859_2(self):
        """ Método que calcula o tamanho amostral Lote isolado da ET-CQDG"""
        amost = self.dlg.lineEdit_7.text()
        index = self.dlg.comboBox_4.currentIndex()   
        try:   
            ql,amostra,ac  = fIso2859_2(amost, index) 
            self.dlg.label_123.setText(ql)
            self.dlg.label_124.setText(str(amostra))
            self.dlg.label_125.setText(str(ac))
        except:  
            self.dlg.label_123.setText('Resultado')
            self.dlg.label_124.setText('Resultado')
            self.dlg.label_125.setText('Resultado')
            self.dlg.lineEdit_7.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')        
            pass    

    
    def cartTopPortugal(self):
        """ Método que calcula o tamanho amostral da janela da norma CartTop de portugal"""
        area = self.dlg.lineEdit_2.text()
        escala = self.dlg.comboBox_7.currentText()
        try:            
            amostra  = fCartTopPortugal(area,escala)
            self.dlg.label_134.setText(str(amostra))  
        except:           
            self.dlg.label_134.setText('Resultado')
            self.dlg.lineEdit_2.setText('')
            QMessageBox.critical(self.dlg, 'Erro', 'Dados incoerentes. Digite um valor numérico válido')            
            pass       
        
            
    def run(self):
        """Run method that performs all the real work"""
       
        #Testando luis
        if not self.connections_made:
            
            
            #Conectando os pushButtons aos métodos         
            self.dlg.pushButton_8.clicked.connect(self.asprs2015)       
            self.dlg.pushButton_6.clicked.connect(self.nbr1994)       
            self.dlg.pushButton_7.clicked.connect(self.nbr2021)       
            self.dlg.pushButton_4.clicked.connect(self.amostProbInf)       
            self.dlg.pushButton_5.clicked.connect(self.amostProbFin)       
            self.dlg.pushButton_2.clicked.connect(self.iso2859_1)              
            self.dlg.pushButton_3.clicked.connect(self.iso2859_2)
            self.dlg.pushButton.clicked.connect(self.etAmostEspacial)              
            self.dlg.pushButton_9.clicked.connect(self.cartTopPortugal)  
            
            #Testando luis
            self.connections_made = True
        
        #show the dialog
        self.dlg.show()    
            # Run the dialog event loop
            #result = self.dlg.exec_()
            # See if OK was pressed
            #if result:
    # pass
	