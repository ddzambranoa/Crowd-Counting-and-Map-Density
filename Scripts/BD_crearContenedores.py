import os
import sqlite3
import sys
from pathlib import Path
from time import strftime
from Scripts.BD_crearBD import crearDatabase

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
dbConsultas = os.path.join(path, r'Database/Consultas.db')
carpMapas = os.path.join(path, r'Mapas_De_Densidad/')
global fecha


def ultimaConsulta():
    try:
        crearDatabase()
        con = sqlite3.connect(dbConsultas)
        c = con.cursor()
        c.execute("SELECT * FROM historial ORDER BY roll DESC LIMIT 1")
        consulta = c.fetchone()
        con.commit()
        c.close()
        con.close()
        return consulta[0]
    except (ValueError, Exception):
        pass


def cambiarNombre(pathFile, file_name):
    n = ultimaConsulta()

    if n is None:
        n = 0
    else:
        pass
    new_name = pathFile + "/CONSULTA_" + str(n) + ".jpg"
    os.rename(file_name, new_name)
    return new_name


def ruta_de_almacenamiento(file):
    try:
        os.stat(carpMapas)
    except (ValueError, Exception):
        os.mkdir(carpMapas)
    fechaConsulta = str(strftime("%B-%d-%Y_%H_%M_%S")).capitalize()
    rootMapas = path + "/Mapas_De_Densidad/" + str(file) + "_" + fechaConsulta
    try:
        os.stat(rootMapas)
    except (ValueError, Exception):
        os.mkdir(rootMapas)
    rootArchivo = rootMapas + "/" + str(file)
    Img_O = rootArchivo + ".png"
    rootMap = rootArchivo + "_Densidad" + ".png"
    Zona_B = rootArchivo + "_Binaria" + ".png"
    Zona_N = rootArchivo + "_Numerada" + ".png"
    Zona_C = rootArchivo + "_Contorno" + ".png"
    IMG_CV2JET = rootArchivo + "_Mapa_Calor" + ".png"
    return rootMap, Img_O, Zona_B, Zona_N, Zona_C, IMG_CV2JET, rootMapas


