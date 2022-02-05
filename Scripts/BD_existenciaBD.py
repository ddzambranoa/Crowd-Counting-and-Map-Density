import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from Scripts.BD_exportarExcel import ExportEXCEL
from Scripts.BD_exportarPDF import ExportPDF
from Scripts.cuadrosDialogos import *

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
interfaz_ayuda = os.path.join(path, r'Interfaz/Ayuda.ui')
dbConsultas = os.path.join(path, r'Database/Consultas.db')
archExcel = os.path.join(path, r'Reportes/Reporte de Consultas.xlsx')
archPDF = os.path.join(path, r'Reportes/Reporte de Consultas.pdf')


def ExportarDatos():
    try:
        with sqlite3.connect(dbConsultas) as db:
            cursor = db.cursor()
            cursor.execute('''SELECT COUNT(*) from historial ''')
            result = cursor.fetchall()
            if result[0][0] == 0:
                pass
            else:
                ExportPDF()
                ExportEXCEL()
    except (ValueError, Exception):
        pass


def abrirPDF():
    try:
        with sqlite3.connect(dbConsultas) as db:
            c = db.cursor()
            c.execute('''SELECT COUNT(*) from historial ''')
            comprobacion = c.fetchall()
            if comprobacion[0][0] == 0:
                pass
            else:
                try:
                    subprocess.Popen([archPDF], shell=True)
                    open(archPDF, "r+")
                except (ValueError, Exception):
                    error_export_pdf()
    except (ValueError, Exception):
        print("1")


def abrirExcel():
    try:
        with sqlite3.connect(dbConsultas) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT COUNT(*) from historial ''')
            check = cursor.fetchall()
            if check[0][0] == 0:
                pass
            else:
                try:
                    os.startfile(archExcel)
                    open(archExcel, "r+")
                except (IOError, ValueError, Exception):
                    error_export_xlsx()
    except (ValueError, Exception):
        print("2")
