# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import os
import sys
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDesktopWidget
from qtpy.uic import loadUi
from Scripts.BD_crearContenedores import cambiarNombre
from Scripts.Procesamiento import procesar
from Scripts.cuadrosDialogos import close_event
from Scripts.setup import centrar_ventana

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
intResultados = os.path.join(path, r'Interfaz/InterfazResultados.ui')
dbConsultas = os.path.join(path, r'Database/Consultas.db')
imgFondo = os.path.join(path, r'Recursos/Blanco')
imgDatabase = os.path.join(path, r'Recursos/database.png')
imgSubir = os.path.join(path, r'Recursos/upload.png')
carpDB = os.path.join(path, r'Database/')
imgExit = os.path.join(path, r'Recursos/exit.png')


class VisualizarResultados(QMainWindow):
    def __init__(self, multitud=None, parent=None):
        super().__init__(parent)
        self.ventana = loadUi(intResultados, self)
        centrar_ventana(self.ventana)
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.name = ""
        self.setFixedSize(1800, 900)
        self.multitudes = multitud
        self.get_image_file()

    def get_image_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Subir Imagen', r"",
                                                       filter='Todos los archivos de imagen (*.jpg *.jpeg *.png '
                                                              '*.tiff *.webp *.bmp *.odd)\n'
                                                              'PNG (*.png)\n' 'JPEG (*.jpeg *.jpe *.jfif)\n' 'JPG ('
                                                              '*.jpg)\n' "TIFF ( *.tif *.tiff)\n "
                                                              "WEBP (*.webp)\n" "Mapa de bits (*.bmp)\n" "ODD (*.odd)")
            # GIF, ICO, EPS, PS, PSD NO FUNCIONA
            path_file = str(Path(Path(file_name).parent.absolute()))
            sys.path.insert(0, path_file)
            nuevo_nombre = cambiarNombre(path_file, file_name)
            base = os.path.basename(nuevo_nombre)
            file = os.path.splitext(base)[0]
            if file_name != "":
                calcular = procesar(base, self.multitudes, file)
                self.ImagenOriginal.setPixmap(QPixmap(nuevo_nombre))
                self.MapaDeDensidad_2.setPixmap(QPixmap(calcular[0]))
                self.Number.setText(calcular[1])
                self.ventana.show()
            else:
                pass
        except (ValueError, Exception):
            pass