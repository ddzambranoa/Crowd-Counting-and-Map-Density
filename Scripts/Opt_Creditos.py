import os
import sys
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QVBoxLayout, QDialog
from pathlib import Path

from qtpy import QtCore

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
imgFondo = os.path.join(path, r'Recursos/Blanco')
imgPersonal = os.path.join(path, r'Recursos/Yo.png')


class Creditos(QDialog):
    def __init__(self, *args, **kwargs):
        super(Creditos, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint |
                            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedWidth(460)
        self.setFixedHeight(250)
        self.setWindowIcon(QIcon(imgPersonal))
        q_btn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        self.setWindowTitle("Créditos")
        title = QLabel("Universidad Técnica del Norte")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)
        label2 = QLabel(self)
        pixmap2 = QPixmap(imgFondo)
        label2.setPixmap(pixmap2)
        label2.setScaledContents(True)
        label2.resize(pixmap2.width(), pixmap2.height())
        label = QLabel(self)
        pixmap = QPixmap(imgPersonal)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.resize(120, 120)
        label.move(335, 80)
        layout.addWidget(title)
        layout.addWidget(QLabel("Estimación de Densidad de Personas a través de Visión por Computador"))
        layout.addWidget(QLabel("Versión: 1.0"))
        layout.addWidget(QLabel("Autor: Daniel David Zambrano Andrade"))
        layout.addWidget(QLabel("Correo: ddzambranoa@utn.edu.ec"))
        layout.addWidget(QLabel("Año: 2021"))
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
