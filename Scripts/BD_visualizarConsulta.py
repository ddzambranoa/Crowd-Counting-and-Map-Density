import os
import sqlite3
import sys
from pathlib import Path
import cv2
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QMessageBox, QDialog, QPushButton, QVBoxLayout, QLineEdit
from Scripts.cuadrosDialogos import error_visualizacion

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

imgVisualizar = os.path.join(path, r'Recursos/visualizar3.png')
dbConsultas = os.path.join(path, r'Database/Consultas.db')
imgDatabase = os.path.join(path, r'Recursos/database.png')


class visualizarConsulta(QDialog):
    def __init__(self, *args, **kwargs):
        super(visualizarConsulta, self).__init__(*args, **kwargs)
        self.con = ""
        self.c = ""
        self.serachresult = ""
        self.QBtn = QPushButton()
        self.QBtn.setText("Visualizar")
        self.setWindowTitle("Visualizar Consulta")
        self.setWindowIcon(QIcon(imgVisualizar))
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.buscarConsulta)
        layout = QVBoxLayout()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("No. Consulta")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def buscarConsulta(self):
        searchrol = self.searchinput.text()
        self.close()
        try:
            self.con = sqlite3.connect(dbConsultas)
            self.c = self.con.cursor()
            result = self.c.execute("SELECT * from historial WHERE roll =" + str(searchrol))
            row = result.fetchone()
            self.serachresult = "Consulta: " + str(row[0]) + '\n' + "Nombre: " + str(
                row[1]) + '\n' + "Aproximación: " + str(row[2]) + '\n' + "Zonas con Aglomeración: " + str(
                row[3]) + '\n' + "Modelo: " + str(row[4]) + '\n' + "Hora de Consulta: " + str(
                row[5]) + '\n' + "Fecha de Consulta: " + str(row[6])
            img_o = str(row[12]) + "/" + str(row[1])
            img_d = str(row[12]) + "/" + str(row[7])
            img_b = str(row[12]) + "/" + str(row[8])
            img_n = str(row[12]) + "/" + str(row[9])
            img_c = str(row[12]) + "/" + str(row[10])
            img_mp = str(row[12]) + "/" + str(row[11])
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
            self.visualizar()
            self.con.commit()
            self.c.close()
            self.con.close()
        except (ValueError, Exception):
            error_visualizacion()

    def visualizar(self):
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle("Visualización de Imágenes")
        messagebox.setIcon(QMessageBox.Information)
        messagebox.setWindowIcon(QIcon(imgDatabase))
        messagebox.setText(self.serachresult)
        aceptar = messagebox.addButton("Aceptar", QMessageBox.AcceptRole)
        messagebox.setDefaultButton(aceptar)
        messagebox.exec_()
