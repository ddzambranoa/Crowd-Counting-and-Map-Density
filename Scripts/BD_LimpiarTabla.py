import os
import sys
from pathlib import Path
from Scripts.BD_crearBD import crearDatabase
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
dbConsultas = os.path.join(path, r'Database/Consultas.db')


def eliminar_tabla():
    os.remove(dbConsultas)
    crearDatabase()

