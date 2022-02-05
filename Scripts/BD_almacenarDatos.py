import sqlite3
from Scripts.BD_crearBD import crearDatabase
from Scripts.BD_exportarExcel import ExportEXCEL
from Scripts.BD_exportarPDF import ExportPDF
from Scripts.cuadrosDialogos import *

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
dbConsultas = os.path.join(path, r'Database/Consultas.db')
imgDatabase = os.path.join(path, r'Recursos/database.png')


def almacenarDatos(ImagenOriginal, Aproximacion, Zona, Modelo, Hora, Fecha, MapaDeDensidad, ImagenBinaria, ImagenNumerada, ImagenContorno, MapaCV2, Ruta):
    try:
        crearDatabase()
        ExportPDF()
        ExportEXCEL()
        conn = sqlite3.connect(dbConsultas)
        c = conn.cursor()
        c.execute(
            "INSERT INTO historial (ImagenOriginal, Aproximacion, Zona, Modelo, Hora, Fecha,  MapaDeDensidad, "
            "ImagenBinaria,ImagenNumerada, ImagenContorno, MapaCV2, Ruta) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (ImagenOriginal, Aproximacion, Zona, Modelo, Hora, Fecha, MapaDeDensidad, ImagenBinaria, ImagenNumerada,
             ImagenContorno, MapaCV2, Ruta))
        conn.commit()
        c.close()
        conn.close()
        try:
            crearTXT(Ruta, ImagenOriginal, Aproximacion, Zona, Modelo, Hora, Fecha, MapaDeDensidad, ImagenBinaria,
                     ImagenNumerada, ImagenContorno, MapaCV2)
        except (ValueError, Exception):
            error_almacenamiento_txt()
        # confirmacion_almacenamiento()
    except (ValueError, Exception):
        error_almacenamiento()


def crearTXT(Ruta, ImagenOriginal, Aproximacion, Zona, Modelo, Hora, Fecha, MapaDeDensidad, ImagenBinaria,
             ImagenNumerada, ImagenContorno, MapaCV2):
    file = open(Ruta + "/Resumen.txt", "w")
    file.write("Nombre de la imagen: " + ImagenOriginal + os.linesep)
    file.write("Aproximación de personas: " + str(Aproximacion) + os.linesep)
    file.write("Zonas de posibles aglomeraciones: " + str(Zona) + os.linesep)
    file.write("Modelo seleccionado: " + Modelo + os.linesep)
    file.write("Hora de consulta: " + Hora + os.linesep)
    file.write("Fecha de consulta: " + Fecha + os.linesep)
    file.write("Nombre del mapa de densidad: " + MapaDeDensidad + os.linesep)
    file.write("Nombre de la imagen binaria: " + ImagenBinaria + os.linesep)
    file.write("Nombre de la imagen numerada: " + ImagenNumerada + os.linesep)
    file.write("Nombre de la imagen con contorno: " + ImagenContorno + os.linesep)
    file.write("Nombre del mapa de densidad de openCV: " + MapaCV2 + os.linesep)
    file.write("Ruta de la carpeta contenedora: " + Ruta + os.linesep)
    file.close()
