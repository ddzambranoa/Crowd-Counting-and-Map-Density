# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Nombre:       InterfazGráfica.py
# Autor:        Daniel David Zambrano Andrade
# Creado:       15 de Septiembre 2020
# Modificado:   23 de Febrero 2021
# Copyright:    Libre
# License:      Libre
# ----------------------------------------------------------------------------

# Versión Python: 3.8

import sys
from time import strftime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDesktopWidget, QTableWidget, QToolBar, \
    QStatusBar, QAction, QTableWidgetItem, QDialogButtonBox, QDialog, QVBoxLayout, QLineEdit, QPushButton, QHeaderView, \
    QAbstractItemView
from PyQt5.uic import *
from PyQt5.QtGui import QPixmap, QIcon, QTextDocument, QTextCursor, QIntValidator
import PIL.Image as Image
import numpy as np
from skimage.transform import rescale

from model import CSRNet
import torch
from torchvision import transforms
import os
from matplotlib import pyplot as plt
import sqlite3

global fecha


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('Interfaz.ui', self)
        self.BotonImagenes.clicked.connect(self.abrirVentanaImagenesConsulta)
        self.actionHistorial_de_Consultas.triggered.connect(self.historial)
        self.center()
        self.setFixedSize(800, 700)

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
        self.ventana = loadUi('ImagenesConsulta.ui', self)
        self.get_image_file()
        self.name = ""
        self.nameFile = ""
        self.file = ""
        self.conn = ""
        self.c = ""
        self.den = ""
        self.conteo = 0
        self.fecha = strftime("%Y-%m-%d-%H:%M:%S")
        self.center()
        self.setFixedSize(1200, 800)

    def abrirVentanaPrincipal(self):
        self.parent().show()
        self.close()

    def get_image_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>",
                                                       "Image files (*.jpg *.jpeg *.png)")
            self.name = os.path.abspath(file_name)
            self.ImagenOriginal.setPixmap(QPixmap(file_name))
            self.predecir()
            self.ventana.show()
        except (ValueError, Exception):
            self.abrirVentanaPrincipal()

    def predecir(self):
        global fecha
        fecha = strftime("%Y-%m-%d-%H:%M:%S")
        base = os.path.basename(self.name)
        self.file = os.path.splitext(base)[0]
        modeloentrenado = 'Modelos Entrenados/Multitudes_Densas.pth.tar'
        # modeloentrenado = 'Modelos Entrenados/Multitudes_Dispersas.pth.tar'
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
        MapaDensidad = np.asarray(output.detach().cpu().reshape(output.detach().cpu().shape[2], output.detach().cpu().shape[3]))
        pathMD = '/Mapas de Densidad/Imágenes/'
        ROOT_DIR = os.path.dirname(__file__)
        self.den = ROOT_DIR + pathMD + str(str(self.file) + "_" + str(fecha) + ".png")
        MapaDensidad = rescale(MapaDensidad, 8, anti_aliasing=True)
        plt.imsave(self.den, MapaDensidad, cmap='jet')
        plt.imshow(MapaDensidad, cmap='jet')
        self.Number.setText(self.conteo)
        self.MapaDeDensidad.setPixmap(QPixmap(self.den))
        self.AlmacenarDatos()

    def AlmacenarDatos(self):
        Nombre = self.file
        Aproximacion = self.conteo
        Fecha = strftime("%Y-%m-%d-%H:%M:%S")
        MapaDeDensidad = self.den
        ImagenOriginal = self.name
        try:
            self.conn = sqlite3.connect("Database/Consultas.db")
            self.c = self.conn.cursor()
            self.c.execute(
                "INSERT INTO historial (Nombre,Aproximacion,Fecha,MapaDeDensidad,ImagenOriginal) VALUES (?,?,?,?,?)",
                (Nombre, Aproximacion, Fecha, MapaDeDensidad, ImagenOriginal))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Listo', 'Consulta agregada a historial.')
        except (ValueError, Exception):
            QMessageBox.warning(QMessageBox(), 'Error', 'Consulta no agregada a historial.')

    def closeEvent(self, event):
        self.abrirVentanaPrincipal()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)
        self.conn = ""
        self.c = ""
        self.QBtn = QPushButton()
        self.QBtn.setText("Detalles")

        self.setWindowTitle("Detalles de Consulta")
        self.setFixedWidth(300)
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
            serachresult = "Consulta : " + str(row[0]) + '\n' + "Nombre : " + str(
                row[1]) + '\n' + "Aproximación : " + str(
                row[2]) + '\n' + "Fecha : " + str(row[3]) + '\n' + "Mapa de Densidad : " + str(
                row[4]) + '\n' + "Imagen : " + str(row[5])
            QMessageBox.information(QMessageBox(), 'Listo', serachresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except (ValueError, Exception):
            QMessageBox.warning(QMessageBox(), 'Error', 'Consulta no encontrada.')


class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)
        self.conn = ""
        self.c = ""
        self.QBtn = QPushButton()
        self.QBtn.setText('Borrar')

        self.setWindowTitle("Borrar Consulta")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("No. Consulta")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):
        delrol = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("Database/Consultas.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from historial WHERE roll=" + str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Listo', 'Consulta eliminada de historial.')
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
        # self.setWindowTitle("Sobre")


class BaseDeDatos(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(BaseDeDatos, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('Recursos/g2.png'))  # window icon
        self.connection = ""

        self.conn = sqlite3.connect("Database/Consultas.db")
        self.c = self.conn.cursor()
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS historial(roll INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,Nombre TEXT,Aproximacion TEXT,Fecha TEXT,MapaDeDensidad TEXT,ImagenOriginal TEXT)")
        self.c.close()
        self.center()

        file_menu = self.menuBar().addMenu("&Archivos")

        # help_menu = self.menuBar().addMenu("&Sobre")
        self.setWindowTitle("Historial de Consultas")
        self.setMinimumSize(753, 800)
        self.setMaximumSize(753, 800)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("No. Consulta", "Nombre de la Imagen", "No. Aproximado de personas",
                                                    "Fecha de Consulta", "Mapa de Densidad", "Imagen Original"))
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for indice, ancho in enumerate((100, 250, 250, 150, 300, 300), start=0):
            self.tableWidget.setColumnWidth(indice, ancho)
        self.tableWidget.setColumnHidden(4, True)
        self.tableWidget.setColumnHidden(5, True)
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_refresh = QAction(QIcon("Recursos/r3.png"), "Actualizar", self)  # refresh icon
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

        # about_action = QAction(QIcon("Recursos/i1.png"), "Sobre", self)  # info icon
        # about_action.triggered.connect(self.about)
        # help_menu.addAction(about_action)

    def loaddata(self):
        self.connection = sqlite3.connect("Database/Consultas.db")
        query = "SELECT * FROM historial"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
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


app = QApplication(sys.argv)
main = VentanaPrincipal()
main.show()
sys.exit(app.exec_())
