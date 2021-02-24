# -*- coding: utf-8 -*-
# !/usr/bin/python

# Version: 1.0
# Author: Daniel Zambrano <ddzambranoa@utn.edu.ec>
# Year: 2020
# Create .json files from datasets, 20% Dataset for validation, 80% Dataset for Train

import random
import os


class dataset:
    def __init__(self):
        self.root = "/home/daniel/TrabajoDeGrado/Dataset/part_A/test_data/images/"  # Ruta del dataset general.
        self.data = sorted(os.listdir(self.root))  # Lista a los elementos dentro del dataset general.
        self.percentage = 0
        self.train_data = []
        self.Val_data = []
        self.listDatasetTrain = []
        self.listDatasetValidation = []
        self.datasetValidation = ""
        self.datasetTrain = ""
        self.fileDatasetTrain = ""

    def makeDataset(self):
        random.shuffle(self.data)  # Mezcla aleatoriamente a los elementos del dataset general.
        self.percentage = round(len(self.data) * 0.2)  # Porcentaje de elementos para el dataset de validación 20%.

        self.datasetTrain = open("datasetTrain.json", "w")  # Crea un archivo .json para almacenar los archivos para el dataset de entrenamiento.
        self.train_data = self.data[:len(self.data)-self.percentage]  # Guarda n elementos a una lista.  (Diferentes y no repetitivos entre datasets)
        for i in self.train_data:  # Ciclo para recorrer cada elemento dentro de la lista.
            self.listDatasetTrain.append(self.root + i)  # Almacena en otra lista los elementos guardados en cada posición i, agregando la ruta de la carpeta del dataset general.
        self.datasetTrain.write(str(self.listDatasetTrain).replace("'", '"'))  # Escribe dentro del archivo .json la dirección donde está ubicado cada elemento.

        self.datasetValidation = open("datasetValidation.json", "w")  # Crea un archivo .json para almacenar los archivos para el dataset de validación.
        self.Val_data = self.data[(len(self.data) - self.percentage):]  # Guarda n elementos a una lista. (Diferentes y no repetitivos entre datasets)
        for j in self.Val_data:   # Ciclo para recorrer cada elemento dentro de la lista.
            self.listDatasetValidation.append(self.root + j)  # Almacena en otra lista los elementos guardados en cada posición j, agregando la ruta de la carpeta del dataset general.
        self.datasetValidation.write(str(self.listDatasetValidation).replace("'", '"'))  # Escribe dentro del archivo .json la dirección donde está ubicado cada elemento.


datasets = dataset()
datasets.makeDataset()
