import os
import sqlite3
import sys
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from Scripts.BD_exportarExcel import ExportEXCEL
from Scripts.BD_exportarPDF import ExportPDF

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
dbConsultas = os.path.join(path, r'Database/Consultas.db')


def actualizar_tabla(self):
    self.conexion = sqlite3.connect(dbConsultas)
    query = "SELECT * FROM historial"
    ExportPDF()
    ExportEXCEL()
    r = self.conexion.execute(query)
    self.tableWidget.setRowCount(0)
    for nFilas, dFilas in enumerate(r):
        self.tableWidget.insertRow(nFilas)
        for nColumnas, datos in enumerate(dFilas):
            item = QTableWidgetItem(str(datos))
            item.setTextAlignment(Qt.AlignHCenter)
            self.tableWidget.setItem(nFilas, nColumnas, item)
    self.conexion.close()
