# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# ----------------------------------------------------------------------------
# Estimación de Densidad de Personas a través de Visión por Computador
# Nombre        Interfaz Principal
# Archivo:      InterfazPrincipal.py
# Autor:        Daniel David Zambrano Andrade
# Creado:       25 de Septiembre 2020
# Modificado:   19 de Abril 2021
# Copyright:    Libre
# License:      Libre
# ----------------------------------------------------------------------------

import os
import sys
from pathlib import Path
from PyQt5.QtCore import QSize, QRect, Qt, QCoreApplication
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QLabel, QComboBox, QPushButton, QMenuBar, QStatusBar, QMenu
from Scripts.BD import Database
from Scripts.Opt_Ayuda import Ayuda
from Scripts.Opt_Creditos import Creditos
from Scripts.Opt_verCUDA import VerificacionGPU
from Scripts.InterfazResultados import VisualizarResultados
from Scripts.cuadrosDialogos import close_event
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
img_ayuda = os.path.join(path, r'Recursos/ayuda.png')
imgNVIDIA = os.path.join(path, r'Recursos/NVIDIA.png')
imgPersonal = os.path.join(path, r'Recursos/Yo.png')
imgExit = os.path.join(path, r'Recursos/exit.png')
imgAyuda = os.path.join(path, r'Recursos/ayuda.png')
imgError = os.path.join(path, r"Recursos/Error.png")
imgFondo = os.path.join(path, r'Recursos/Blanco')
imgCrowd = os.path.join(path, r'Recursos/crowd2.png')
imgEliminar = os.path.join(path, r'Recursos/d1.png')
imgDatabase = os.path.join(path, r'Recursos/database.png')
imgSubir = os.path.join(path, r'Recursos/upload.png')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.baseDatos = ""
        self.procesar = ""
        self.multitudes = ""
        self.setEnabled(True)
        self.resize(1020, 720)
        self.setMinimumSize(QSize(1020, 720))
        self.setMaximumSize(QSize(1020, 720))
        self.font = QFont()
        self.font.setStyleStrategy(QFont.PreferAntialias)
        self.setFont(self.font)
        self.icon = QIcon()
        self.icon.addFile(imgCrowd, QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(self.icon)
        self.actionSobre = QAction(self)
        self.actionSobre.setObjectName(u"actionSobre")
        self.icon1 = QIcon()
        self.icon1.addFile(imgEliminar, QSize(), QIcon.Normal, QIcon.Off)
        self.actionSobre.setIcon(self.icon1)
        self.actionHistorial_de_Consultas = QAction(self)
        self.actionHistorial_de_Consultas.setObjectName(u"actionHistorial_de_Consultas")
        self.icon2 = QIcon()
        self.icon2.addFile(imgDatabase, QSize(), QIcon.Normal, QIcon.Off)
        self.actionHistorial_de_Consultas.setIcon(self.icon2)
        self.actionHistorial_de_Consultas.triggered.connect(self.historial)
        self.actionManual_de_Usuario = QAction(self)
        self.actionManual_de_Usuario.setObjectName(u"actionManual_de_Usuario")
        self.actionAutor = QAction(self)
        self.actionAutor.setObjectName(u"actionAutor")
        self.actionAyuda = QAction(self)
        self.actionAyuda.setObjectName(u"actionAyuda")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Titulo = QLabel(self.centralwidget)
        self.Titulo.setObjectName(u"Titulo")
        self.Titulo.setGeometry(QRect(0, 0, 1020, 165))
        self.font1 = QFont()
        self.font1.setFamily(u"Helvetica LT Std Fractions")
        self.font1.setPointSize(26)
        self.font1.setItalic(False)
        self.font1.setStrikeOut(False)
        self.font1.setKerning(True)
        self.font1.setStyleStrategy(QFont.PreferAntialias)
        self.Titulo.setFont(self.font1)
        self.Titulo.setScaledContents(True)
        self.Titulo.setAlignment(Qt.AlignCenter)
        self.BotonImagenes = QPushButton(self.centralwidget)
        self.BotonImagenes.setObjectName(u"BotonImagenes")
        self.BotonImagenes.setGeometry(QRect(410, 590, 200, 60))
        self.font2 = QFont()
        self.font2.setFamily(u"Helvetica LT Std Fractions")
        self.font2.setPointSize(13)
        self.font2.setBold(False)
        self.font2.setItalic(False)
        self.font2.setUnderline(False)
        self.font2.setWeight(50)
        self.font2.setStyleStrategy(QFont.PreferAntialias)
        self.BotonImagenes.setFont(self.font2)
        self.BotonImagenes.setStyleSheet(u"")
        self.icon3 = QIcon()
        self.icon3.addFile(imgSubir, QSize(), QIcon.Normal, QIcon.Off)
        self.BotonImagenes.setIcon(self.icon3)
        self.BotonImagenes.clicked.connect(self.procesamiento_imagen)
        self.BotonImagenes.setIconSize(QSize(40, 40))
        self.BotonImagenes.setAutoRepeatDelay(300)
        self.BotonImagenes.setAutoDefault(True)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(330, 140, 361, 294))
        self.label.setFont(self.font)
        self.label.setPixmap(QPixmap(imgCrowd))
        self.label.setScaledContents(True)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(-20, -10, 1241, 771))
        self.label_3.setPixmap(QPixmap(imgFondo))
        self.label_3.setScaledContents(True)
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(375, 470, 270, 60))
        self.font3 = QFont()
        self.font3.setFamily(u"Helvetica LT Std Fractions")
        self.font3.setPointSize(13)
        self.font3.setStyleStrategy(QFont.PreferAntialias)
        self.comboBox.setFont(self.font3)
        self.comboBox.setEditable(False)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(390, 440, 241, 31))
        self.font4 = QFont()
        self.font4.setFamily(u"Helvetica LT Std Fractions")
        self.font4.setPointSize(13)
        self.font4.setBold(True)
        self.font4.setWeight(75)
        self.font4.setStyleStrategy(QFont.PreferAntialias)
        self.label_4.setFont(self.font4)
        self.label_4.setScaledContents(True)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(390, 560, 241, 31))
        self.label_5.setFont(self.font4)
        self.label_5.setScaledContents(True)
        self.setCentralWidget(self.centralwidget)
        self.label_3.raise_()
        self.label_4.raise_()
        self.label.raise_()
        self.Titulo.raise_()
        self.BotonImagenes.raise_()
        self.label_5.raise_()
        self.comboBox.raise_()
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1020, 26))
        self.menuBase_de_Datos = QMenu(self.menubar)
        self.menuBase_de_Datos.setObjectName(u"menuBase_de_Datos")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuBase_de_Datos.menuAction())
        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"Estimación de Densidad de Personas a través de "
                                                                     u"Visión por Computador", None))
        self.actionSobre.setText(QCoreApplication.translate("MainWindow", u"Sobre", None))
        self.actionHistorial_de_Consultas.setText(QCoreApplication.translate("MainWindow", u"Historial", None))
        self.actionManual_de_Usuario.setText(QCoreApplication.translate("MainWindow", u"Manual de Usuario", None))
        self.actionAutor.setText(QCoreApplication.translate("MainWindow", u"Autor", None))
        self.actionAyuda.setText(QCoreApplication.translate("MainWindow", u"Ayuda", None))
        self.Titulo.setText(QCoreApplication.translate("MainWindow",
                                                       u"<html><head/><body><p align=\"center\"><span style=\" "
                                                       u"font-size:26pt; font-weight:600;\">ESTIMACIÓN DE DENSIDAD DE "
                                                       u"PERSONAS </span></p><p align=\"center\"><span style=\" "
                                                       u"font-size:26pt; font-weight:600;\">A TRAVÉS DE VISIÓN POR "
                                                       u"COMPUTADOR</span></p></body></html>",
                                                       None))
        self.BotonImagenes.setText(QCoreApplication.translate("MainWindow", u" Subir", None))
        self.label.setText("")
        self.label_3.setText("")
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Multitudes Dispersas", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Multitudes Densas", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Multitudes Combinadas", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Seleccione el modelo", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Seleccione la imagen", None))
        self.menuBase_de_Datos.setTitle(QCoreApplication.translate("MainWindow", u"Base de datos", None))
        self.menuBase_de_Datos.addAction(self.actionHistorial_de_Consultas)
        self.help_menu = self.menuBar().addMenu("&Ayuda")
        self.about_ayuda = QAction(QIcon(img_ayuda), "Ayuda", self)
        self.about_ayuda.triggered.connect(self.ayuda)
        self.help_menu.addAction(self.about_ayuda)
        self.ver_gpu = QAction(QIcon(imgNVIDIA), "Verificación CUDA", self)
        self.ver_gpu.triggered.connect(self.cuda)
        self.help_menu.addAction(self.ver_gpu)
        self.about_action = QAction(QIcon(imgPersonal), "Créditos", self)
        self.about_action.triggered.connect(self.creditos)
        self.help_menu.addAction(self.about_action)
        self.about_ayuda.setStatusTip("Ayuda")
        self.ver_gpu.setStatusTip("Verificación CUDA")
        self.about_action.setStatusTip("Créditos")

    def procesamiento_imagen(self):
        self.multitudes = self.comboBox.currentText()
        multitud = self.multitudes
        VisualizarResultados(multitud)

    def historial(self):
        self.baseDatos = Database(self)
        self.baseDatos.show()

    @staticmethod
    def creditos():
        creditos = Creditos()
        creditos.exec_()

    @staticmethod
    def ayuda():
        help_1 = Ayuda()
        help_1.exec_()

    @staticmethod
    def cuda():
        ver_cuda = VerificacionGPU()
        ver_cuda.exec_()

    def closeEvent(self, event):
        close_event(event, "¿Desea salir del programa?")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyleSheet(stylesheet)
#     w = MainWindow()
#     w.show()
#     sys.exit(app.exec_())
