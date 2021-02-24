

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
import numpy as np
from arrow import utcnow
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas
import os
import cv2
from natsort import natsorted


class reportePDF(object):
    def __init__(self, titulo, cabecera, datos, nombrePDF):
        super(reportePDF, self).__init__()
        self.titulo = titulo
        self.cabecera = cabecera
        self.datos = datos
        self.nombrePDF = nombrePDF
        self.estilos = getSampleStyleSheet()

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


def verificar():
    global datos
    PATH = 'Dataset/part_A/test_data/images/'
    files = natsorted(os.listdir(PATH))

    for i in range(0, 182):
        imagen = files[i]
        print(imagen)
        img_filenames = os.listdir(PATH)
        m_list, s_list = [], []
        for img_filename in range(len(img_filenames)):
            img = cv2.imread('Dataset/part_A/test_data/images/' + imagen)
            img = img / 255.0
            m, s = cv2.meanStdDev(img)

            m_list.append(m.reshape((3,)))
            s_list.append(s.reshape((3,)))

            m_array = np.array(m_list)
            s_array = np.array(s_list)
            m = m_array.mean(axis=0, keepdims=True)
            s = s_array.mean(axis=0, keepdims=True)

            R_mean = m[0][2::]
            G_mean = m[0][1:0:-1]
            B_mean = m[0][0::-1]

            R_std = s[0][2::]
            G_std = s[0][1:0:-1]
            B_std = s[0][0::-1]
            NOMBRE_DE_IMAGEN = imagen
            Media_R = format(float(R_mean), ".3f")
            Media_G = format(float(G_mean), ".3f")
            Media_B = format(float(B_mean), ".3f")
            Desviacion_Estandar_R = format(float(R_std), ".3f")
            Desviacion_Estandar_G = format(float(G_std), ".3f")
            Desviacion_Estandar_B = format(float(B_std), ".3f")

        def dict_factory(c, row):
            d = {}
            for idx, col in enumerate(c.description):
                d[col[0]] = row[idx]
            return d

        conn = sqlite3.connect("Database/Normalizacion.db")
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS historial(NOMBRE_DE_IMAGEN TEXT,Media_R INTEGER , Media_G INTEGER,Media_B INTEGER ,Desviacion_Estandar_R INTEGER, Desviacion_Estandar_G INTEGER, Desviacion_Estandar_B INTEGER)")
        c.execute(
            "INSERT INTO historial (NOMBRE_DE_IMAGEN,Media_R , Media_G,Media_B ,Desviacion_Estandar_R, Desviacion_Estandar_G, Desviacion_Estandar_B) VALUES (?,?,?,?,?,?,?)",
            (NOMBRE_DE_IMAGEN, Media_R, Media_G, Media_B, Desviacion_Estandar_R, Desviacion_Estandar_G, Desviacion_Estandar_B))
        c.execute(
            "SELECT NOMBRE_DE_IMAGEN,Media_R , Media_G,Media_B ,Desviacion_Estandar_R, Desviacion_Estandar_G, Desviacion_Estandar_B FROM historial")
        datos = c.fetchall()
        conn.commit()
        c.close()
        conn.close()

    titulo = "REPORTE DE NORMALIZACION"
    cabecera = (
        ("NOMBRE_DE_IMAGEN", "NOMBRE DE IMAGEN"),
        ("Media_R", "Media en R"),
        ("Media_G", "Media en G"),
        ("Media_B", "Media en B"),
        ("Desviacion_Estandar_R", "Desviación Estandar en R"),
        ("Desviacion_Estandar_G", "Desviación Estandar en G"),
        ("Desviacion_Estandar_B", "Desviación Estandar en B"),
    )
    nombrePDF = "Reportes/Reporte de Normalización.pdf"
    reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
    print(reporte)


verificar()
