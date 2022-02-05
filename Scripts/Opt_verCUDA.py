import os
import sys

import torch
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QDialog, QGridLayout, QApplication
from pathlib import Path
global use_cuda

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
imgFondo = os.path.join(path, r'Recursos/Blanco')
imgNVIDIA = os.path.join(path, r'Recursos/NVIDIA.png')


class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setParent(parent)


class VerificacionGPU(QDialog):
    def __init__(self, *args, **kwargs):
        super(VerificacionGPU, self).__init__(*args, **kwargs)
        global use_cuda
        use_cuda = torch.cuda.is_available()
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedWidth(460)
        self.setFixedHeight(250)
        self.setWindowIcon(QIcon(imgNVIDIA))
        btn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        btn2 = QDialogButtonBox.Cancel
        self.buttonBox2 = QDialogButtonBox(btn2)
        self.buttonBox2.accepted.connect(self.accept)
        self.buttonBox2.rejected.connect(self.reject)
        q_btn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout = QGridLayout()
        self.setWindowTitle("CUDA")
        title = QLabel("Verificación CUDA")
        font = title.font()
        font.setPointSize(15)
        title.setFont(font)
        label2 = QLabel(self)
        pixmap2 = QPixmap(imgFondo)
        label2.setPixmap(pixmap2)
        label2.resize(pixmap2.width(), pixmap2.height())
        label = QLabel(self)
        pixmap = QPixmap(imgNVIDIA)
        label.setPixmap(pixmap)
        label.setOpenExternalLinks(True)
        label.setScaledContents(True)
        label.resize(120, 120)
        label.move(325, 15)
        layout.addWidget(title)
        if use_cuda:
            device = (torch.cuda.current_device())
            name_device = torch.cuda.get_device_name(device)
            memoria = torch.cuda.get_device_properties(device).total_memory / (1024 ** 2)
            layout.addWidget(QLabel("CUDA DISPONIBLE"))
            layout.addWidget(QLabel("Tarjeta: " + str(name_device)))
            layout.addWidget(QLabel("Memoria Total: " + str(memoria)))
            layout.addWidget(QLabel("Dispositivo: " + str(device)))
            layout.addWidget(self.buttonBox)
            self.setLayout(layout)
        else:
            link_template = 'Instale los drivers de <a href= https://la.nvidia.com/Download/index.aspx?lang=la>NVIDIA' \
                           '</a> y <a href=https://developer.nvidia.com/cuda-downloads>CUDA</a>. '
            label1 = HyperlinkLabel(self)
            label1.setText(link_template.format())
            layout.addWidget(QLabel())
            layout.addWidget(QLabel())
            layout.addWidget(label1, 5, 0)
            layout.addWidget(self.buttonBox, 6, 5)
            layout.addWidget(QLabel("Verifique la disponibilidad de una tarjeta NVIDIA."), 4, 0)
            layout.addWidget(QLabel("CUDA NO DISPONIBLE"), 2, 0)
            self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = VerificacionGPU()
    main.show()
    sys.exit(app.exec_())
