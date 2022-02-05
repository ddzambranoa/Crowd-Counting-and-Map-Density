# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Nombre:           reportePDF.py
# Autor:            Daniel David Zambrano Andrade
# Creado:           13 de Enero 2020
# Modificado:       13 de Enero 2020
# Copyright:        Free
# License:          Free
# Versión Python:   3.8
# ----------------------------------------------------------------------------

import sqlite3
import sys
from pathlib import Path

import numpy as np
import h5py
from arrow import utcnow
from natsort import natsorted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas
import PIL.Image as Image
from model import CSRNet
import torch
from torchvision import transforms
import os
import time
print(torch.__version__)
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
database = os.path.join(path, r'Database/ComparacionDispersas.db')
Reporte = os.path.join(path, r"Reportes/Reporte de Consultas.pdf")
carpReporte = os.path.join(path, r"Reportes/")
modDispersas = os.path.join(path, r'Modelos Entrenados/Multitudes_Dispersas.pth.tar')
modDensas = os.path.join(path, r'Modelos Entrenados/Multitudes_Densas.pth.tar')
modCombinadas = os.path.join(path, r'Modelos Entrenados/Multitudes_Densas-Dispersas.pth.tar')
conjuntoEtiquetas = os.path.join(path, r'Conjunto de Datos/Multitudes Dispersas/Pruebas/Etiquetas/')
conjuntoImagenes = os.path.join(path, r'Conjunto de Datos/Multitudes Dispersas/Pruebas/Imágenes/')
class reportePDF(object):
    def __init__(self, titulo, cabecera, datos, nombrePDF):
        super(reportePDF, self).__init__()
        try:
            os.stat(carpReporte)
        except (ValueError, Exception):
            os.mkdir(carpReporte)
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
                                       title="Reporte de Verificación", author="Daniel Zambrano")

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
    global MODELO, datos
    rootImages = conjuntoImagenes  # Ruta de las images en el dataset.
    rootGroundTruth = conjuntoEtiquetas  # Ruta de las images en el dataset.
    dataImages = natsorted(os.listdir(rootImages))  # Lista a las imagenes dentro del dataset.

    for i in range(len(dataImages)):  # Ejecutar por lotes (0,22) (22,25)(25,49)(49,182) len(dataImages)

        def dict_factory(c, row):
            d = {}
            for idx, col in enumerate(c.description):
                d[col[0]] = row[idx]
            return d
        conn = sqlite3.connect(database)
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS historial(NOMBRE_DE_IMAGEN TEXT,APROXIMACION_REAL INTEGER , "
            "APROXIMACION_DEL_MODELO INTEGER,DIFERENCIA_GROUND_TRUTH_VS_MODELO INTEGER , MODELO TEXT)")        # start = time.time()
        images = dataImages[i]
        dataGT = dataImages[i].replace('.jpg', '.h5')
        groundRoot = rootGroundTruth + dataGT
        imagen = rootImages + images
        print(images)
        NOMBRE_DE_IMAGEN = images
        mean_R = 0.485
        mean_G = 0.456
        mean_B = 0.406
        std_R = 0.229
        std_G = 0.224
        std_B = 0.225

        # modeloentrenado = modDensas
        # modeloentrenado = modDispersas
        modeloentrenado = modCombinadas
        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize(mean=[mean_R, mean_G, mean_B], std=[std_R, std_G, std_B]), ])
        model = CSRNet()
        cargarModelo = torch.load(modeloentrenado, map_location=torch.device('cpu'))
        model.load_state_dict(cargarModelo['state_dict'])
        image = Image.open(imagen)
        salida = model(transform(image.convert('RGB')).unsqueeze(0))
        groundtruth = h5py.File(groundRoot, 'r')
        groundtruth = np.asarray(groundtruth['density'])
        D_GT_M = (int(np.sum(groundtruth)) - int(salida.detach().cpu().sum().numpy()))
        # end = time.time()
        # print(end - start)


        APROXIMACION_REAL = int(np.sum(groundtruth))
        APROXIMACION_DEL_MODELO = int(salida.detach().cpu().sum().numpy())
        DIFERENCIA_GROUND_TRUTH_VS_MODELO = abs(D_GT_M)
        # if modeloentrenado == 'Modelos Entrenados/Multitudes_Densas.pth.tar':
        #     MODELO = "Modelo de multitud densa"
        # MODELO = "Modelo de multitud dispersa"
        # if modeloentrenado == 'Modelos Entrenados/Multitudes_Densas-Dispersas.pth.tar':
        MODELO = "Modelo de multitud combinada"


        c.execute(
            "INSERT INTO historial (NOMBRE_DE_IMAGEN ,APROXIMACION_REAL ,"
            "APROXIMACION_DEL_MODELO,DIFERENCIA_GROUND_TRUTH_VS_MODELO, MODELO) VALUES (?,?,?,?,?)",
            (NOMBRE_DE_IMAGEN, APROXIMACION_REAL, APROXIMACION_DEL_MODELO, DIFERENCIA_GROUND_TRUTH_VS_MODELO, MODELO))
        c.execute(
            "SELECT NOMBRE_DE_IMAGEN,APROXIMACION_REAL ,APROXIMACION_DEL_MODELO  ,"
            "DIFERENCIA_GROUND_TRUTH_VS_MODELO, MODELO FROM historial")
        datos = c.fetchall()
        conn.commit()
        c.close()
        conn.close()

    titulo = "REPORTE DE VERIFICACIÓN"
    cabecera = (
        ("NOMBRE_DE_IMAGEN", "NOMBRE DE IMAGEN"),
        ("APROXIMACION_REAL", "APROXIMACIÓN REAL"),
        ("APROXIMACION_DEL_MODELO", "APROXIMACIÓN DEL MODELO CSRNet"),
        ("DIFERENCIA_GROUND_TRUTH_VS_MODELO", "DIFERENCIA GROUND TRUTH VS MODELO CSRNet"),
        ("MODELO", "MODELO"),
    )
    nombrePDF = Reporte
    reporte = reportePDF(titulo, cabecera, datos, nombrePDF).Exportar()
    print(reporte)


verificar()
