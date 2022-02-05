import sys
from time import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout

from Scripts.setupProgressBar import CircularProgress
counter = 0


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(500, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.container = QFrame()
        self.container.setStyleSheet("background-color: transparent")
        self.layout = QVBoxLayout()
        self.progress = CircularProgress()
        self.progress.value = 0
        self.progress.suffix = "%"
        self.progress.font_size = 30
        self.progress.width = 300
        self.progress.height = 300
        self.progress.progress_width = 20
        self.progress.text_color = 0xFFFFFF
        self.progress.progress_color = 0xFFFFFF
        self.progress.progress_rounded_cap = True
        self.progress.add_shadow(True)
        self.progress.setMinimumSize(self.progress.width, self.progress.height)
        self.layout.addWidget(self.progress, Qt.AlignCenter, Qt.AlignCenter)
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(120)
        # self.update(activacion)

    def update(self):
        global counter
        print(counter)
        self.progress.set_value(counter)
        counter += 1
        if counter > 100:
            counter = 0
            self.timer.stop()

    def change_value(self, value):
        self.progress.set_value(value)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec_())
