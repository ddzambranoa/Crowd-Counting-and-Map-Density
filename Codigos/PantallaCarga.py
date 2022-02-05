import sys

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import QMetaObject, QCoreApplication, QRect, Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QLabel, QProgressBar, QFrame, \
    QVBoxLayout, QWidget
counter = 0


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, parent=None)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)
        self.ui.label_description.setText("<strong>INICIANDO</strong>")
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>CARGANDO</strong> BASE DE DATOS"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>CARGANDO</strong> INTERFAZ DE USUARIO"))
        self.show()

    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter)
        if counter > 100:
            self.timer.stop()
            self.close()
        counter += 1


class Ui_SplashScreen(object):

    centralwidget: QWidget
    verticalLayout: QVBoxLayout
    dropShadowFrame: QFrame
    label_title: QLabel
    label_description = QLabel
    progressBar = QProgressBar
    label_loading = QLabel
    label_credits = QLabel

    def setupUi(self, SplashScreenI):
        if SplashScreenI.objectName():
            SplashScreenI.setObjectName(u"SplashScreen")
        SplashScreenI.resize(680, 400)
        self.centralwidget = QWidget(SplashScreenI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"QFrame {	\n"
                                           "	background-color: rgb(56, 58, 89);	\n"

                                           "	border-radius: 10px;\n"
                                           "}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.label_title = QLabel(self.dropShadowFrame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(0, 90, 661, 61))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(19)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"color: rgb(254, 121, 199);")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_description = QLabel(self.dropShadowFrame)
        self.label_description.setObjectName(u"label_description")
        self.label_description.setGeometry(QRect(0, 150, 661, 31))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(14)
        self.label_description.setFont(font1)
        self.label_description.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_description.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(self.dropShadowFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(50, 280, 561, 23))
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
                                       "	\n"
                                       "	background-color: rgb(98, 114, 164);\n"
                                       "	color: rgb(200, 200, 200);\n"
                                       "	border-style: none;\n"
                                       "	border-radius: 10px;\n"
                                       "	text-align: center;\n"
                                       "}\n"
                                       "QProgressBar::chunk{\n"
                                       "	border-radius: 10px;\n"
                                       "	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));\n"
                                       "}")
        self.progressBar.setValue(24)
        self.label_loading = QLabel(self.dropShadowFrame)
        self.label_loading.setObjectName(u"label_loading")
        self.label_loading.setGeometry(QRect(-1, 320, 660, 20))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(12)
        self.label_loading.setFont(font2)
        self.label_loading.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_loading.setAlignment(Qt.AlignCenter)
        self.label_credits = QLabel(self.dropShadowFrame)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setGeometry(QRect(20, 350, 621, 21))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(10)
        self.label_credits.setFont(font3)
        self.label_credits.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_credits.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.dropShadowFrame)
        SplashScreenI.setCentralWidget(self.centralwidget)
        self.retranslateUi(SplashScreenI)
        QMetaObject.connectSlotsByName(SplashScreenI)

    def retranslateUi(self, SplashScreenI):
        SplashScreenI.setWindowTitle(QCoreApplication.translate("SplashScreen", u"MainWindow", None))
        self.label_title.setText(QCoreApplication.translate("SplashScreen", u"<strong>ESTIMACIÓN DE DENSIDAD DE PERSONAS</strong>", None))
        self.label_description.setText(QCoreApplication.translate("SplashScreen", u"<strong></strong>", None))
        self.label_loading.setText(QCoreApplication.translate("SplashScreen", u"Cargando...", None))
        self.label_credits.setText(QCoreApplication.translate("SplashScreen", u"<strong>Creador</strong>: Daniel Zambrano A.", None))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = SplashScreen()
    sys.exit(app.exec_())
