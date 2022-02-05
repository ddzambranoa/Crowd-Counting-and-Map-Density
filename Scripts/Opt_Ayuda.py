import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from qtpy.uic import loadUi
from pathlib import Path

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
interfaz_ayuda = os.path.join(path, r'Interfaz\Ayuda.ui')
img_ayuda = os.path.join(path, r'Recursos\ayuda.png')


class Ayuda(QDialog):
    def __init__(self, *args, **kwargs):
        super(Ayuda, self).__init__(*args, **kwargs)
        loadUi(interfaz_ayuda, self)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(img_ayuda))
