from tkinter import filedialog

file = filedialog.askopenfilename(title="abrir")
print(file)

# # import sys
# # import time
# # from IPython.external.qt_for_kernel import QtCore
# # from PyQt5.QtGui import QIcon, QPixmap
# # from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QDialogButtonBox, QGridLayout, QPushButton
# # import torch
# # import GPUtil
# import sqlite3
# from time import strftime
#
# from arrow import utcnow
# from xlsxwriter.workbook import Workbook
#
# FechaConsulta = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
# fechaReporte = FechaConsulta.replace("-", "de")
# Hora = strftime("%H:%M:%S")
# celdaConteo = 2
# celdaZonas = 3
# n = 3
# m = 4
# workbook = Workbook('Reportes/Reporte de Consultas.xlsx')
# worksheet = workbook.add_worksheet("Base de Datos")
# alineacion = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
# numbersformat = workbook.add_format({'num_format': '#,##0.00', 'align': 'center', 'valign': 'vcenter'})
# font = workbook.add_format()
# font.set_font_size(26)
# font2 = workbook.add_format()
# font2.set_font_size(12)
# conn = sqlite3.connect("Database/Consultas.db")
# c = conn.cursor()
# c.execute("SELECT * FROM historial")
# mysel = c.execute("SELECT * FROM historial ")
# connection = sqlite3.connect("Database/Consultas.db")
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM historial")
# recuento = (len(cursor.fetchall()))
# margenTabla = "A" + str(n) + ":" "M" + str(recuento + m)
# titulo = 'Estimación de Densidad de Personas a través de Visión por Computador'
# subtitulo = 'Reporte generado automáticamente el dia '
# worksheet.merge_range('A1:M1', "")
# worksheet.merge_range('A2:M2', "")
# worksheet.write('A1:M1', titulo, font)
# worksheet.write('A2:M2', subtitulo + fechaReporte + " a las " + Hora, font2)
# worksheet.set_column('A:A', 25, alineacion)
# worksheet.set_column('B:B', 25, alineacion)
# worksheet.set_column('C:C', 25, alineacion)
# worksheet.set_column('D:D', 35, alineacion)
# worksheet.set_column('E:E', 25, alineacion)
# worksheet.set_column('F:F', 25, alineacion)
# worksheet.set_column('G:G', 25, alineacion)
# worksheet.set_column('H:H', 35, alineacion)
# worksheet.set_column('I:I', 35, alineacion)
# worksheet.set_column('J:J', 35, alineacion)
# worksheet.set_column('K:K', 35, alineacion)
# worksheet.set_column('L:L', 35, alineacion)
# worksheet.set_column('M:M', 100, alineacion)
# formula = '=SUM(Table8[@[Conteo de Personas]:[Zonas con Aglomeraciones])'
# worksheet.add_table(margenTabla, {'total_row': 2, 'columns': [{'total_string': 'Total', 'header': 'No. Consulta'},
#                                                               {'header': 'Nombre de la Imagen',
#                                                                'total_function': 'count',
#                                                                'format': numbersformat},
#                                                               {'header': 'Conteo de Personas', 'total_function': 'sum',
#                                                                'format': numbersformat},
#                                                               {'header': 'Zonas con Aglomeraciones',
#                                                                'total_function': 'sum',
#                                                                'format': numbersformat},
#                                                               {'header': 'Modelo Seleccionado'},
#                                                               {'header': 'Hora'}, {'header': 'Fecha'},
#                                                               {'header': 'Nombre de Mapa de Densidad'},
#                                                               {'header': 'Nombre de Imagen Binaria'},
#                                                               {'header': 'Nombre de Imagen Numerada'},
#                                                               {'header': 'Nombre de Imagen con Contorno'},
#                                                               {'header': 'Nombre de Mapa de Calor CV2'},
#                                                               {'header': 'Ruta de Almacenamiento'}, ]})
# for i, row in enumerate(mysel):
#     for j, value in enumerate(row):
#         if j == celdaConteo or j == celdaZonas:
#             worksheet.write(i + n, j, int(value))
#         else:
#             worksheet.write(i + n, j, value)
# workbook.close()

# GPUtil.showUtilization()
# import psutil
# while True:
#     ramTotalGB = (psutil.virtual_memory().total/(1024.0 ** 3))
#     ramTotalGB = round(ramTotalGB, 1)
#     print("Ram total " + str(ramTotalGB) + "GB")
#
#     ramDisponibleGB = (psutil.virtual_memory().available/(1024.0 ** 3))
#     ramDisponibleGB = round(ramDisponibleGB, 1)
#     print("Ram disponible " + str(ramDisponibleGB) + "GB")
#
#     ramOcupadoGB = ramTotalGB - ramDisponibleGB
#     ramOcupadoGB = round(ramOcupadoGB, 1)
#     print("Ram ocupada " + str(ramOcupadoGB) + "GB")
#
#     print("Porcentaje ram ocupado "+str(psutil.virtual_memory().percent) + "%")
#
#     ramDisponiblePorcentaje = (float(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))
#     ramDisponiblePorcentaje = round(ramDisponiblePorcentaje, 1)
#     print("Porcentaje ram disponible " + str(ramDisponiblePorcentaje) + "%")
#     time.sleep(1)
#
# global use_cuda
#
#
# class HyperlinkLabel(QLabel):
#     def __init__(self, parent=None):
#         super().__init__()
#         self.setOpenExternalLinks(True)
#         self.setParent(parent)
#
#
# class VerificacionGPU(QDialog):
#     def __init__(self, *args, **kwargs):
#         super(VerificacionGPU, self).__init__(*args, **kwargs)
#         global use_cuda
#         use_cuda = torch.cuda.is_available()
#         self.setWindowFlags(
#             QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowStaysOnTopHint)
#         self.setFixedWidth(460)
#         self.setFixedHeight(250)
#         self.setWindowIcon(QIcon("Recursos/NVIDIA.png"))
#         QBtn = QDialogButtonBox.Ok
#         self.buttonBox = QDialogButtonBox(QBtn)
#         self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)
#         QBtn2 = QDialogButtonBox.Cancel
#         self.buttonBox2 = QDialogButtonBox(QBtn2)
#         self.buttonBox2.accepted.connect(self.accept)
#         self.buttonBox2.rejected.connect(self.reject)
#         self.button = QPushButton('Omitir')
#         self.button.setFixedWidth(100)
#         self.button.setFixedHeight(25)
#         self.button.setDefault(False)
#         self.button1 = QPushButton('Salir')
#         self.button1.setFixedWidth(100)
#         self.button1.setFixedHeight(25)
#         self.button1.setDefault(True)
#         self.button2 = QPushButton('Aceptar')
#         self.button2.setFixedWidth(100)
#         self.button2.setFixedHeight(25)
#         self.button2.setDefault(True)
#         layout = QGridLayout()
#         self.setWindowTitle("CUDA")
#         title = QLabel("Verificación CUDA")
#         font = title.font()
#         font.setPointSize(15)
#         title.setFont(font)
#         label2 = QLabel(self)
#         pixmap2 = QPixmap('Recursos/Blanco.png')
#         label2.setPixmap(pixmap2)
#         label2.resize(pixmap2.width(), pixmap2.height())
#         label = QLabel(self)
#         pixmap = QPixmap('Recursos/NVIDIA.png')
#         label.setPixmap(pixmap)
#         label.setOpenExternalLinks(True)
#         label.setScaledContents(True)
#         label.resize(120, 120)
#         label.move(325, 15)
#         layout.addWidget(title)
#         if use_cuda:
#             device = (torch.cuda.current_device())
#             nameDevice = torch.cuda.get_device_name(device)
#             memoria = torch.cuda.get_device_properties(device).total_memory / (1024 ** 2)
#             layout.addWidget(QLabel("CUDA DISPONIBLE"))
#             layout.addWidget(QLabel("Tarjeta: " + str(nameDevice)))
#             layout.addWidget(QLabel("Memoria Total: " + str(memoria)))
#             layout.addWidget(QLabel("Dispositivo: " + str(device)))
#             layout.addWidget(self.button2, 6, 5)
#             self.setLayout(layout)
#         else:
#             linkTemplate = 'Instale los drivers de <a href= https://la.nvidia.com/Download/index.aspx?lang=la>NVIDIA</a> y <a href=https://developer.nvidia.com/cuda-downloads>CUDA</a>.'
#             label1 = HyperlinkLabel(self)
#             label1.setText(linkTemplate.format())
#             layout.addWidget(QLabel())
#             layout.addWidget(QLabel())
#             layout.addWidget(label1, 5, 0)
#             layout.addWidget(self.button, 5, 5)
#             layout.addWidget(self.button1, 6, 5)
#             layout.addWidget(QLabel("Verifique la disponibilidad de una tarjeta NVIDIA."), 4, 0)
#             layout.addWidget(QLabel("CUDA NO DISPONIBLE"), 2, 0)
#             self.setLayout(layout)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     demo = VerificacionGPU()
#     demo.show()
#
#     sys.exit(app.exec_())
