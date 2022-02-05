# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Nombre:           Mean_Std.py
# Autor:            Daniel David Zambrano Andrade
# Creado:           13 de Enero 2020
# Modificado:       13 de Enero 2020
# Copyright:        Free
# License:          Free
# Versión Python:   3.8
# ----------------------------------------------------------------------------
import sqlite3
from arrow import utcnow
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas


class reportePDF(object):
    def __init__(self, datos):
        super(reportePDF, self).__init__()
        self.titulo = "REPORTE DE CONSULTAS"
        self.cabecera = (("Nombre", "Nombre"),
                         ("Aproximacion", "Aproximacion"),
                         ("Zona", "Zona"),
                         ("Fecha", "Fecha"),
                         ("Year", "Year"),
                         ("MapaDeDensidad", "Mapa de Densidad"),
                         ("ImagenOriginal", "Imagen Original"),)
        self.datos = datos
        self.nombrePDF = "Reportes/Reporte de Consultas.pdf"
        self.estilos = getSampleStyleSheet()
        self.ancho = ""
        self.alto = ""

    @staticmethod
    def _encabezadoPiePagina(canvas, archivoPDF):
        canvas.saveState()
        estilos = getSampleStyleSheet()
        alineacion = ParagraphStyle(name="alineacion", alignment=TA_LEFT, parent=estilos["Normal"])

        encabezadoNombre = Paragraph(
            "Estimación de Densidad de Multitudes de Personas a través de Visión por Computador", estilos["Normal"])
        anchura, altura = encabezadoNombre.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoNombre.drawOn(canvas, archivoPDF.leftMargin, 736)

        fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
        fechaReporte = fecha.replace("-", "de")

        encabezadoFecha = Paragraph(fechaReporte, alineacion)
        anchura, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoFecha.drawOn(canvas, archivoPDF.leftMargin, 725)

        piePagina = Paragraph("Reporte generado por Daniel Zambrano.", estilos["Normal"])
        anchura, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
        piePagina.drawOn(canvas, archivoPDF.leftMargin, 15 * mm + (0.2 * inch))

        canvas.restoreState()

    def convertirDatos(self):
        estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_CENTER,
                                          fontSize=7, textColor=white,
                                          fontName="Helvetica-Bold",
                                          parent=self.estilos["Normal"])

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
        alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13,
                                          leading=10, textColor=purple,
                                          parent=self.estilos["Heading1"])
        self.ancho, self.alto = letter
        convertirDatos = self.convertirDatos()
        tabla = Table(convertirDatos, colWidths=(self.ancho - 100) / len(self.cabecera), hAlign="CENTER")
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), purple),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black),
            ("BOX", (0, 0), (-1, -1), 0.25, black),
        ]))
        historia = [Paragraph(self.titulo, alineacionTitulo), Spacer(1, 0.16 * inch), tabla]
        archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Reporte de Normalización", author="Daniel Zambrano")

        try:
            archivoPDF.build(historia, onFirstPage=self._encabezadoPiePagina,
                             onLaterPages=self._encabezadoPiePagina,
                             canvasmaker=numeracionPaginas)
            return "Reporte generado con éxito."
        except PermissionError:
            return "Error inesperado: Permiso denegado."


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
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                             "Página {} de {}".format(self._pageNumber, conteoPaginas))


def dict_factory(c, row):
    d = {}
    for idx, col in enumerate(c.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect("Database/Consultas.db")
conn.row_factory = dict_factory
c = conn.cursor()
c.execute(
    "SELECT Nombre,Aproximacion, Zona, Fecha, Year, MapaDeDensidad,ImagenOriginal FROM historial")
datos = c.fetchall()
conn.commit()
c.close()
conn.close()
reporte = reportePDF(datos).Exportar()
print(reporte)
