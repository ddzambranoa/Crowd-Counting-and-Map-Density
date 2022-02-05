import os
import sqlite3
import sys
from pathlib import Path
from time import strftime
from arrow import utcnow
from xlsxwriter.workbook import Workbook

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
archExcel = os.path.join(path, r'Reportes/Reporte de Consultas.xlsx')
dbConsultas = os.path.join(path, r'Database/Consultas.db')


class ExportEXCEL:
    def __init__(self):
        super(ExportEXCEL, self).__init__()
        try:
            FechaConsulta = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
            Hora = strftime("%H:%M:%S")
            celdaConteo = 2
            celdaZonas = 3
            n = 3
            m = 4
            workbook = Workbook(archExcel)
            worksheet = workbook.add_worksheet("Base de Datos")
            alineacion = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
            numbersformat = workbook.add_format({'num_format': '#,##0', 'align': 'center', 'valign': 'vcenter'})
            font = workbook.add_format()
            font.set_font_size(26)
            font2 = workbook.add_format()
            font2.set_font_size(12)
            conn = sqlite3.connect(dbConsultas)
            c = conn.cursor()
            c.execute("SELECT * FROM historial")
            mysel = c.execute("SELECT * FROM historial ")
            connection = sqlite3.connect(dbConsultas)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM historial")
            recuento = (len(cursor.fetchall()))
            margenTabla = "A" + str(n) + ":" "M" + str(recuento + m)
            titulo = 'Estimación de Densidad de Personas a través de Visión por Computador'
            subtitulo = 'Reporte generado automáticamente el dia '
            worksheet.merge_range('A1:M1', "")
            worksheet.merge_range('A2:M2', "")
            worksheet.freeze_panes(3, 2)
            worksheet.write('A1:M1', titulo, font)
            worksheet.write('A2:M2', subtitulo + FechaConsulta + " a las " + Hora, font2)
            worksheet.set_column('A:A', 25, alineacion)
            worksheet.set_column('B:B', 25, alineacion)
            worksheet.set_column('C:C', 25, alineacion)
            worksheet.set_column('D:D', 35, alineacion)
            worksheet.set_column('E:E', 25, alineacion)
            worksheet.set_column('F:F', 25, alineacion)
            worksheet.set_column('G:G', 25, alineacion)
            worksheet.set_column('H:H', 35, alineacion)
            worksheet.set_column('I:I', 35, alineacion)
            worksheet.set_column('J:J', 35, alineacion)
            worksheet.set_column('K:K', 35, alineacion)
            worksheet.set_column('L:L', 35, alineacion)
            worksheet.set_column('M:M', 100, alineacion)
            worksheet.add_table(margenTabla,
                                {'total_row': 1, 'columns': [{'total_string': 'Total', 'header': 'No. Consulta'},
                                                             {'header': 'Nombre de la Imagen',
                                                              'total_function': 'count',
                                                              'format': numbersformat},
                                                             {'header': 'Conteo de Personas',
                                                              'total_function': 'sum',
                                                              'format': numbersformat},
                                                             {'header': 'Zonas con Aglomeraciones',
                                                              'total_function': 'sum',
                                                              'format': numbersformat},
                                                             {'header': 'Modelo Seleccionado'},
                                                             {'header': 'Hora'}, {'header': 'Fecha'},
                                                             {'header': 'Nombre de Mapa de Densidad'},
                                                             {'header': 'Nombre de Imagen Binaria'},
                                                             {'header': 'Nombre de Imagen Numerada'},
                                                             {'header': 'Nombre de Imagen con Contorno'},
                                                             {'header': 'Nombre de Mapa de Calor CV2'},
                                                             {'header': 'Ruta de Almacenamiento'}, ]})
            for i, row in enumerate(mysel):
                for j, value in enumerate(row):
                    if j == celdaConteo or j == celdaZonas:
                        worksheet.write(i + n, j, int(value))
                    else:
                        worksheet.write(i + n, j, value)
            workbook.close()
        except (ValueError, Exception):
            pass
