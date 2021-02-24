import os
import cv2
from natsort import natsorted

rootImages = "Dataset/part_A_B/test_data/images/"  # Ruta de las images en el dataset.
dataImages = natsorted(os.listdir(rootImages))  # Lista a las imagenes dentro del dataset.

for i in range(len(dataImages)):  # Ejecutar por lotes (0,22) (22,25)(25,49)(49,182) len(dataImages)
    images = dataImages[i]
    imagen = cv2.imread(rootImages + images)
    grayscale = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("Dataset/part_A_B_gray/test_data/images/" + images, grayscale)
    print(images)
