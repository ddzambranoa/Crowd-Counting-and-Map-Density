# # -*- coding: utf-8 -*-
# # !/usr/bin/env python3
#
# # ----------------------------------------------------------------------------
# # Estimación de Densidad de Personas a través de Visión por Computador
# # Archivo:      main.py
# # Autor:        Daniel David Zambrano Andrade
# # Creado:       25 de Septiembre 2020
# # Modificado:   19 de Abril 2021
# # Copyright:    Libre
# # License:      Libre
# # ----------------------------------------------------------------------------
# import cv2
# import sys
# import time
# from time import strftime, time
# from IPython.external.qt_for_kernel import QtCore
# from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDesktopWidget, QTableWidget, QToolBar, \
#     QStatusBar, QAction, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, QPushButton, \
#     QHeaderView, QAbstractItemView, QDialogButtonBox, QLabel, QGridLayout, QGraphicsDropShadowEffect, QWidget, QFrame, \
#     QProgressBar
# from PyQt5.QtCore import Qt
# from PyQt5.uic import *
# from PyQt5.QtGui import QPixmap, QIcon, QTextDocument, QTextCursor, QIntValidator, QFont, QColor
# import PIL.Image as Image
# import numpy as np
# from PyQt5.QtCore import *
# from qtpy.uic import loadUi
# from skimage.transform import rescale
# from model import CSRNet
# import torch
# from torchvision import transforms
# from matplotlib import pyplot as plt
# import sqlite3
# import os
# from arrow import utcnow
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch, mm
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
# from reportlab.lib.enums import TA_LEFT, TA_CENTER
# from reportlab.lib.colors import black, purple, white
# from reportlab.pdfgen import canvas
# from xlsxwriter.workbook import Workbook
# import locale
# from shutil import rmtree
# import subprocess
# counter = 0
# global fecha
# global use_cuda
# locale.setlocale(locale.LC_ALL, '')
# global start_time
#
#
# class SplashScreen(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self, parent=None)
#         self.main = VentanaPrincipal()
#         self.ui = Ui_SplashScreen()
#         self.ui.setupUi(self)
#         self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
#         self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#         self.shadow = QGraphicsDropShadowEffect(self)
#         self.shadow.setBlurRadius(20)
#         self.shadow.setXOffset(0)
#         self.shadow.setYOffset(0)
#         self.shadow.setColor(QColor(0, 0, 0, 60))
#         self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.progress)
#         self.timer.start(35)
#         self.ui.label_description.setText("<strong>INICIANDO</strong>")
#         QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>CARGANDO</strong> BASE DE DATOS"))
#         QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>CARGANDO</strong> INTERFAZ DE USUARIO"))
#         self.show()
#
#     def progress(self):
#         global counter
#         self.ui.progressBar.setValue(counter)
#         if counter > 100:
#             self.timer.stop()
#             self.main.show()
#             self.close()
#         counter += 1
#
#
# class Ui_SplashScreen(object):
#
#     centralwidget: QWidget
#     verticalLayout: QVBoxLayout
#     dropShadowFrame: QFrame
#     label_title: QLabel
#     label_description = QLabel
#     progressBar = QProgressBar
#     label_loading = QLabel
#     label_credits = QLabel
#
#     def setupUi(self, SplashScreenI):
#         if SplashScreenI.objectName():
#             SplashScreenI.setObjectName(u"SplashScreen")
#         SplashScreenI.resize(680, 400)
#         self.centralwidget = QWidget(SplashScreenI)
#         self.centralwidget.setObjectName(u"centralwidget")
#         self.verticalLayout = QVBoxLayout()
#         self.verticalLayout.setSpacing(0)
#         self.verticalLayout.setObjectName(u"verticalLayout")
#         self.verticalLayout.setContentsMargins(10, 10, 10, 10)
#         self.dropShadowFrame = QFrame(self.centralwidget)
#         self.dropShadowFrame.setObjectName(u"dropShadowFrame")
#         self.dropShadowFrame.setStyleSheet(u"QFrame {	\n"
#                                            "	background-color: rgb(56, 58, 89);	\n"
#                                            "	color: rgb(220, 220, 220);\n"
#                                            "	border-radius: 10px;\n"
#                                            "}")
#         self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
#         self.dropShadowFrame.setFrameShadow(QFrame.Raised)
#         self.label_title = QLabel(self.dropShadowFrame)
#         self.label_title.setObjectName(u"label_title")
#         self.label_title.setGeometry(QRect(0, 90, 661, 61))
#         font = QFont()
#         font.setFamily(u"Segoe UI")
#         font.setPointSize(19)
#         self.label_title.setFont(font)
#         self.label_title.setStyleSheet(u"color: rgb(254, 121, 199);")
#         self.label_title.setAlignment(Qt.AlignCenter)
#         self.label_description = QLabel(self.dropShadowFrame)
#         self.label_description.setObjectName(u"label_description")
#         self.label_description.setGeometry(QRect(0, 150, 661, 31))
#         font1 = QFont()
#         font1.setFamily(u"Segoe UI")
#         font1.setPointSize(14)
#         self.label_description.setFont(font1)
#         self.label_description.setStyleSheet(u"color: rgb(98, 114, 164);")
#         self.label_description.setAlignment(Qt.AlignCenter)
#         self.progressBar = QProgressBar(self.dropShadowFrame)
#         self.progressBar.setObjectName(u"progressBar")
#         self.progressBar.setGeometry(QRect(50, 280, 561, 23))
#         self.progressBar.setStyleSheet(u"QProgressBar {\n"
#                                        "	\n"
#                                        "	background-color: rgb(98, 114, 164);\n"
#                                        "	color: rgb(200, 200, 200);\n"
#                                        "	border-style: none;\n"
#                                        "	border-radius: 10px;\n"
#                                        "	text-align: center;\n"
#                                        "}\n"
#                                        "QProgressBar::chunk{\n"
#                                        "	border-radius: 10px;\n"
#                                        "	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));\n"
#                                        "}")
#         self.progressBar.setValue(24)
#         self.label_loading = QLabel(self.dropShadowFrame)
#         self.label_loading.setObjectName(u"label_loading")
#         self.label_loading.setGeometry(QRect(0, 320, 661, 21))
#         font2 = QFont()
#         font2.setFamily(u"Segoe UI")
#         font2.setPointSize(10)
#         self.label_loading.setFont(font2)
#         self.label_loading.setStyleSheet(u"color: rgb(98, 114, 164);")
#         self.label_loading.setAlignment(Qt.AlignCenter)
#         self.label_credits = QLabel(self.dropShadowFrame)
#         self.label_credits.setObjectName(u"label_credits")
#         self.label_credits.setGeometry(QRect(20, 350, 621, 21))
#         font3 = QFont()
#         font3.setFamily(u"Segoe UI")
#         font3.setPointSize(9)
#         self.label_credits.setFont(font3)
#         self.label_credits.setStyleSheet(u"color: rgb(98, 114, 164);")
#         self.label_credits.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
#         self.verticalLayout.addWidget(self.dropShadowFrame)
#         SplashScreenI.setCentralWidget(self.centralwidget)
#         self.retranslateUi(SplashScreenI)
#         QMetaObject.connectSlotsByName(SplashScreenI)
#
#     def retranslateUi(self, SplashScreenI):
#         SplashScreenI.setWindowTitle(QCoreApplication.translate("SplashScreen", u"MainWindow", None))
#         self.label_title.setText(QCoreApplication.translate("SplashScreen", u"<strong>ESTIMACIÓN DE DENSIDAD DE PERSONAS</strong>", None))
#         self.label_description.setText(QCoreApplication.translate("SplashScreen", u"<strong></strong>", None))
#         self.label_loading.setText(QCoreApplication.translate("SplashScreen", u"Cargando...", None))
#         self.label_credits.setText(QCoreApplication.translate("SplashScreen", u"<strong>Creador</strong>: Daniel Zambrano A.", None))
#
#
# class VentanaPrincipal(QMainWindow):
#     def __init__(self):
#         try:
#             global use_cuda
#             use_cuda = torch.cuda.is_available()
#             if use_cuda:
#                 super(VentanaPrincipal, self).__init__()
#                 loadUi('Interfaz.ui', self)
#                 self.BotonImagenes.clicked.connect(self.procesamiento)
#                 self.actionHistorial_de_Consultas.triggered.connect(self.historial)
#                 self.center()
#                 self.setFixedSize(1020, 720)
#                 self.multitud = ""
#                 help_menu = self.menuBar().addMenu("&Ayuda")
#                 about_ayuda = QAction(QIcon("Recursos/ayuda.png"), "Ayuda", self)
#                 about_ayuda.triggered.connect(self.ayuda)
#                 help_menu.addAction(about_ayuda)
#                 ver_gpu = QAction(QIcon("Recursos/NVIDIA.png"), "Verificación CUDA", self)
#                 ver_gpu.triggered.connect(self.CUDA)
#                 help_menu.addAction(ver_gpu)
#                 about_action = QAction(QIcon("Recursos/Yo.png"), "Créditos", self)
#                 about_action.triggered.connect(self.about)
#                 help_menu.addAction(about_action)
#             else:
#                 self.CUDA()
#         except (ValueError, Exception):
#             pass
#
#     def procesamiento(self):
#         self.multitud = str(self.comboBox.currentText())
#         multitud = str(self.multitud)
#         procesamientoImagen(multitud)
#
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#     def historial(self):
#         window = BaseDeDatos(self)
#         window.show()
#         window.loaddata()
#
#     @staticmethod
#     def about():
#         dlg = AboutDialog()
#         dlg.exec_()
#
#     @staticmethod
#     def ayuda():
#         help_1 = Ayuda()
#         help_1.exec_()
#
#     @staticmethod
#     def CUDA():
#         ver_cuda = VerificacionGPU()
#         ver_cuda.exec_()
#
#     def closeEvent(self, event):
#         messageBox = QMessageBox(self)
#         messageBox.setWindowTitle("Salir")
#         messageBox.setIcon(QMessageBox.Question)
#         messageBox.setWindowIcon(QIcon("Recursos/exit.png"))
#         messageBox.setText("¿Desea salir del programa?")
#         Si = messageBox.addButton("Si", QMessageBox.YesRole)
#         No = messageBox.addButton("No", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#         if messageBox.clickedButton() == Si:
#             event.accept()
#         elif messageBox.clickedButton() == No:
#             event.ignore()
#
#
# class VentanaCarga(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self, parent=None)
#         # self.main = VentanaPrincipal()
#         self.ui = ventanaSoporteCarga()
#         self.ui.setupUi(self)
#         self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
#         self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#         self.shadow = QGraphicsDropShadowEffect(self)
#         self.shadow.setBlurRadius(20)
#         self.shadow.setXOffset(0)
#         self.shadow.setYOffset(0)
#         self.shadow.setColor(QColor(0, 0, 0, 60))
#         self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.progress)
#         self.timer.start(35)
#         self.ui.label_description.setText("<strong></strong>")
#         QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>CARGANDO</strong> ESPERE POR FAVOR"))
#         # QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>CARGANDO</strong> INTERFAZ DE USUARIO"))
#         self.show()
#
#     def progress(self):
#         global counter
#         self.ui.progressBar.setValue(counter)
#         if counter > 100:
#             self.timer.stop()
#             # self.main.show()
#             self.close()
#         counter += 1
#
#
# class ventanaSoporteCarga(object):
#
#     centralwidget: QWidget
#     verticalLayout: QVBoxLayout
#     dropShadowFrame: QFrame
#     label_title: QLabel
#     label_description = QLabel
#     progressBar = QProgressBar
#     label_loading = QLabel
#     label_credits = QLabel
#
#     def setupUi(self, SplashScreenI):
#         if SplashScreenI.objectName():
#             SplashScreenI.setObjectName(u"SplashScreen")
#         SplashScreenI.resize(680, 400)
#         self.centralwidget = QWidget(SplashScreenI)
#         self.centralwidget.setObjectName(u"centralwidget")
#         self.verticalLayout = QVBoxLayout()
#         self.verticalLayout.setSpacing(0)
#         self.verticalLayout.setObjectName(u"verticalLayout")
#         self.verticalLayout.setContentsMargins(10, 10, 10, 10)
#         self.dropShadowFrame = QFrame(self.centralwidget)
#         self.dropShadowFrame.setObjectName(u"dropShadowFrame")
#         self.dropShadowFrame.setStyleSheet(u"QFrame {	\n"
#                                            "	background-color: rgb(56, 58, 89);	\n"
#                                            "	color: rgb(220, 220, 220);\n"
#                                            "	border-radius: 10px;\n"
#                                            "}")
#         self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
#         self.dropShadowFrame.setFrameShadow(QFrame.Raised)
#         self.label_title = QLabel(self.dropShadowFrame)
#         self.label_title.setObjectName(u"label_title")
#         self.label_title.setGeometry(QRect(0, 90, 661, 61))
#         font = QFont()
#         font.setFamily(u"Segoe UI")
#         font.setPointSize(19)
#         self.label_title.setFont(font)
#         self.label_title.setStyleSheet(u"color: rgb(254, 121, 199);")
#         self.label_title.setAlignment(Qt.AlignCenter)
#         self.label_description = QLabel(self.dropShadowFrame)
#         self.label_description.setObjectName(u"label_description")
#         self.label_description.setGeometry(QRect(0, 150, 661, 31))
#         font1 = QFont()
#         font1.setFamily(u"Segoe UI")
#         font1.setPointSize(14)
#         self.label_description.setFont(font1)
#         self.label_description.setStyleSheet(u"color: rgb(98, 114, 164);")
#         self.label_description.setAlignment(Qt.AlignCenter)
#         self.progressBar = QProgressBar(self.dropShadowFrame)
#         self.progressBar.setObjectName(u"progressBar")
#         self.progressBar.setGeometry(QRect(50, 280, 561, 23))
#         self.progressBar.setStyleSheet(u"QProgressBar {\n"
#                                        "	\n"
#                                        "	background-color: rgb(98, 114, 164);\n"
#                                        "	color: rgb(200, 200, 200);\n"
#                                        "	border-style: none;\n"
#                                        "	border-radius: 10px;\n"
#                                        "	text-align: center;\n"
#                                        "}\n"
#                                        "QProgressBar::chunk{\n"
#                                        "	border-radius: 10px;\n"
#                                        "	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));\n"
#                                        "}")
#         self.progressBar.setValue(24)
#         self.label_loading = QLabel(self.dropShadowFrame)
#         self.label_loading.setObjectName(u"label_loading")
#         self.label_loading.setGeometry(QRect(0, 320, 661, 21))
#         font2 = QFont()
#         font2.setFamily(u"Segoe UI")
#         font2.setPointSize(10)
#         self.label_loading.setFont(font2)
#         self.label_loading.setStyleSheet(u"color: rgb(98, 114, 164);")
#         self.label_loading.setAlignment(Qt.AlignCenter)
#         self.label_credits = QLabel(self.dropShadowFrame)
#         self.label_credits.setObjectName(u"label_credits")
#         self.label_credits.setGeometry(QRect(20, 350, 621, 21))
#         font3 = QFont()
#         font3.setFamily(u"Segoe UI")
#         font3.setPointSize(9)
#         self.label_credits.setFont(font3)
#         self.label_credits.setStyleSheet(u"color: rgb(98, 114, 164);")
#         self.label_credits.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
#         self.verticalLayout.addWidget(self.dropShadowFrame)
#         SplashScreenI.setCentralWidget(self.centralwidget)
#         self.retranslateUi(SplashScreenI)
#         QMetaObject.connectSlotsByName(SplashScreenI)
#
#     def retranslateUi(self, SplashScreenI):
#         SplashScreenI.setWindowTitle(QCoreApplication.translate("SplashScreen", u"MainWindow", None))
#         self.label_title.setText(QCoreApplication.translate("SplashScreen", u"<strong>ESTIMACIÓN DE DENSIDAD DE PERSONAS</strong>", None))
#         self.label_description.setText(QCoreApplication.translate("SplashScreen", u"<strong></strong>", None))
#         self.label_loading.setText(QCoreApplication.translate("SplashScreen", u"Analizando...", None))
#         self.label_credits.setText(QCoreApplication.translate("SplashScreen", u"<strong>Creador</strong>: Daniel Zambrano A.", None))
#
#
# class VentanaResultados(QMainWindow):
#     def __init__(self, parent=None, imgOriginal=None, imgMapa=None, resConteo=None, resZonas=None):
#         super(VentanaResultados, self).__init__(parent)
#         loadUi("ImagenesConsulta.ui", self)
#         self.show()
#         try:
#             self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#             self.center()
#             self.setFixedSize(1800, 900)
#             self.Number_2.setStyleSheet("QLabel""{""color : #ffffff;""background : red;""}")
#             self.ImagenOriginal.setPixmap(QPixmap(imgOriginal))
#             self.MapaDeDensidad_2.setPixmap(QPixmap(imgMapa))
#             self.Number.setText(resConteo)
#             self.Number_2.setText(str(resZonas))
#         except (ValueError, Exception):
#             print("ERROR")
#
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#
# class procesamientoImagen(QMainWindow):
#     def __init__(self, multitud=None, parent=None):
#         super().__init__(parent)
#         self.ventana = loadUi("ImagenesConsulta.ui", self)
#         self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#         self.center()
#         self.setFixedSize(1800, 900)
#         self.Number_2.setStyleSheet("QLabel""{""color : #ffffff;""background : red;""}")
#         self.multitudes = multitud
#         self.get_image_file()
#         self.file_name = ""
#         self.base = ""
#         self.name = ""
#         self.nameFile = ""
#         self.file = ""
#         self.almImg = ""
#         self.dir_F = ""
#         self.rutaAlmacenamiento = ""
#         self.conn = ""
#         self.c = ""
#         self.den = ""
#         self.Rden = ""
#         self.conteo = 0
#         self.totalCnts = ""
#         self.Zona = ""
#         self.imagen_O = ""
#         self.Img_O = ""
#         self.Zona_N = ""
#         self.Zona_B = ""
#         self.Zona_C = ""
#         self.imagen = ""
#         self.imagen_2 = ""
#         self.imagen_3 = ""
#         self.IMG_CV2JET = ""
#
#     def get_image_file(self):
#         try:
#             self.file_name, _ = QFileDialog.getOpenFileName(self, 'Subir Imagen', r"", "Imagen (*.jpg *.png)")
#             self.name = os.path.abspath(self.file_name)
#             if self.file_name != "":
#                 self.predecir()
#                 self.ventana.show()
#             else:
#                 pass
#         except (ValueError, Exception):
#             pass
#
#     def predecir(self):
#         try:
#             global fecha
#             fecha = strftime("%B-%d-%Y_%H_%M_%S")
#             self.base = os.path.basename(self.name)
#             self.file = os.path.splitext(self.base)[0]
#             _time = time()
#             try:
#                 os.stat("Modelos Entrenados")
#             except (ValueError, Exception):
#                 os.mkdir("Modelos Entrenados")
#             if self.multitudes == "Multitudes Dispersas":
#                 modeloentrenado = 'Modelos Entrenados/Multitudes_Dispersas.pth.tar'
#             elif self.multitudes == "Multitudes Densas":
#                 modeloentrenado = "Modelos Entrenados/Multitudes_Densas.pth.tar"
#             elif self.multitudes == "Multitudes Combinadas":
#                 modeloentrenado = 'Modelos Entrenados/Multitudes_Densas-Dispersas.pth.tar'
#             else:
#                 modeloentrenado = 'Modelos Entrenados/Multitudes_Dispersas.pth.tar'
#             transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
#             model = CSRNet()
#             model = model.cuda()
#             checkpoint = torch.load(modeloentrenado)
#             model.load_state_dict(checkpoint['state_dict'])
#             img = transform(Image.open(self.name).convert('RGB')).cuda()
#             output = model(img.unsqueeze(0))
#             self.conteo = str(int(output.detach().cpu().sum().numpy()))
#             MapaDensidad = np.asarray(output.detach().cpu().reshape(output.detach().cpu().shape[2], output.detach().cpu().shape[3]))
#             ROOT_DIR = os.path.dirname(__file__)
#             try:
#                 os.stat(ROOT_DIR + "/Mapas_De_Densidad/")
#             except (ValueError, Exception):
#                 os.mkdir(ROOT_DIR + "/Mapas_De_Densidad/")
#             self.almImg = "/Mapas_De_Densidad/" + str(str(self.file)) + "_" + str(fecha).capitalize()
#             self.dir_F = ROOT_DIR + self.almImg
#             self.Rden = self.dir_F + "/" + str(str(self.file))
#             self.den = self.Rden + "_Densidad" + ".png"
#             os.mkdir(self.dir_F)
#             MapaDensidad = rescale(MapaDensidad, 8, anti_aliasing=True)
#             plt.imsave(self.den, MapaDensidad, cmap='jet', vmin=0, vmax=0.07)
#             rojoBajo1 = np.array([0, 50, 20], np.uint8)
#             rojoAlto1 = np.array([30, 255, 255], np.uint8)
#             rojoBajo2 = np.array([150, 50, 20], np.uint8)
#             rojoAlto2 = np.array([180, 255, 255], np.uint8)
#             self.imagen = cv2.imread(self.den)
#             self.imagen_2 = cv2.imread(self.den)
#             self.imagen_O = cv2.imread(self.name)
#             bordersize = 30
#             self.imagen = cv2.copyMakeBorder(self.imagen, top=bordersize, bottom=bordersize, left=bordersize,
#                                              right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[127, 0, 0])
#             self.imagen_2 = cv2.copyMakeBorder(self.imagen_2, top=bordersize, bottom=bordersize, left=bordersize,
#                                                right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[127, 0, 0])
#             imagenHSV = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2HSV)
#             maskRojo1 = cv2.inRange(imagenHSV, rojoBajo1, rojoAlto1)
#             maskRojo2 = cv2.inRange(imagenHSV, rojoBajo2, rojoAlto2)
#             maskRojo = cv2.add(maskRojo1, maskRojo2)
#             contornosRojo = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
#             self.dibujarContorno(contornosRojo)
#             self.totalCnts = len(contornosRojo)
#             self.imagen_3 = cv2.applyColorMap(self.imagen_2, cv2.COLORMAP_JET)
#             self.IMG_CV2JET = self.Rden + "_Mapa_Calor" + ".png"
#             self.Img_O = self.Rden + ".png"
#             self.Zona_N = self.Rden + "_Numerada" + ".png"
#             self.Zona_C = self.Rden + "_Contorno" + ".png"
#             self.Zona_B = self.Rden + "_Binaria" + ".png"
#             cv2.imwrite(self.Zona_B, maskRojo)
#             cv2.imwrite(self.Zona_N, self.imagen)
#             cv2.imwrite(self.Zona_C, self.imagen_2)
#             cv2.imwrite(self.Img_O, self.imagen_O)
#             cv2.imwrite(self.IMG_CV2JET, self.imagen_3)
#             # elapsed_time = time() - _time
#             # print(elapsed_time)
#             self.AlmacenarDatos()
#             sqliteExcel()
#             pdf()
#             imgOriginal = str(self.file_name)
#             imgMapa = str(self.Zona_C)
#             resConteo = str(self.conteo)
#             resZonas = str(self.totalCnts)
#             print(imgOriginal)
#             print(imgMapa)
#             print(resConteo)
#             print(resZonas)
#             # self.visualizarResultado(imgOriginal, imgMapa, resConteo, resZonas)
#             self.ImagenOriginal.setPixmap(QPixmap(imgOriginal))
#             self.MapaDeDensidad_2.setPixmap(QPixmap(imgMapa))
#             self.Number.setText(resConteo)
#             self.Number_2.setText(str(resZonas))
#         except (ValueError, Exception):
#             self.errorModelo()
#
#     def visualizarResultado(self, imgOriginal, imgMapa, resConteo, resZonas):
#         # window = VentanaResultados(self, imgOriginal, imgMapa, resConteo, resZonas)
#         # window.show()
#         ventana = loadUi("ImagenesConsulta.ui", self)
#         ventana.show()
#         try:
#             self.setWindowFlags(
#                 QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#             self.center()
#             self.setFixedSize(1800, 900)
#             self.Number_2.setStyleSheet("QLabel""{""color : #ffffff;""background : red;""}")
#             self.ImagenOriginal.setPixmap(QPixmap(imgOriginal))
#             self.MapaDeDensidad_2.setPixmap(QPixmap(imgMapa))
#             self.Number.setText(resConteo)
#             self.Number_2.setText(str(resZonas))
#         except (ValueError, Exception):
#             print("ERROR")
#
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#     def errorModelo(self):
#         messageBox = QMessageBox(self)
#         messageBox.setWindowTitle("Error")
#         messageBox.setIcon(QMessageBox.Critical)
#         messageBox.setWindowIcon(QIcon("Recursos/Error.png"))
#         messageBox.setText(
#             "Falla en el sistema, compruebe las dimensiones de la imagen y el modelo entrenado de la red neuronal convolucional.")
#         Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#
#     def dibujarContorno(self, contornos):
#         for (i, c) in enumerate(contornos):
#             M = cv2.moments(c)
#             if M["m00"] != 0:
#                 x = int(M["m10"] / M["m00"])
#                 y = int(M["m01"] / M["m00"])
#             else:
#                 x, y = 0, 0
#             cv2.drawContours(self.imagen, [c], 0, (0, 0, 255), 2)
#             cv2.drawContours(self.imagen_2, [c], 0, (0, 255, 255), 4)
#             cv2.putText(self.imagen, str(i + 1), (x, y), 5, 1, (0, 0, 0), 2)
#
#     def AlmacenarDatos(self):
#         ImagenOriginal = os.path.basename(self.Img_O)
#         Aproximacion = self.conteo
#         Zona = self.totalCnts
#         Modelo = self.multitudes
#         Fecha = strftime("%H:%M:%S")
#         Year = strftime("%B %d, %Y").capitalize()
#         MapaDeDensidad = os.path.basename(self.den)
#         ImagenBinaria = os.path.basename(self.Zona_B)
#         ImagenNumerada = os.path.basename(self.Zona_N)
#         ImagenContorno = os.path.basename(self.Zona_C)
#         MapaCV2 = os.path.basename(self.IMG_CV2JET)
#         Ruta = self.dir_F
#         try:
#             try:
#                 os.stat("Database")
#             except (ValueError, Exception):
#                 os.mkdir("Database")
#             self.conn = sqlite3.connect("Database/Consultas.db")
#             self.c = self.conn.cursor()
#             self.c.execute(
#                 "CREATE TABLE IF NOT EXISTS historial(roll INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,ImagenOriginal TEXT,"
#                 "Aproximacion TEXT,Zona TEXT, Modelo TEXT, Fecha TEXT, Year Text,  MapaDeDensidad TEXT, ImagenBinaria TEXT,ImagenNumerada TEXT, ImagenContorno TEXT, MapaCV2 TEXT, Ruta TEXT)")
#             self.c.execute(
#                 "INSERT INTO historial (ImagenOriginal, Aproximacion, Zona, Modelo, Fecha, Year,  MapaDeDensidad, ImagenBinaria,ImagenNumerada, ImagenContorno, MapaCV2, Ruta) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
#                 (ImagenOriginal, Aproximacion, Zona, Modelo, Fecha, Year, MapaDeDensidad, ImagenBinaria, ImagenNumerada,
#                  ImagenContorno, MapaCV2, Ruta))
#             self.conn.commit()
#             self.c.close()
#             self.conn.close()
#             file = open(Ruta + "/Resumen.txt", "w")
#             file.write("Nombre de la imagen: " + ImagenOriginal + os.linesep)
#             file.write("Aproximación de personas: " + str(Aproximacion) + os.linesep)
#             file.write("Zonas de posibles aglomeraciones: " + str(Zona) + os.linesep)
#             file.write("Modelo seleccionado: " + Modelo + os.linesep)
#             file.write("Hora de consulta: " + Fecha + os.linesep)
#             file.write("Fecha de consulta: " + Year + os.linesep)
#             file.write("Nombre del mapa de densidad: " + MapaDeDensidad + os.linesep)
#             file.write("Nombre de la imagen binaria: " + ImagenBinaria + os.linesep)
#             file.write("Nombre de la imagen numerada: " + ImagenNumerada + os.linesep)
#             file.write("Nombre de la imagen con contorno: " + ImagenContorno + os.linesep)
#             file.write("Nombre del mapa de densidad de openCV: " + MapaCV2 + os.linesep)
#             file.write("Ruta de la carpeta contenedora: " + Ruta + os.linesep)
#             file.close()
#             self.confirmacionConsulta()
#         except (ValueError, Exception):
#             self.errorConsultas()
#
#     def confirmacionConsulta(self):
#         messageBox = QMessageBox(self)
#         messageBox.setWindowTitle("Mensaje")
#         messageBox.setIcon(QMessageBox.Information)
#         messageBox.setWindowIcon(QIcon("Recursos/database.png"))
#         messageBox.setText("Consulta agregada a historial de consultas")
#         Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#
#     def errorConsultas(self):
#         messageBox = QMessageBox(self)
#         messageBox.setWindowTitle("Error")
#         messageBox.setIcon(QMessageBox.Warning)
#         messageBox.setWindowIcon(QIcon("Recursos/database.png"))
#         messageBox.setText("Consulta no agregada a historial. Reinicie el programa.")
#         Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#
#
# class BaseDeDatos(QMainWindow):
#     def __init__(self, *args, **kwargs):
#         super(BaseDeDatos, self).__init__(*args, **kwargs)
#         self.setWindowIcon(QIcon("Recursos/database.png"))
#         self.connection = ""
#         self.conn = sqlite3.connect("Database/Consultas.db")
#         self.c = self.conn.cursor()
#         self.c.execute(
#             "CREATE TABLE IF NOT EXISTS historial(roll INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,ImagenOriginal TEXT,"
#             "Aproximacion TEXT,Zona TEXT, Modelo TEXT,Fecha TEXT, Year Text, MapaDeDensidad TEXT, ImagenBinaria TEXT,ImagenNumerada TEXT, ImagenContorno TEXT, MapaCV2 TEXT, Ruta)")
#         self.c.close()
#         self.center()
#         file_menu = self.menuBar().addMenu("&Archivos")
#         self.setWindowTitle("Historial de Consultas")
#         self.setMinimumSize(1345, 740)
#         self.setMaximumSize(1350, 740)
#         self.tableWidget = QTableWidget()
#         self.setCentralWidget(self.tableWidget)
#         self.tableWidget.setAlternatingRowColors(True)
#         self.tableWidget.setStyleSheet("background-color: #BCD9EA;")
#         self.tableWidget.setColumnCount(12)
#         self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
#         self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
#         self.tableWidget.horizontalHeader().setStretchLastSection(False)
#         self.tableWidget.verticalHeader().setVisible(False)
#         self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
#         self.tableWidget.verticalHeader().setStretchLastSection(False)
#         self.tableWidget.setHorizontalHeaderLabels(("No. Consulta", "Nombre de la Imagen", "No. Aproximado de personas",
#                                                     "Zonas Posibles de Aglomeración", "Modelo Seleccionado",
#                                                     "Hora de Consulta", "Fecha de Consulta", "Mapa de Densidad",
#                                                     "Imagen Binaria",
#                                                     "Imagen Numerada", "Imagen Contorno", "Mapa CV2", "Ruta"))
#         self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
#         for indice, ancho in enumerate((100, 300, 225, 225, 175, 150, 150, 300, 300, 300, 300, 300), start=0):
#             self.tableWidget.setColumnWidth(indice, ancho)
#         self.tableWidget.setColumnHidden(7, True)
#         self.tableWidget.setColumnHidden(8, True)
#         self.tableWidget.setColumnHidden(9, True)
#         self.tableWidget.setColumnHidden(10, True)
#         self.tableWidget.setColumnHidden(11, True)
#         self.tableWidget.setColumnHidden(12, True)
#         toolbar = QToolBar()
#         toolbar.setMovable(False)
#         self.addToolBar(toolbar)
#         statusbar = QStatusBar()
#         self.setStatusBar(statusbar)
#         btn_ac_refresh = QAction(QIcon("Recursos/r3.png"), "Actualizar Reporte/Base de Datos", self)  # refresh icon
#         btn_ac_refresh.triggered.connect(self.loaddata)
#         btn_ac_refresh.setStatusTip("Refresh Table")
#         toolbar.addAction(btn_ac_refresh)
#         btn_ac_search = QAction(QIcon("Recursos/visualizar3.png"), "Visualizar", self)  # search icon
#         btn_ac_search.triggered.connect(self.search)
#         btn_ac_search.setStatusTip("Search User")
#         toolbar.addAction(btn_ac_search)
#         btn_ac_delete = QAction(QIcon("Recursos/d1.png"), "Borrar", self)
#         btn_ac_delete.triggered.connect(self.delete)
#         btn_ac_delete.triggered.connect(self.loaddata)
#         btn_ac_delete.setStatusTip("Borrar Consulta")
#         toolbar.addAction(btn_ac_delete)
#         export_Excel_m = QAction(QIcon("Recursos/EXCEL.png"), "Exportar a Excel", self)
#         export_Excel_m.triggered.connect(self.EXCELread)
#         export_Excel_m.triggered.connect(self.loaddata)
#         export_Excel_m.setStatusTip("Exportar a Excel, si tiene un archivo exportado anteriormente cierrelo inmediatamente.")
#         toolbar.addAction(export_Excel_m)
#         export_PDF_m = QAction(QIcon("Recursos/PDF.png"), "Exportar a PDF", self)
#         export_PDF_m.triggered.connect(self.PDFread)
#         export_PDF_m.triggered.connect(self.loaddata)
#         export_PDF_m.setStatusTip(
#             "Exportar a PDF, si tiene un archivo exportado anteriormente cierrelo inmediatamente.")
#         toolbar.addAction(export_PDF_m)
#         searchuser_action = QAction(QIcon("Recursos/visualizar3.png"), "Visualizar", self)
#         searchuser_action.triggered.connect(self.search)
#         file_menu.addAction(searchuser_action)
#         deluser_action = QAction(QIcon("Recursos/d1.png"), "Borrar", self)
#         deluser_action.triggered.connect(self.delete)
#         deluser_action.triggered.connect(self.loaddata)
#         file_menu.addAction(deluser_action)
#         findMenu = file_menu.addMenu(QIcon("Recursos/exportar.png"), 'Exportar')
#         export_Excel = QAction(QIcon("Recursos/EXCEL.png"), 'Exportar a Excel', self)
#         export_Excel.setStatusTip(
#             'Exportar base de datos a EXCEL, si tiene un archivo exportado anteriormente cierrelo inmediatamente.')
#         export_Excel.triggered.connect(self.loaddata)
#         export_Excel.triggered.connect(self.EXCELread)
#         export_PDF = QAction(QIcon("Recursos/PDF.png"), 'Exportar a PDF', self)
#         export_PDF.setStatusTip(
#             'Exportar base de datos a PDF, si tiene un archivo exportado anteriormente cierrelo inmediatamente.')
#         export_PDF.triggered.connect(self.loaddata)
#         export_PDF.triggered.connect(self.PDFread)
#         findMenu.addAction(export_Excel)
#         findMenu.addAction(export_PDF)
#         help_menu = self.menuBar().addMenu("&Ayuda")
#         about_ayuda = QAction(QIcon("Recursos/ayuda.png"), "Ayuda ", self)
#         about_ayuda.triggered.connect(self.ayuda)
#         help_menu.addAction(about_ayuda)
#         ver_gpu = QAction(QIcon("Recursos/NVIDIA.png"), "Verificación CUDA", self)
#         ver_gpu.triggered.connect(self.CUDA)
#         help_menu.addAction(ver_gpu)
#         about_action = QAction(QIcon("Recursos/Yo.png"), "Créditos ", self)  # info icon
#         about_action.triggered.connect(self.about)
#         help_menu.addAction(about_action)
#
#     def loaddata(self):
#         self.connection = sqlite3.connect("Database/Consultas.db")
#         query = "SELECT * FROM historial"
#         pdf()
#         sqliteExcel()
#         result = self.connection.execute(query)
#         self.tableWidget.setRowCount(0)
#         for row_number, row_data in enumerate(result):
#             self.tableWidget.insertRow(row_number)
#             for column_number, data in enumerate(row_data):
#                 item = QTableWidgetItem(str(data))
#                 item.setTextAlignment(Qt.AlignHCenter)
#                 self.tableWidget.setItem(row_number, column_number, item)
#         self.connection.close()
#
#     def handlePaintRequest(self, printer):
#         document = QTextDocument()
#         cursor = QTextCursor(document)
#         model = self.table.model()
#         table = cursor.insertTable(model.rowCount(), model.columnCount())
#         for row in range(table.rows()):
#             for column in range(table.columns()):
#                 cursor.insertText(model.item(row, column).text())
#                 cursor.movePosition(QTextCursor.NextCell)
#         document.print_(printer)
#
#     @staticmethod
#     def delete():
#         dlg = DeleteDialog()
#         dlg.exec_()
#
#     @staticmethod
#     def search():
#         dlg = SearchDialog()
#         dlg.exec_()
#
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#
#     @staticmethod
#     def about():
#         dlg = AboutDialog()
#         dlg.exec_()
#
#     @staticmethod
#     def ayuda():
#         help_1 = Ayuda()
#         help_1.exec_()
#
#     @staticmethod
#     def CUDA():
#         ver_cuda = VerificacionGPU()
#         ver_cuda.exec_()
#
#     @staticmethod
#     def PDFread():
#         try:
#             subprocess.Popen(['Reportes/Reporte de Consultas.pdf'], shell=True)
#         except IOError:
#             errorExportar()
#
#     @staticmethod
#     def EXCELread():
#         try:
#             subprocess.Popen(['Reportes/Reporte de Consultas.xlsx'], shell=True)
#         except (ValueError, Exception):
#             pass
#
#     def abrirVentanaPrincipal(self):
#         self.parent().show()
#         self.close()
#
#     def closeEvent(self, event):
#         self.abrirVentanaPrincipal()
#
#
# class SearchDialog(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(SearchDialog, self).__init__(*args, **kwargs)
#         self.conn = ""
#         self.c = ""
#         self.serachresult = ""
#         self.QBtn = QPushButton()
#         self.QBtn.setText("Visualizar")
#         self.setWindowTitle("Visualizar Consulta")
#         self.setWindowIcon(QIcon("Recursos/s1.png"))
#         self.setFixedWidth(300)
#         self.setFixedHeight(100)
#         self.QBtn.clicked.connect(self.buscarConsulta)
#         layout = QVBoxLayout()
#         self.setWindowFlags(
#             QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#         self.searchinput = QLineEdit()
#         self.onlyInt = QIntValidator()
#         self.searchinput.setValidator(self.onlyInt)
#         self.searchinput.setPlaceholderText("No. Consulta")
#         layout.addWidget(self.searchinput)
#         layout.addWidget(self.QBtn)
#         self.setLayout(layout)
#
#     def buscarConsulta(self):
#         searchrol = self.searchinput.text()
#         self.close()
#         try:
#             self.conn = sqlite3.connect("Database/Consultas.db")
#             self.c = self.conn.cursor()
#             result = self.c.execute("SELECT * from historial WHERE roll =" + str(searchrol))
#             row = result.fetchone()
#             self.serachresult = "Consulta: " + str(row[0]) + '\n' + "Nombre: " + str(
#                 row[1]) + '\n' + "Aproximación: " + str(row[2]) + '\n' + "Zonas con Aglomeración: " + str(
#                 row[3]) + '\n' + "Modelo: " + str(row[4]) + '\n' + "Hora de Consulta: " + str(
#                 row[5]) + '\n' + "Fecha de Consulta: " + str(row[6])
#             img_o = str(row[12]) + "/" + str(row[1])
#             img_d = str(row[12]) + "/" + str(row[7])
#             img_b = str(row[12]) + "/" + str(row[8])
#             img_n = str(row[12]) + "/" + str(row[9])
#             img_c = str(row[12]) + "/" + str(row[10])
#             img_mp = str(row[12]) + "/" + str(row[11])
#             imagenMP = cv2.imread(img_mp)
#             cv2.imshow('Imagen Mapa CV2', imagenMP)
#             imagenN = cv2.imread(img_n)
#             cv2.imshow('Imagen Numerada', imagenN)
#             imagenC = cv2.imread(img_c)
#             cv2.imshow('Imagen Contorno', imagenC)
#             imagenB = cv2.imread(img_b)
#             cv2.imshow('Imagen Binaria', imagenB)
#             imagenMD = cv2.imread(img_d)
#             cv2.imshow('Mapa de Densidad', imagenMD)
#             imagenO = cv2.imread(img_o)
#             cv2.imshow('Imagen Original', imagenO)
#             self.visualizar()
#             self.conn.commit()
#             self.c.close()
#             self.conn.close()
#         except (ValueError, Exception):
#             self.errorVisualizacion()
#
#     def visualizar(self):
#         messageBox = QMessageBox(self)
#         messageBox.setWindowTitle("Visualización de Imágenes")
#         messageBox.setIcon(QMessageBox.Information)
#         messageBox.setWindowIcon(QIcon("Recursos/database.png"))
#         messageBox.setText(self.serachresult)
#         Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#
#     @staticmethod
#     def errorVisualizacion():
#         messageBox = QMessageBox()
#         messageBox.setWindowTitle("Error")
#         messageBox.setIcon(QMessageBox.Warning)
#         messageBox.setWindowIcon(QIcon("Recursos/database.png"))
#         messageBox.setText("Consulta no encontrada.")
#         Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#
#
# class DeleteDialog(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(DeleteDialog, self).__init__(*args, **kwargs)
#         self.conn = ""
#         self.c = ""
#         self.serachresultdel = ""
#         self.QBtn = QPushButton()
#         self.QBtn.setText('Borrar')
#         self.setWindowTitle("Borrar Consulta")
#         self.setWindowIcon(QIcon("Recursos/d1.png"))
#         self.setFixedWidth(300)
#         self.setFixedHeight(100)
#         self.QBtn.clicked.connect(self.deleteconsulta)
#         layout = QVBoxLayout()
#         self.setWindowFlags(
#             QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#         self.deleteinput = QLineEdit()
#         self.onlyInt = QIntValidator()
#         self.deleteinput.setValidator(self.onlyInt)
#         self.deleteinput.setPlaceholderText("No. Consulta")
#         layout.addWidget(self.deleteinput)
#         layout.addWidget(self.QBtn)
#         self.setLayout(layout)
#
#     def deleteconsulta(self):
#         delrol = self.deleteinput.text()
#         self.close()
#         try:
#             self.conn = sqlite3.connect("Database/Consultas.db")
#             self.c = self.conn.cursor()
#             result = self.c.execute("SELECT * from historial WHERE roll =" + str(delrol))
#             row = result.fetchone()
#             rmtree(str(row[12]))
#             self.c.execute("DELETE from historial WHERE roll=" + str(delrol))
#             self.conn.commit()
#             pdf()
#             self.c.close()
#             self.conn.close()
#             self.confirmacionEliminacion()
#             self.close()
#         except (ValueError, Exception):
#             self.errorEliminacion()
#
#     def confirmacionEliminacion(self):
#         messageBox = QMessageBox(self)
#         messageBox.setWindowTitle("Listo")
#         messageBox.setIcon(QMessageBox.Information)
#         messageBox.setWindowIcon(QIcon("Recursos/database.png"))
#         messageBox.setText('Consulta eliminada de historial.')
#         Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#
#     @staticmethod
#     def errorEliminacion():
#         messageBox = QMessageBox()
#         messageBox.setWindowTitle("Error")
#         messageBox.setIcon(QMessageBox.Warning)
#         messageBox.setWindowIcon(QIcon("Recursos/database.png"))
#         messageBox.setText("Consulta no eliminada de historial.")
#         Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#
#
# class reportePDF(object):
#     def __init__(self, datos):
#         super(reportePDF, self).__init__()
#         self.titulo = "REPORTE DE CONSULTAS"
#         self.cabecera = (("ImagenOriginal", "Imagen Original"), ("Aproximacion", "Aproximacion de Personas"),
#                          ("Zona", "Zonas Posibles de Aglomeración"), ("Modelo", "Modelo Seleccionado"),
#                          ("Fecha", "Hora"), ("Year", "Fecha"), ("Ruta", "Ruta"))
#         self.datos = datos
#         try:
#             os.stat("Reportes")
#         except (ValueError, Exception):
#             os.mkdir("Reportes")
#         self.nombrePDF = "Reportes/Reporte de Consultas.pdf"
#         self.estilos = getSampleStyleSheet()
#         self.ancho = ""
#         self.alto = ""
#
#     @staticmethod
#     def _encabezadoPiePagina(canva, archivoPDF):
#         canva.saveState()
#         estilos = getSampleStyleSheet()
#         alineacion = ParagraphStyle(name="alineacion", alignment=TA_LEFT, parent=estilos["Normal"])
#         encabezadoNombre = Paragraph(
#             "Estimación de Densidad de Multitudes de Personas a través de Visión por Computador", estilos["Normal"])
#         _, altura = encabezadoNombre.wrap(archivoPDF.width, archivoPDF.topMargin)
#         encabezadoNombre.drawOn(canva, archivoPDF.leftMargin, 736)
#         FechaConsulta = utcnow().to("local").format("dddd, DD  MMMM  YYYY", locale="es")
#         Hora = strftime("%H:%M:%S")
#         encabezadoFecha = Paragraph(FechaConsulta + " a las " + Hora, alineacion)
#         _, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
#         encabezadoFecha.drawOn(canva, archivoPDF.leftMargin, 725)
#         piePagina = Paragraph("Reporte generado automáticamente.", estilos["Normal"])
#         _, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
#         piePagina.drawOn(canva, archivoPDF.leftMargin, 15 * mm + (0.2 * inch))
#         canva.restoreState()
#
#     def convertirDatos(self):
#         estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_CENTER, fontSize=7, textColor=white,
#                                           fontName="Helvetica-Bold", parent=self.estilos["Normal"])
#         estiloNormal = self.estilos["Normal"]
#         estiloNormal.alignment = TA_CENTER
#         estiloNormal.fontSize = 7
#         claves, nombres = zip(*[[k, n] for k, n in self.cabecera])
#         encabezado = [Paragraph(nombre, estiloEncabezado) for nombre in nombres]
#         nuevosDatos = [tuple(encabezado)]
#         for dato in self.datos:
#             nuevosDatos.append([Paragraph(str(dato[clave]), estiloNormal) for clave in claves])
#         return nuevosDatos
#
#     def Exportar(self):
#         alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13, leading=10,
#                                           textColor=purple, parent=self.estilos["Heading1"])
#         self.ancho, self.alto = letter
#         convertirDatos = self.convertirDatos()
#         tabla = Table(convertirDatos, colWidths=(self.ancho - 100) / len(self.cabecera), hAlign="CENTER")
#         tabla.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), purple), ("ALIGN", (0, 0), (0, -1), "LEFT"),
#                                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("INNERGRID", (0, 0), (-1, -1), 0.50, black),
#                                    ("BOX", (0, 0), (-1, -1), 0.25, black), ]))
#         historia = [Paragraph(self.titulo, alineacionTitulo), Spacer(1, 0.16 * inch), tabla]
#         archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
#                                        title="Reporte de Consultas", author="Daniel Zambrano")
#         try:
#             archivoPDF.build(historia, onFirstPage=self._encabezadoPiePagina, onLaterPages=self._encabezadoPiePagina,
#                              canvasmaker=numeracionPaginas)
#         except PermissionError:
#             self.errorPDF()
#
#     def errorPDF(self):
#         messageBox = QMessageBox(self)
#         messageBox.setWindowTitle("Error")
#         messageBox.setIcon(QMessageBox.Critical)
#         messageBox.setWindowIcon(QIcon("Recursos/Error.png"))
#         messageBox.setText("Archivo PDF no generado.")
#         Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#         messageBox.setDefaultButton(Si)
#         messageBox.exec_()
#
#
# class numeracionPaginas(canvas.Canvas):
#     def __init__(self, *args, **kwargs):
#         canvas.Canvas.__init__(self, *args, **kwargs)
#         self._saved_page_states = []
#
#     def showPage(self):
#         self._saved_page_states.append(dict(self.__dict__))
#         self._startPage()
#
#     def save(self):
#         numeroPaginas = len(self._saved_page_states)
#         for state in self._saved_page_states:
#             self.__dict__.update(state)
#             self.draw_page_number(numeroPaginas)
#             canvas.Canvas.showPage(self)
#         canvas.Canvas.save(self)
#
#     def draw_page_number(self, conteoPaginas):
#         self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
#                              "Página {} de {}".format(self._pageNumber, conteoPaginas))
#
#
# def pdf():
#     try:
#         def dict_factory(canv, row):
#             d = {}
#             for idx, col in enumerate(canv.description):
#                 d[col[0]] = row[idx]
#             return d
#
#         conn = sqlite3.connect("Database/Consultas.db")
#         conn.row_factory = dict_factory
#         c = conn.cursor()
#         c.execute(
#             "SELECT ImagenOriginal, Aproximacion, Zona, Modelo, Fecha, Year, MapaDeDensidad, ImagenBinaria,ImagenNumerada, ImagenContorno, MapaCV2, Ruta FROM historial")
#         datos = c.fetchall()
#         conn.commit()
#         c.close()
#         conn.close()
#         reportePDF(datos).Exportar()
#     except (ValueError, Exception):
#         pass
#
#
# def sqliteExcel():
#     try:
#         FechaConsulta = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
#         fechaReporte = FechaConsulta.replace("-", "de")
#         Hora = strftime("%H:%M:%S")
#         celdaConteo = 2
#         celdaZonas = 3
#         n = 3
#         m = 4
#         workbook = Workbook('Reportes/Reporte de Consultas.xlsx')
#         worksheet = workbook.add_worksheet("Base de Datos")
#         alineacion = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
#         numbersformat = workbook.add_format({'num_format': '#,##0', 'align': 'center', 'valign': 'vcenter'})
#         font = workbook.add_format()
#         font.set_font_size(26)
#         font2 = workbook.add_format()
#         font2.set_font_size(12)
#         conn = sqlite3.connect("Database/Consultas.db")
#         c = conn.cursor()
#         c.execute("SELECT * FROM historial")
#         mysel = c.execute("SELECT * FROM historial ")
#         connection = sqlite3.connect("Database/Consultas.db")
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM historial")
#         recuento = (len(cursor.fetchall()))
#         margenTabla = "A" + str(n) + ":" "M" + str(recuento + m)
#         titulo = 'Estimación de Densidad de Personas a través de Visión por Computador'
#         subtitulo = 'Reporte generado automáticamente el dia '
#         worksheet.merge_range('A1:M1', "")
#         worksheet.merge_range('A2:M2', "")
#         worksheet.freeze_panes(3, 2)
#         worksheet.write('A1:M1', titulo, font)
#         worksheet.write('A2:M2', subtitulo + fechaReporte + " a las " + Hora, font2)
#         worksheet.set_column('A:A', 25, alineacion)
#         worksheet.set_column('B:B', 25, alineacion)
#         worksheet.set_column('C:C', 25, alineacion)
#         worksheet.set_column('D:D', 35, alineacion)
#         worksheet.set_column('E:E', 25, alineacion)
#         worksheet.set_column('F:F', 25, alineacion)
#         worksheet.set_column('G:G', 25, alineacion)
#         worksheet.set_column('H:H', 35, alineacion)
#         worksheet.set_column('I:I', 35, alineacion)
#         worksheet.set_column('J:J', 35, alineacion)
#         worksheet.set_column('K:K', 35, alineacion)
#         worksheet.set_column('L:L', 35, alineacion)
#         worksheet.set_column('M:M', 100, alineacion)
#         worksheet.add_table(margenTabla,
#                             {'total_row': 1, 'columns': [{'total_string': 'Total', 'header': 'No. Consulta'},
#                                                          {'header': 'Nombre de la Imagen',
#                                                           'total_function': 'count',
#                                                           'format': numbersformat},
#                                                          {'header': 'Conteo de Personas',
#                                                           'total_function': 'sum',
#                                                           'format': numbersformat},
#                                                          {'header': 'Zonas con Aglomeraciones',
#                                                           'total_function': 'sum',
#                                                           'format': numbersformat},
#                                                          {'header': 'Modelo Seleccionado'},
#                                                          {'header': 'Hora'}, {'header': 'Fecha'},
#                                                          {'header': 'Nombre de Mapa de Densidad'},
#                                                          {'header': 'Nombre de Imagen Binaria'},
#                                                          {'header': 'Nombre de Imagen Numerada'},
#                                                          {'header': 'Nombre de Imagen con Contorno'},
#                                                          {'header': 'Nombre de Mapa de Calor CV2'},
#                                                          {'header': 'Ruta de Almacenamiento'}, ]})
#         for i, row in enumerate(mysel):
#             for j, value in enumerate(row):
#                 if j == celdaConteo or j == celdaZonas:
#                     worksheet.write(i + n, j, int(value))
#                 else:
#                     worksheet.write(i + n, j, value)
#         workbook.close()
#     except (ValueError, Exception):
#         errorExportar()
#
#
# def errorExportar():
#     messageBox = QMessageBox()
#     messageBox.setWindowTitle("Error")
#     messageBox.setIcon(QMessageBox.Warning)
#     messageBox.setWindowIcon(QIcon("Recursos/database.png"))
#     messageBox.setText("Cierre el archivo anteriormente exportado.")
#     Si = messageBox.addButton("Aceptar", QMessageBox.AcceptRole)
#     messageBox.setDefaultButton(Si)
#     messageBox.exec_()
#
#
# class Ayuda(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(Ayuda, self).__init__(*args, **kwargs)
#         loadUi('Ayuda.ui', self)
#         self.setWindowFlags(
#             QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#         self.setWindowIcon(QIcon("Recursos/ayuda.png"))
#
#
# class HyperlinkLabel(QLabel):
#     def __init__(self, parent=None):
#         super().__init__()
#         self.setOpenExternalLinks(True)
#         self.setParent(parent)
#
#
# class VerificacionGPU(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(VerificacionGPU, self).__init__(*args, **kwargs)
#         global use_cuda
#         self.setWindowFlags(
#             QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#         self.setFixedWidth(460)
#         self.setFixedHeight(250)
#         self.setWindowIcon(QIcon("Recursos/NVIDIA.png"))
#         QBtn = QDialogButtonBox.Ok
#         self.buttonBox = QDialogButtonBox(QBtn)
#         self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)
#         QBtn2 = QDialogButtonBox.Cancel
#         self.buttonBox2 = QDialogButtonBox(QBtn2)
#         self.buttonBox2.accepted.connect(self.accept)
#         self.buttonBox2.rejected.connect(self.reject)
#         self.button = QPushButton('Omitir')
#         self.button.setFixedWidth(100)
#         self.button.setFixedHeight(25)
#         self.button.setDefault(False)
#         self.button1 = QPushButton('Salir')
#         self.button1.setFixedWidth(100)
#         self.button1.setFixedHeight(25)
#         self.button1.setDefault(True)
#         layout = QGridLayout()
#         self.setWindowTitle("CUDA")
#         title = QLabel("Verificación CUDA")
#         font = title.font()
#         font.setPointSize(15)
#         title.setFont(font)
#         label2 = QLabel(self)
#         pixmap2 = QPixmap('Recursos/Blanco.png')
#         label2.setPixmap(pixmap2)
#         label2.resize(pixmap2.width(), pixmap2.height())
#         label = QLabel(self)
#         pixmap = QPixmap('Recursos/NVIDIA.png')
#         label.setPixmap(pixmap)
#         label.setOpenExternalLinks(True)
#         label.setScaledContents(True)
#         label.resize(120, 120)
#         label.move(325, 15)
#         layout.addWidget(title)
#         if use_cuda:
#             device = (torch.cuda.current_device())
#             nameDevice = torch.cuda.get_device_name(device)
#             memoria = torch.cuda.get_device_properties(device).total_memory / (1024 ** 2)
#             layout.addWidget(QLabel("CUDA DISPONIBLE"))
#             layout.addWidget(QLabel("Tarjeta: " + str(nameDevice)))
#             layout.addWidget(QLabel("Memoria Total: " + str(memoria)))
#             layout.addWidget(QLabel("Dispositivo: " + str(device)))
#             layout.addWidget(self.buttonBox)
#             self.setLayout(layout)
#         else:
#             linkTemplate = 'Instale los drivers de <a href= https://la.nvidia.com/Download/index.aspx?lang=la>NVIDIA</a> y <a href=https://developer.nvidia.com/cuda-downloads>CUDA</a>.'
#             label1 = HyperlinkLabel(self)
#             label1.setText(linkTemplate.format())
#             layout.addWidget(QLabel())
#             layout.addWidget(QLabel())
#             layout.addWidget(label1, 5, 0)
#             layout.addWidget(self.button, 5, 5)
#             layout.addWidget(self.button1, 6, 5)
#             layout.addWidget(QLabel("Verifique la disponibilidad de una tarjeta NVIDIA."), 4, 0)
#             layout.addWidget(QLabel("CUDA NO DISPONIBLE"), 2, 0)
#             self.setLayout(layout)
#
#
# class AboutDialog(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(AboutDialog, self).__init__(*args, **kwargs)
#         self.setWindowFlags(
#             QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#         self.setFixedWidth(460)
#         self.setFixedHeight(250)
#         self.setWindowIcon(QIcon("Recursos/Yo.png"))
#         QBtn = QDialogButtonBox.Ok
#         self.buttonBox = QDialogButtonBox(QBtn)
#         self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)
#         layout = QVBoxLayout()
#         self.setWindowTitle("Créditos")
#         title = QLabel("Universidad Técnica del Norte")
#         font = title.font()
#         font.setPointSize(20)
#         title.setFont(font)
#         label2 = QLabel(self)
#         pixmap2 = QPixmap('Recursos/Blanco.png')
#         label2.setPixmap(pixmap2)
#         label2.setScaledContents(True)
#         label2.resize(pixmap2.width(), pixmap2.height())
#         label = QLabel(self)
#         pixmap = QPixmap('Recursos/Yo.png')
#         label.setPixmap(pixmap)
#         label.setScaledContents(True)
#         label.resize(120, 120)
#         label.move(335, 80)
#         layout.addWidget(title)
#         layout.addWidget(QLabel("Estimación de Densidad de Personas a través de Visión por Computador"))
#         layout.addWidget(QLabel("Versión: 1.0"))
#         layout.addWidget(QLabel("Autor: Daniel David Zambrano Andrade"))
#         layout.addWidget(QLabel("Correo: ddzambranoa@utn.edu.ec"))
#         layout.addWidget(QLabel("Año: 2021"))
#         layout.addWidget(self.buttonBox)
#         self.setLayout(layout)
#
#
# stylesheet = """
# QScrollArea > QWidget > QWidget
# {
#     background: none;
#     border: 0px;
#     margin: 0px 0px 0px 0px;
# }
#
#  QScrollBar:vertical
#  {
#      background-color: #2A2929;
#      width: 15px;
#      margin: 15px 3px 15px 3px;
#      border: 1px transparent #2A2929;
#      border-radius: 4px;
#  }
#  QScrollBar::handle:vertical
#  {
#      background-color: BLACK;
#      min-height: 5px;
#      border-radius: 4px;
#  }
#  QScrollBar::sub-line:vertical
#  {
#      margin: 3px 0px 3px 0px;
#      border-image: url(Recursos/arrow_up.jpg);
#      height: 10px;
#      width: 10px;
#      subcontrol-position: top;
#      subcontrol-origin: margin;
#  }
#  QScrollBar::add-line:vertical
#  {
#      margin: 3px 0px 3px 0px;
#      border-image: url(Recursos/arrow_down.jpg);
#      height: 10px;
#      width: 10px;
#      subcontrol-position: bottom;
#      subcontrol-origin: margin;
#  }
#  QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
#  {
#      border-image: url(Recursos/arrow_up.jpg);
#      height: 10px;
#      width: 10px;
#      subcontrol-position: top;
#      subcontrol-origin: margin;
#  }
#  QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
#  {
#      border-image: url(Recursos/arrow_down.jpg);
#      height: 10px;
#      width: 10px;
#      subcontrol-position: bottom;
#      subcontrol-origin: margin;
#  }
#  QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
#  {
#      background: none;
#      border-radius: 4px;
#      min-height: 5px;
#  }
#  QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
#  {
#      background: none;
#      border-radius: 4px;
#      min-height: 5px;
#  }
# """
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyleSheet(stylesheet)
#     main = SplashScreen()
#     main.show()
#     sys.exit(app.exec_())
