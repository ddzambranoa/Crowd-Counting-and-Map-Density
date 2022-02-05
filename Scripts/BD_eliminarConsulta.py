import os
import sqlite3
import sys
from pathlib import Path
from shutil import rmtree
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QPushButton, QDialog
from Scripts.BD_exportarPDF import ExportPDF
from Scripts.BD_exportarExcel import ExportEXCEL
from Scripts.cuadrosDialogos import *

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
imgEliminar = os.path.join(path, r'Recursos/d1.png')
dbConsultas = os.path.join(path, r'Database/Consultas.db')
imgDatabase = os.path.join(path, r'Recursos/database.png')


class eliminarConsulta(QDialog):
    def __init__(self, *args, **kwargs):
        super(eliminarConsulta, self).__init__(*args, **kwargs)
        self.conn = ""
        self.c = ""
        self.serachresultdel = ""
        self.QBtn = QPushButton()
        self.QBtn.setText('Eliminar')
        self.setWindowTitle("Eliminar consulta")
        self.setWindowIcon(QIcon(imgEliminar))
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deleteconsulta)
        layout = QVBoxLayout()
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("No. Consulta")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deleteconsulta(self):
        delrol = self.deleteinput.text()
        self.close()
        try:
            self.conn = sqlite3.connect(dbConsultas)
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT * from historial WHERE roll =" + str(delrol))
            row = result.fetchone()
            rmtree(str(row[12]))
            self.c.execute("DELETE from historial WHERE roll=" + str(delrol))
            self.conn.commit()
            ExportPDF()
            ExportEXCEL()
            self.c.close()
            self.conn.close()
            confirmacionEliminacion()
            self.close()
        except (ValueError, Exception):
            errorEliminacion()
