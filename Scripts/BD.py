import sys
import os
from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QTableWidget, QToolBar, QStatusBar, QHeaderView, QAbstractItemView, \
    QApplication

from Scripts.BD_LimpiarTabla import eliminar_tabla
from Scripts.BD_actualizarTabla import actualizar_tabla
from Scripts.BD_crearBD import crearDatabase
from Scripts.BD_existenciaBD import abrirExcel, abrirPDF
from Scripts.Opt_Ayuda import Ayuda
from Scripts.Opt_Creditos import Creditos
from Scripts.BD_visualizarConsulta import visualizarConsulta
from Scripts.BD_eliminarConsulta import eliminarConsulta
from Scripts.cuadrosDialogos import close_event

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
interfaz_ayuda = os.path.join(path, r'Interfaz/Ayuda.ui')
dbConsultas = os.path.join(path, r'Database/Consultas.db')
img_ayuda = os.path.join(path, r'Recursos/ayuda.png')
imgNVIDIA = os.path.join(path, r'Recursos/NVIDIA.png')
imgPersonal = os.path.join(path, r'Recursos/Yo.png')
imgExit = os.path.join(path, r'Recursos/exit.png')
imgDatabase = os.path.join(path, r'Recursos/database.png')
imgActualizar = os.path.join(path, r'Recursos/r3.png')
imgExcel = os.path.join(path, r'Recursos/EXCEL.png')
imgPDF = os.path.join(path, r'Recursos/PDF.png')
imgVisualizar = os.path.join(path, r'Recursos/visualizar3.png')
imgEliminar = os.path.join(path, r'Recursos/d1.png')
imgAyuda = os.path.join(path, r'Recursos/ayuda.png')
imgExportar = os.path.join(path, r'Recursos/exportar.png')
imgError = os.path.join(path, r"Recursos/Error.png")
imgFondo = os.path.join(path, r'Recursos/Blanco')

archExcel = os.path.join(path, r'Reportes/Reporte de Consultas.xlsx')
archPDF = os.path.join(path, r'Reportes/Reporte de Consultas.pdf')
Reporte = os.path.join(path, r"Reportes/Reporte de Consultas.pdf")


class Database(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Database, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon(imgDatabase))
        self.conexion = ""
        crearDatabase()
        menu_archivos = self.menuBar().addMenu("&Archivos")
        self.setWindowTitle("Historial de consultas")
        self.setMinimumSize(1125, 740)
        self.setMaximumSize(1125, 740)
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("background-color: #BCD9EA;")
        self.tableWidget.setColumnCount(12)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("No. Consulta", "Nombre de la Imagen", "No. Aproximado de personas",
                                                    "Zonas Posibles de Aglomeración", "Modelo Seleccionado",
                                                    "Hora de Consulta", "Fecha de Consulta", "Mapa de Densidad",
                                                    "Imagen Binaria",
                                                    "Imagen Numerada", "Imagen Contorno", "Mapa CV2", "Ruta"))
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for indice, ancho in enumerate((100, 300, 225, 225, 175, 150, 150, 300, 300, 300, 300, 300), start=0):
            self.tableWidget.setColumnWidth(indice, ancho)
        self.tableWidget.setColumnHidden(3, True)
        self.tableWidget.setColumnHidden(7, True)
        self.tableWidget.setColumnHidden(8, True)
        self.tableWidget.setColumnHidden(9, True)
        self.tableWidget.setColumnHidden(10, True)
        self.tableWidget.setColumnHidden(11, True)
        self.tableWidget.setColumnHidden(12, True)
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        btn_actualizar = QAction(QIcon(imgActualizar), "Actualizar Reporte/Base de Datos", self)  # refresh icon
        btn_actualizar.triggered.connect(self.cargar_datos)
        btn_actualizar.setStatusTip("Actualizar base de datos")
        toolbar.addAction(btn_actualizar)
        btn_visualizar = QAction(QIcon(imgVisualizar), "Visualizar", self)  # search icon
        btn_visualizar.triggered.connect(self.visualizar)
        btn_visualizar.setStatusTip("Visualizar consulta")
        toolbar.addAction(btn_visualizar)
        btn_eliminar = QAction(QIcon(imgEliminar), "Eliminar", self)
        btn_eliminar.triggered.connect(self.eliminar)
        btn_eliminar.triggered.connect(self.cargar_datos)
        btn_eliminar.setStatusTip("Eliminar consulta")
        toolbar.addAction(btn_eliminar)
        export_excel_m = QAction(QIcon(imgExcel), "Exportar a Excel", self)
        export_excel_m.triggered.connect(self.cargar_datos)
        export_excel_m.triggered.connect(self.abrir_excel)
        export_excel_m.setStatusTip(
            "Exportar a Excel, si tiene un archivo exportado anteriormente cierrelo inmediatamente.")
        toolbar.addAction(export_excel_m)
        export_pdf_m = QAction(QIcon(imgPDF), "Exportar a PDF", self)
        export_pdf_m.triggered.connect(self.cargar_datos)
        export_pdf_m.triggered.connect(self.abrir_pdf)
        export_pdf_m.setStatusTip(
            "Exportar a PDF, si tiene un archivo exportado anteriormente cierrelo inmediatamente.")
        toolbar.addAction(export_pdf_m)
        visualizar = QAction(QIcon(imgVisualizar), "Visualizar consulta", self)
        visualizar.triggered.connect(self.visualizar)
        visualizar.setStatusTip("Visualizar consulta")
        menu_archivos.addAction(visualizar)
        eliminar = QAction(QIcon(imgEliminar), "Eliminar consulta", self)
        eliminar.triggered.connect(self.eliminar)
        eliminar.triggered.connect(self.cargar_datos)
        eliminar.setStatusTip("Eliminar consulta")
        menu_archivos.addAction(eliminar)
        exportar = menu_archivos.addMenu(QIcon(imgExportar), 'Exportar')
        export_excel = QAction(QIcon(imgExcel), 'Exportar a Excel', self)
        export_excel.setStatusTip(
            'Exportar base de datos a EXCEL, si tiene un archivo exportado anteriormente cierrelo inmediatamente.')
        export_excel.triggered.connect(self.cargar_datos)
        export_excel.triggered.connect(self.abrir_excel)
        export_pdf = QAction(QIcon(imgPDF), 'Exportar a PDF', self)
        export_pdf.setStatusTip(
            'Exportar base de datos a PDF, si tiene un archivo exportado anteriormente cierrelo inmediatamente.')
        export_pdf.triggered.connect(self.cargar_datos)
        export_pdf.triggered.connect(self.abrir_pdf)
        exportar.addAction(export_excel)
        exportar.addAction(export_pdf)
        menu_ayuda = self.menuBar().addMenu("&Ayuda")
        ayuda = QAction(QIcon(imgAyuda), "Ayuda ", self)
        ayuda.setStatusTip("Ayuda")
        ayuda.triggered.connect(self.ayuda)
        menu_ayuda.addAction(ayuda)
        creditos = QAction(QIcon(imgPersonal), "Créditos ", self)  # info icon
        creditos.triggered.connect(self.creditos)
        creditos.setStatusTip("Créditos")
        menu_ayuda.addAction(creditos)
        menu_opciones = self.menuBar().addMenu("&Opciones")
        opciones = QAction(QIcon(imgEliminar), "Eliminar base de datos ", self)
        opciones.setStatusTip("Limpiar base de datos")
        opciones.triggered.connect(self.limpiar_database)
        opciones.triggered.connect(self.cargar_datos)
        menu_opciones.addAction(opciones)
        self.cargar_datos()
        self.show()

    def cargar_datos(self):
        actualizar_tabla(self)

    @staticmethod
    def eliminar():
        db_eliminar_consulta = eliminarConsulta()
        db_eliminar_consulta.exec_()

    @staticmethod
    def visualizar():
        db_visualizar = visualizarConsulta()
        db_visualizar.exec_()

    @staticmethod
    def creditos():
        creditos = Creditos()
        creditos.exec_()

    @staticmethod
    def ayuda():
        ayuda = Ayuda()
        ayuda.exec_()

    @staticmethod
    def abrir_pdf():
        abrirPDF()

    @staticmethod
    def abrir_excel():
        abrirExcel()

    @staticmethod
    def limpiar_database():
        eliminar_tabla()

    def closeEvent(self, event):
        close_event(event, "¿Desea salir de la base de datos?")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Database()
    w.show()
    sys.exit(app.exec_())
