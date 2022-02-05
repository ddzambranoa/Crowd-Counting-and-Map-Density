import os
import sqlite3
import sys
from pathlib import Path
from time import strftime
from arrow import utcnow
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas
from Scripts.cuadrosDialogos import *

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
database = os.path.join(path, r'Database/Consultas.db')
imgError = os.path.join(path, r"Recursos/Error.png")
Reporte = os.path.join(path, r"Reportes/Reporte de Consultas.pdf")
carpReporte = os.path.join(path, r"Reportes/")


class reportePDF(object):
    def __init__(self, datos):
        super(reportePDF, self).__init__()
        self.titulo = "REPORTE DE CONSULTAS"
        self.cabecera = (("roll", "No. Consulta"), ("ImagenOriginal", "Imagen Original"), ("Aproximacion", "Aproximacion de Personas"),
                         ("Zona", "Zonas Posibles de Aglomeración"), ("Modelo", "Modelo Seleccionado"),
                         ("Hora", "Hora"), ("Fecha", "Fecha"))
        self.datos = datos
        try:
            os.stat(carpReporte)
        except (ValueError, Exception):
            os.mkdir(carpReporte)
        self.nombrePDF = Reporte
        self.estilos = getSampleStyleSheet()
        self.ancho = ""
        self.alto = ""

    @staticmethod
    def _encabezadoPiePagina(canva, archivoPDF):
        canva.saveState()
        estilos = getSampleStyleSheet()
        alineacion = ParagraphStyle(name="alineacion", alignment=TA_LEFT, parent=estilos["Normal"])
        encabezadoNombre = Paragraph(
            "Estimación de Densidad de Multitudes de Personas a través de Visión por Computador", estilos["Normal"])
        _, altura = encabezadoNombre.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoNombre.drawOn(canva, archivoPDF.leftMargin, 736)
        FechaConsulta = utcnow().to("local").format("dddd, DD  MMMM  YYYY", locale="es")
        Hora = strftime("%H:%M:%S")
        encabezadoFecha = Paragraph(FechaConsulta + " a las " + Hora, alineacion)
        _, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoFecha.drawOn(canva, archivoPDF.leftMargin, 725)
        piePagina = Paragraph("Reporte generado automáticamente.", estilos["Normal"])
        _, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
        piePagina.drawOn(canva, archivoPDF.leftMargin, 15 * mm + (0.2 * inch))
        canva.restoreState()

    def convertirDatos(self):
        estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_CENTER, fontSize=7, textColor=white,
                                          fontName="Helvetica-Bold", parent=self.estilos["Normal"])
        estiloNormal = self.estilos["Normal"]
        estiloNormal.alignment = TA_CENTER
        estiloNormal.fontSize = 7
        claves, nombres = zip(*[[k, n] for k, n in self.cabecera])
        encabezado = [Paragraph(nombre, estiloEncabezado) for nombre in nombres]
        nuevosDatos = [tuple(encabezado)]
        for dato in self.datos:
            nuevosDatos.append([Paragraph(str(dato[clave]), estiloNormal) for clave in claves])
        return nuevosDatos

    def Exportar(self):
        alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13, leading=10,
                                          textColor=purple, parent=self.estilos["Heading1"])
        self.ancho, self.alto = letter
        convertirDatos = self.convertirDatos()
        tabla = Table(convertirDatos, colWidths=(self.ancho - 100) / len(self.cabecera), hAlign="CENTER")
        tabla.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), purple), ("ALIGN", (0, 0), (0, -1), "LEFT"),
                                   ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("INNERGRID", (0, 0), (-1, -1), 0.50, black),
                                   ("BOX", (0, 0), (-1, -1), 0.25, black), ]))
        historia = [Paragraph(self.titulo, alineacionTitulo), Spacer(1, 0.16 * inch), tabla]
        archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Reporte de Consultas", author="Daniel Zambrano")
        try:
            archivoPDF.build(historia, onFirstPage=self._encabezadoPiePagina, onLaterPages=self._encabezadoPiePagina,
                             canvasmaker=numeracionPaginas)
        except PermissionError:
            pass


class numeracionPaginas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        numeroPaginas = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(numeroPaginas)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, conteoPaginas):
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch), "Página {} de {}".format(self._pageNumber, conteoPaginas))


class ExportPDF:
    def __init__(self):
        super(ExportPDF, self).__init__()
        try:
            def dict_factory(canv, row):
                d = {}
                for idx, col in enumerate(canv.description):
                    d[col[0]] = row[idx]
                return d

            conn = sqlite3.connect(database)
            conn.row_factory = dict_factory
            c = conn.cursor()
            c.execute("SELECT * FROM historial")
            datos = c.fetchall()
            conn.commit()
            c.close()
            conn.close()
            reportePDF(datos).Exportar()
        except (ValueError, Exception):
            pass
