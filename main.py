# -*- coding: utf-8 -*-
# !/usr/bin/env python3

# ----------------------------------------------------------------------------
# Estimación de Densidad de Personas a través de Visión por Computador
# Archivo:      main.py
# Autor:        Daniel David Zambrano Andrade
# Creado:       25 de Septiembre 2020
# Modificado:   19 de Abril 2021
# Copyright:    Libre
# License:      Libre
# ----------------------------------------------------------------------------

import sys
from PyQt5.QtWidgets import QApplication
from Scripts.Opt_Carga import iniciarPrograma
from Scripts.setup import stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    main = iniciarPrograma()
    main.show()
    sys.exit(app.exec_())