import sqlite3
from Scripts.cuadrosDialogos import *

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
dbConsultas = os.path.join(path, r'Database/Consultas.db')
carpDB = os.path.join(path, r'Database/')
imgDatabase = os.path.join(path, r'Recursos/database.png')


def crearDatabase():
    try:
        try:
            os.stat(carpDB)
        except (ValueError, Exception):
            os.mkdir(carpDB)
        conn = sqlite3.connect(dbConsultas)
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS historial(roll INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,ImagenOriginal TEXT,"
            "Aproximacion TEXT,Zona TEXT, Modelo TEXT, Hora TEXT, Fecha Text,  MapaDeDensidad TEXT, ImagenBinaria TEXT,"
            "ImagenNumerada TEXT, ImagenContorno TEXT, MapaCV2 TEXT, Ruta TEXT)")

    except (ValueError, Exception):
        error_creacion()
