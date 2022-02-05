from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect


class CircularProgress(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.value = 0
        self.width = 200
        self.height = 200
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.progress_color = 0xFFFFFF
        self.max_value = 100
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.text_color = 0x4988D1
        self.resize(self.width, self.height)

    def add_shadow(self, enable):
        if enable:
            self.shadow.setBlurRadius(15)
            self.shadow.setXOffset(0)
            self.shadow.setYOffset(0)
            self.shadow.setColor(QColor(0, 0, 0, 120))
            self.setGraphicsEffect(self.shadow)

    def set_value(self, value):
        self.value = value
        self.repaint()

    def paintEvent(self, event):
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setFont(QFont(self.font_family, self.font_size))
        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)
        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)
        pen.setColor(QColor(self.text_color))
        paint.setPen(pen)
        wait = "Espere por favor"
        analizando = "Analizando..."
        paint.drawText(rect, Qt.AlignCenter, f"{self.value}{self.suffix}")
        paint.setFont(QFont(self.font_family, 12))
        rect = QRect(0, -75, self.width, self.height)
        paint.drawText(rect, Qt.AlignCenter, f"{wait}")
        paint.setFont(QFont(self.font_family, 12))
        rect = QRect(0, 75, self.width, self.height)
        paint.drawText(rect, Qt.AlignCenter, f"{analizando}")
        paint.end()
