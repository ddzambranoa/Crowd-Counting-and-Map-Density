import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
imgDatabase = os.path.join(path, r'Recursos/database.png')
imgWarning = os.path.join(path, r"Recursos/Warning.png")
imgExit = os.path.join(path, r'Recursos/exit.png')


def cuadro_dialogo(titulo, texto, seticon, icono):
    messagebox = QMessageBox()
    messagebox.setIcon(seticon)
    messagebox.setWindowIcon(QIcon(icono))
    messagebox.setWindowTitle(titulo)
    aceptar = messagebox.addButton("Aceptar", QMessageBox.AcceptRole)
    messagebox.setText(texto)
    messagebox.setDefaultButton(aceptar)
    messagebox.exec_()
    return messagebox


def error_creacion():
    cuadro_dialogo("Error", "Base de datos no creada.", QMessageBox.Warning, imgDatabase)


def error_almacenamiento():
    cuadro_dialogo("Error", "Consulta no almacenada en el historial.", QMessageBox.Warning, imgDatabase)


def error_almacenamiento_txt():
    cuadro_dialogo("Error", "Consulta no almacenada en el archivo TXT.", QMessageBox.Warning, imgDatabase)


def error_visualizacion():
    cuadro_dialogo("Error", "Consulta no encontrada.", QMessageBox.Warning, imgDatabase)


def error_eliminacion():
    cuadro_dialogo("Error", "Consulta no eliminada de historial.", QMessageBox.Warning, imgDatabase)


def error_export_pdf():
    cuadro_dialogo("Error", "Cierre el archivo .PDF anteriormente exportado.", QMessageBox.Warning, imgDatabase)


def error_export_xlsx():
    cuadro_dialogo("Error", "Cierre el archivo .XLSX anteriormente exportado.", QMessageBox.Warning, imgDatabase)


def error_modelo():
    cuadro_dialogo("Error", "Falla en el sistema, compruebe las dimensiones de la imagen y el modelo entrenado de la "
                            "red neuronal convolucional.", QMessageBox.Warning, imgWarning)


def confirmacion_almacenamiento():
    cuadro_dialogo("Mensaje", "Consulta almacenada en el historial", QMessageBox.Information, imgDatabase)


def confirmacion_eliminacion():
    cuadro_dialogo("Mensaje", "Consulta eliminada de historial.", QMessageBox.Information, imgDatabase)


def close_event(event, titulo):
    messagebox = QMessageBox()
    messagebox.setWindowTitle("Salir")
    messagebox.setIcon(QMessageBox.Question)
    messagebox.setWindowIcon(QIcon(imgExit))
    messagebox.setText(titulo)
    si = messagebox.addButton("Si", QMessageBox.YesRole)
    no = messagebox.addButton("No", QMessageBox.AcceptRole)
    messagebox.setDefaultButton(si)
    messagebox.exec_()
    if messagebox.clickedButton() == si:
        event.accept()
    elif messagebox.clickedButton() == no:
        event.ignore()
