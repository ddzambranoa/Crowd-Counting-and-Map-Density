# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# ----------------------------------------------------------------------------
# Nombre:       InterfazGrafica.py
# Autor:        Daniel David Zambrano Andrade
# Creado:       15 de Septiembre 2020
# Modificado:   03 de Abril 2021
# Copyright:    Libre
# License:      Libre
# ----------------------------------------------------------------------------

import cv2
import sys
from time import strftime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDesktopWidget, QTableWidget, QToolBar, \
    QStatusBar, QAction, QTableWidgetItem, QDialogButtonBox, QDialog, QVBoxLayout, QLineEdit, QPushButton, \
    QHeaderView, QAbstractItemView
from PyQt5.uic import *
from PyQt5.QtGui import QPixmap, QIcon, QTextDocument, QTextCursor, QIntValidator
import PIL.Image as Image
import numpy as np
from PyQt5.QtCore import *
from skimage.transform import rescale
from model import CSRNet
import torch
from torchvision import transforms
from matplotlib import pyplot as plt
import sqlite3
import os
from arrow import utcnow
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas
import locale
from shutil import rmtree

global fecha
locale.setlocale(locale.LC_ALL, 'es_EC')


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('Interfaz.ui', self)
        self.BotonImagenes.clicked.connect(self.abrirVentanaImagenesConsulta)
        self.actionHistorial_de_Consultas.triggered.connect(self.historial)
        self.center()
        self.setFixedSize(1020, 720)

    def abrirVentanaImagenesConsulta(self):
        self.hide()
        VentanaImagenesConsulta(self)

    def closeEvent(self, event):
        messageBox = QMessageBox(self)
        messageBox.setWindowTitle("Salir")
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setText("¿Desea salir del programa?")
        Si = messageBox.addButton("Si", QMessageBox.YesRole)
        No = messageBox.addButton("No", QMessageBox.AcceptRole)
        messageBox.setDefaultButton(Si)
        messageBox.exec_()

        if messageBox.clickedButton() == Si:
            event.accept()
        elif messageBox.clickedButton() == No:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def historial(self):
        window = BaseDeDatos(self)
        window.show()
        window.loaddata()


class VentanaImagenesConsulta(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaImagenesConsulta, self).__init__(parent)
        self.ventana = loadUi("ImagenesConsulta.ui", self)
        self.get_image_file()
        self.base = ""
        self.name = ""
        self.nameFile = ""
        self.file = ""
        self.dir_F = ""
        self.conn = ""
        self.c = ""
        self.den = ""
        self.Rden = ""
        self.conteo = 0
        self.center()
        self.setFixedSize(1920, 1000)
        self.totalCnts = ""
        self.Zona = ""
        self.imagen_O = ""
        self.Img_O = ""
        self.Zona_N = ""
        self.Zona_B = ""
        self.Zona_C = ""
        self.imagen = ""
        self.imagen_2 = ""
        self.imagen_3 = ""
        self.IMG_CV2JET = ""
        self.Number_2.setStyleSheet("QLabel""{""color : #ffffff;""background : red;""}")
        self.Number.setStyleSheet("QLabel""{""color : #ffffff;" "}")

    def abrirVentanaPrincipal(self):
        self.parent().show()
        self.close()

    def get_image_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"", "Image files (*.jpg *.jpeg *.png)")
            self.name = os.path.abspath(file_name)
            self.ImagenOriginal.setPixmap(QPixmap(file_name))
            self.predecir()
            self.ventana.show()
        except (ValueError, Exception):
            self.abrirVentanaPrincipal()

    def predecir(self):
        try:
            global fecha
            fecha = strftime("%B-%d-%Y_%H_%M_%S")
            self.base = os.path.basename(self.name)
            self.file = os.path.splitext(self.base)[0]
            try:
                os.stat("Modelos Entrenados")
            except (ValueError, Exception):
                os.mkdir("Modelos Entrenados")
            # modeloentrenado = "Modelos Entrenados/Multitudes_Densas.pth.tar"
            modeloentrenado = 'Modelos Entrenados/Multitudes_Dispersas.pth.tar'
            # modeloentrenado = 'Modelos Entrenados/Multitudes_Densas-Dispersas.pth.tar'
            transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                                        std=[0.229, 0.224, 0.225]), ])
            model = CSRNet()
            model = model.cuda()
            checkpoint = torch.load(modeloentrenado)
            model.load_state_dict(checkpoint['state_dict'])
            img = transform(Image.open(self.name).convert('RGB')).cuda()
            output = model(img.unsqueeze(0))
            self.conteo = str(int(output.detach().cpu().sum().numpy()))
            MapaDensidad = np.asarray(
                output.detach().cpu().reshape(output.detach().cpu().shape[2], output.detach().cpu().shape[3]))
            ROOT_DIR = os.path.dirname(__file__)
            try:
                os.stat(ROOT_DIR + "/Mapas_De_Densidad/")
            except (ValueError, Exception):
                os.mkdir(ROOT_DIR + "/Mapas_De_Densidad/")
            self.dir_F = ROOT_DIR + "/Mapas_De_Densidad/" + str(str(self.file)) + "_" + str(fecha).capitalize()
            self.Rden = self.dir_F + "/" + str(str(self.file))
            self.den = self.Rden + "_Densidad" + ".png"
            os.mkdir(self.dir_F)
            MapaDensidad = rescale(MapaDensidad, 8, anti_aliasing=True)
            plt.imsave(self.den, MapaDensidad, cmap='jet', vmin=0, vmax=0.07)
            self.Number.setText(self.conteo)
            rojoBajo1 = np.array([0, 50, 20], np.uint8)
            rojoAlto1 = np.array([30, 255, 255], np.uint8)
            rojoBajo2 = np.array([150, 50, 20], np.uint8)
            rojoAlto2 = np.array([180, 255, 255], np.uint8)
            self.imagen = cv2.imread(self.den)
            self.imagen_2 = cv2.imread(self.den)
            self.imagen_O = cv2.imread(self.name)
            bordersize = 30
            self.imagen = cv2.copyMakeBorder(self.imagen, top=bordersize, bottom=bordersize, left=bordersize,
                                             right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[127, 0, 0])
            self.imagen_2 = cv2.copyMakeBorder(self.imagen_2, top=bordersize, bottom=bordersize, left=bordersize,
                                               right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[127, 0, 0])
            imagenHSV = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2HSV)
            maskRojo1 = cv2.inRange(imagenHSV, rojoBajo1, rojoAlto1)
            maskRojo2 = cv2.inRange(imagenHSV, rojoBajo2, rojoAlto2)
            maskRojo = cv2.add(maskRojo1, maskRojo2)
            contornosRojo = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            self.dibujarContorno(contornosRojo)
            self.totalCnts = len(contornosRojo)
            self.imagen_3 = cv2.applyColorMap(self.imagen_2, cv2.COLORMAP_JET)
            self.IMG_CV2JET = self.Rden + "_Mapa_Calor" + ".png"
            self.Img_O = self.Rden + ".png"
            self.Zona_N = self.Rden + "_Numerada" + ".png"
            self.Zona_C = self.Rden + "_Contorno" + ".png"
            self.Zona_B = self.Rden + "_Binaria" + ".png"
            cv2.imwrite(self.Zona_B, maskRojo)
            cv2.imwrite(self.Zona_N, self.imagen)
            cv2.imwrite(self.Zona_C, self.imagen_2)
            cv2.imwrite(self.Img_O, self.imagen_O)
            cv2.imwrite(self.IMG_CV2JET, self.imagen_3)
            self.MapaDeDensidad_2.setPixmap(QPixmap(self.Zona_C))
            self.Number_2.setText(str(self.totalCnts))
            self.AlmacenarDatos()
            pdf()
        except (ValueError, Exception):
            QMessageBox.warning(QMessageBox(), 'Error',
                                'Falla en el sistema, compruebe los datos de entrada y el modelo entrenado de la red neuronal convolucional.')
            self.ventana.show().quit()

    def dibujarContorno(self, contornos):
        for (i, c) in enumerate(contornos):
            M = cv2.moments(c)
            if M["m00"] != 0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
            else:
                x, y = 0, 0
            cv2.drawContours(self.imagen, [c], 0, (0, 0, 255), 2)
            cv2.drawContours(self.imagen_2, [c], 0, (0, 255, 255), 4)
            cv2.putText(self.imagen, str(i + 1), (x, y), 5, 1, (0, 0, 0), 2)

    def AlmacenarDatos(self):
        ImagenOriginal = os.path.basename(self.Img_O)
        Aproximacion = self.conteo
        Zona = self.totalCnts
        Fecha = strftime("%H:%M:%S")
        Year = strftime("%B %d, %Y").capitalize()
        MapaDeDensidad = os.path.basename(self.den)
        ImagenBinaria = os.path.basename(self.Zona_B)
        ImagenNumerada = os.path.basename(self.Zona_N)
        ImagenContorno = os.path.basename(self.Zona_C)
        MapaCV2 = os.path.basename(self.IMG_CV2JET)
        Ruta = self.dir_F
        try:
            try:
                os.stat("Database")
            except (ValueError, Exception):
                os.mkdir("Database")
            self.conn = sqlite3.connect("Database/Consultas.db")
            self.c = self.conn.cursor()
            self.c.execute(
                "CREATE TABLE IF NOT EXISTS historial(roll INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,ImagenOriginal TEXT,"
                "Aproximacion TEXT,Zona TEXT, Fecha TEXT, Year Text,  MapaDeDensidad TEXT, ImagenBinaria TEXT,ImagenNumerada TEXT, ImagenContorno TEXT, MapaCV2 TEXT, Ruta TEXT)")
            self.c.execute(
                "INSERT INTO historial (ImagenOriginal, Aproximacion, Zona, Fecha, Year,  MapaDeDensidad, ImagenBinaria,ImagenNumerada, ImagenContorno, MapaCV2, Ruta) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (ImagenOriginal, Aproximacion, Zona, Fecha, Year, MapaDeDensidad, ImagenBinaria, ImagenNumerada,
                 ImagenContorno, MapaCV2, Ruta))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            file = open(Ruta + "/Resumen.txt", "w")
            file.write("Nombre de la imagen: " + ImagenOriginal + os.linesep)
            file.write("Aproximación de Personas: " + str(Aproximacion) + os.linesep)
            file.write("Zonas de posibles aglomeraciones: " + str(Zona) + os.linesep)
            file.write("Hora de consulta: " + Fecha + os.linesep)
            file.write("Fecha de Consulta: " + Year + os.linesep)
            file.write("Nombre del mapa de densidad: " + MapaDeDensidad + os.linesep)
            file.write("Nombre de la imagen binaria: " + ImagenBinaria + os.linesep)
            file.write("Nombre de la imagen numerada: " + ImagenNumerada + os.linesep)
            file.write("Nombre de la imagen con contorno: " + ImagenContorno + os.linesep)
            file.write("Nombre del mapa de densidad de openCV: " + MapaCV2 + os.linesep)
            file.write("Ruta de la carpeta contenedora: " + Ruta + os.linesep)
            file.close()
            QMessageBox.information(QMessageBox(), 'Listo', 'Consulta agregada a historial.')
        except (ValueError, Exception):
            QMessageBox.warning(QMessageBox(), 'Error', 'Consulta no agregada a historial. Reinicie el programa.')

    def closeEvent(self, event):
        self.abrirVentanaPrincipal()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def pdf():
    try:
        def dict_factory(c, row):
            d = {}
            for idx, col in enumerate(c.description):
                d[col[0]] = row[idx]
            return d

        conn = sqlite3.connect("Database/Consultas.db")
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(
            "SELECT ImagenOriginal, Aproximacion, Zona, Fecha, Year, MapaDeDensidad, ImagenBinaria,ImagenNumerada, ImagenContorno, MapaCV2, Ruta FROM historial")
        datos = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        reporte = reportePDF(datos).Exportar()
        print(reporte)
    except (ValueError, Exception):
        pass


class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)
        self.conn = ""
        self.c = ""
        self.serachresult = ""
        self.QBtn = QPushButton()
        self.QBtn.setText("Detalles")
        self.setWindowTitle("Detalles de Consulta")
        self.setFixedWidth(500)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.buscarConsulta)
        layout = QVBoxLayout()
        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("No. Consulta")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def buscarConsulta(self):
        searchrol = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("Database/Consultas.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from historial WHERE roll =" + str(searchrol))
            row = result.fetchone()
            self.serachresult = "Consulta : " + str(row[0]) + '\n' + "Nombre : " + str(
                row[1]) + '\n' + "Aproximación : " + str(row[2]) + '\n' + "Zonas con Aglomeración : " + str(
                row[3]) + '\n' + "Hora de Consulta : " + \
                                str(row[4]) + '\n' + "Fecha de Consulta : " + str(row[5])
            img_o = str(row[11]) + "/" + str(row[1])
            img_d = str(row[11]) + "/" + str(row[6])
            img_b = str(row[11]) + "/" + str(row[7])
            img_n = str(row[11]) + "/" + str(row[8])
            img_c = str(row[11]) + "/" + str(row[9])
            img_mp = str(row[11]) + "/" + str(row[10])
            imagenMP = cv2.imread(img_mp)
            cv2.imshow('Imagen Mapa CV2', imagenMP)
            imagenN = cv2.imread(img_n)
            cv2.imshow('Imagen Numerada', imagenN)
            imagenC = cv2.imread(img_c)
            cv2.imshow('Imagen Contorno', imagenC)
            imagenB = cv2.imread(img_b)
            cv2.imshow('Imagen Binaria', imagenB)
            imagenMD = cv2.imread(img_d)
            cv2.imshow('Mapa de Densidad', imagenMD)
            imagenO = cv2.imread(img_o)
            cv2.imshow('Imagen Original', imagenO)
            QMessageBox.information(QMessageBox(), 'Consulta', self.serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except (ValueError, Exception):
            QMessageBox.warning(QMessageBox(), 'Error', 'Consulta no encontrada.')
            # QMessageBox.warning(QMessageBox(), 'Error', 'Consulta no encontrada.' + os.linesep + 'Actualice la base de datos')
            # QMessageBox.warning(QMessageBox(), 'Error', 'Imágenes no encontradas, asegúrese que la ruta de la imagen sea idéntica a la generada en el reporte en pdf.')


class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)
        self.conn = ""
        self.c = ""
        self.serachresultdel = ""
        self.QBtn = QPushButton()
        self.QBtn.setText('Borrar')
        self.setWindowTitle("Borrar Consulta")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deleteconsulta)
        layout = QVBoxLayout()
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("No. Consulta")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteconsulta(self):
        delrol = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("Database/Consultas.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from historial WHERE roll =" + str(delrol))
            row = result.fetchone()
            rmtree(str(row[11]))
            self.c.execute("DELETE from historial WHERE roll=" + str(delrol))
            self.conn.commit()
            pdf()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Listo',
                                    'Consulta eliminada de historial.' + os.linesep + 'Actualice la base de datos')
            self.close()
        except (ValueError, Exception):
            QMessageBox.warning(QMessageBox(), 'Error', 'Consulta no eliminada de historial.')


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.setFixedWidth(500)
        self.setFixedHeight(250)
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


class BaseDeDatos(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(BaseDeDatos, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon("Recursos/g2.png"))  # window icon
        self.connection = ""
        self.conn = sqlite3.connect("Database/Consultas.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS historial(roll INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,ImagenOriginal TEXT,"
            "Aproximacion TEXT,Zona TEXT, Fecha TEXT, Year Text, MapaDeDensidad TEXT, ImagenBinaria TEXT,ImagenNumerada TEXT, ImagenContorno TEXT, MapaCV2 TEXT, Ruta)")
        self.c.close()
        self.center()
        file_menu = self.menuBar().addMenu("&Archivos")
        self.setWindowTitle("Historial de Consultas")
        self.setMinimumSize(1320, 1000)
        self.setMaximumSize(1320, 1000)
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(11)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("No. Consulta", "Nombre de la Imagen", "No. Aproximado de personas",
                                                    "Zonas Posibles de Aglomeración", "Hora de Consulta",
                                                    "Fecha de Consulta",
                                                    "Mapa de Densidad", "Imagen Binaria",
                                                    "Imagen Numerada", "Imagen Contorno", "Mapa CV2", "Ruta"))
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for indice, ancho in enumerate((100, 300, 225, 225, 220, 220, 300, 300, 300, 300, 300), start=0):
            self.tableWidget.setColumnWidth(indice, ancho)
        self.tableWidget.setColumnHidden(6, True)
        self.tableWidget.setColumnHidden(7, True)
        self.tableWidget.setColumnHidden(8, True)
        self.tableWidget.setColumnHidden(9, True)
        self.tableWidget.setColumnHidden(10, True)
        self.tableWidget.setColumnHidden(11, True)
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        btn_ac_refresh = QAction(QIcon("Recursos/r3.png"), "Actualizar Reporte/Base de Datos", self)  # refresh icon
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)
        btn_ac_search = QAction(QIcon("Recursos/s1.png"), "Detalles", self)  # search icon
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User")
        toolbar.addAction(btn_ac_search)
        btn_ac_delete = QAction(QIcon("Recursos/d1.png"), "Borrar", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Borrar Consulta")
        toolbar.addAction(btn_ac_delete)
        searchuser_action = QAction(QIcon("Recursos/s1.png"), "Detalles", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)
        deluser_action = QAction(QIcon("Recursos/d1.png"), "Borrar", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

    def loaddata(self):
        self.connection = sqlite3.connect("Database/Consultas.db")
        query = "SELECT * FROM historial"
        pdf()
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignHCenter)
                self.tableWidget.setItem(row_number, column_number, item)
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    @staticmethod
    def delete():
        dlg = DeleteDialog()
        dlg.exec_()

    @staticmethod
    def search():
        dlg = SearchDialog()
        dlg.exec_()

    @staticmethod
    def about():
        dlg = AboutDialog()
        dlg.exec_()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)


class reportePDF(object):
    def __init__(self, datos):
        super(reportePDF, self).__init__()
        self.titulo = "REPORTE DE CONSULTAS"
        self.cabecera = (("ImagenOriginal", "Imagen Original"),
                         ("Aproximacion", "Aproximacion de Personas"),
                         ("Zona", "Zonas Posibles de Aglomeración"),
                         ("Fecha", "Hora"),
                         ("Year", "Fecha"),
                         ("MapaDeDensidad", "Mapa de Densidad"),
                         ("ImagenBinaria", "Imagen Binaria"),
                         ("ImagenNumerada", "Imagen Numerada"),
                         ("ImagenContorno", "Imagen Contorno"),
                         ("MapaCV2", "Mapa CV2"),
                         ("Ruta", "Ruta"))
        self.datos = datos
        try:
            os.stat("Reportes")
        except (ValueError, Exception):
            os.mkdir("Reportes")
        self.nombrePDF = "Reportes/Reporte de Consultas.pdf"
        self.estilos = getSampleStyleSheet()
        self.ancho = ""
        self.alto = ""

    @staticmethod
    def _encabezadoPiePagina(canvas, archivoPDF):
        canvas.saveState()
        estilos = getSampleStyleSheet()
        alineacion = ParagraphStyle(name="alineacion", alignment=TA_LEFT, parent=estilos["Normal"])
        encabezadoNombre = Paragraph(
            "Estimación de Densidad de Multitudes de Personas a través de Visión por Computador", estilos["Normal"])
        anchura, altura = encabezadoNombre.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoNombre.drawOn(canvas, archivoPDF.leftMargin, 736)
        fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
        fechaReporte = fecha.replace("-", "de")
        encabezadoFecha = Paragraph(fechaReporte, alineacion)
        anchura, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoFecha.drawOn(canvas, archivoPDF.leftMargin, 725)
        piePagina = Paragraph("Reporte generado por Daniel Zambrano.", estilos["Normal"])
        anchura, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
        piePagina.drawOn(canvas, archivoPDF.leftMargin, 15 * mm + (0.2 * inch))
        canvas.restoreState()

    def convertirDatos(self):
        estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_CENTER,
                                          fontSize=7, textColor=white,
                                          fontName="Helvetica-Bold",
                                          parent=self.estilos["Normal"])

        estiloNormal = self.estilos["Normal"]
        estiloNormal.alignment = TA_CENTER
        estiloNormal.fontSize = 7
        claves, nombres = zip(*[[k, n] for k, n in self.cabecera])
        encabezado = [Paragraph(nombre, estiloEncabezado) for nombre in nombres]
        nuevosDatos = [tuple(encabezado)]
        for dato in self.datos:
            nuevosDatos.append([Paragraph(str(dato[clave]), estiloNormal) for clave in claves])
        return nuevosDatos

    def Exportar(self):
        alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13,
                                          leading=10, textColor=purple,
                                          parent=self.estilos["Heading1"])
        self.ancho, self.alto = letter
        convertirDatos = self.convertirDatos()
        tabla = Table(convertirDatos, colWidths=(self.ancho - 100) / len(self.cabecera), hAlign="CENTER")
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), purple),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black),
            ("BOX", (0, 0), (-1, -1), 0.25, black),
        ]))
        historia = [Paragraph(self.titulo, alineacionTitulo), Spacer(1, 0.16 * inch), tabla]
        archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Reporte de Consultas", author="Daniel Zambrano")
        try:
            archivoPDF.build(historia, onFirstPage=self._encabezadoPiePagina,
                             onLaterPages=self._encabezadoPiePagina,
                             canvasmaker=numeracionPaginas)
            return "Reporte generado con éxito."
        except PermissionError:
            return "Error inesperado: Permiso denegado."


class numeracionPaginas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        numeroPaginas = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(numeroPaginas)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, conteoPaginas):
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                             "Página {} de {}".format(self._pageNumber, conteoPaginas))


app = QApplication(sys.argv)
main = VentanaPrincipal()
main.show()
sys.exit(app.exec_())
