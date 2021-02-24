# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Nombre:           test.py
# Autor:            Daniel David Zambrano Andrade
# Creado:           13 de Enero 2020
# Modificado:       13 de Enero 2020
# Copyright:        Free
# License:          Free
# Versión Python:   3.8
# ----------------------------------------------------------------------------

import PIL.Image as Image
import numpy as np
from matplotlib import pyplot as plt
from model import CSRNet
import torch
from torchvision import transforms
from skimage.transform import rescale
import time

start = time.time()
I_mean_R = 0.30173253676484
I_mean_G = 0.32579306722701
I_mean_B = 0.33202998074239
I_std_R = 0.22317625513840
I_std_G = 0.20531329233443
I_std_B = 0.19716607821370

mean_R = 0.485
mean_G = 0.456
mean_B = 0.406
std_R = 0.229
std_G = 0.224
std_B = 0.225

N_mean_R = (I_mean_R + mean_R)/2
N_mean_G = (I_mean_G + mean_G)/2
N_mean_B = (I_mean_B + mean_B)/2

N_std_R = (I_std_R + std_R)/2
N_std_G = (I_std_G + std_G)/2
N_std_B = (I_std_B + std_B)/2

# print(N_mean_R)
# print(N_mean_G)
# print(N_mean_B)
# print()
# print(N_std_R)
# print(N_std_G)
# print(N_std_B)

# imagen = 'Dataset/part_B/test_data/images/IMG_205.jpg'
# imagen = '/home/daniel/TrabajoDeGrado/Dataset/part_B/test_data/images/IMG_1.jpg'
imagen = '/home/daniel/Downloads/Prueba4.jpg'
# imagen = '/home/daniel/Downloads/ImagenesPruebas/IMG_130.jpg'
# modeloentrenado = 'Modelos Entrenados/Multitudes_Densas.pth.tar'
modeloentrenado = 'Modelos Entrenados/Multitudes_Dispersas.pth.tar'
# modeloentrenado = 'Modelos Entrenados/Multitudes_Densas-Dispersas.pth.tar'
# mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
model = CSRNet().cuda()
cargarModelo = torch.load(modeloentrenado)
model.load_state_dict(cargarModelo['state_dict'])
image = Image.open(imagen)

salida = model(transform(image.convert('RGB')).cuda().unsqueeze(0))
print("Aproximación de Personas: ", int(salida.detach().cpu().sum().numpy()))


def NuevaSalidaNormalizada(norm):
    nuevatransformacion = model(norm(image.convert('RGB')).cuda().unsqueeze(0))
    # print("Aproximación de Personas: ", int(nuevatransformacion.detach().cpu().sum().numpy()))
    MapaDensidad = np.array(salida.detach().cpu().reshape(nuevatransformacion.detach().cpu().shape[2], nuevatransformacion.detach().cpu().shape[3]))
    MapaDensidad = rescale(MapaDensidad, 8, anti_aliasing=True)
    # print(MapaDensidad)
    # plt.imsave("Imagen2.png", MapaDensidad, cmap='coolwarm', vmin=0, vmax=0.07)
    plt.imshow(MapaDensidad, cmap='jet')
    end = time.time()
    tiempo = float(end - start)
    print("{:.2f}".format(round(tiempo, 2)))
    plt.show()


if modeloentrenado == 'Modelos Entrenados/Multitudes_Densas.pth.tar':
    if 0 <= int(salida.detach().cpu().sum().numpy()) < 49:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Multitud Densa Baja")
    elif 50 <= int(salida.detach().cpu().sum().numpy()) < 99:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Multitud Densa Media-Baja")
    elif 100 <= int(salida.detach().cpu().sum().numpy()) < 999:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Multitud Densa Media")
    elif 1000 <= int(salida.detach().cpu().sum().numpy()) < 9999:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Multitud Densa")

if modeloentrenado == 'Modelos Entrenados/Multitudes_Dispersas.pth.tar':
    if 0 <= int(salida.detach().cpu().sum().numpy()) < 49:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Multitud Dispersa Baja")
    elif 50 <= int(salida.detach().cpu().sum().numpy()) < 99:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Multitud Dispersa Media")
    elif 100 <= int(salida.detach().cpu().sum().numpy()) < 999:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Multitud Dispersa Alta")

if modeloentrenado == 'Modelos Entrenados/Multitudes_Densas-Dispersas.pth.tar':
    if 0 <= int(salida.detach().cpu().sum().numpy()) < 49:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Modelo Multitudes Densas-Dispersas Baja")
    elif 50 <= int(salida.detach().cpu().sum().numpy()) < 99:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Modelo Multitudes Densas-Dispersas Media")
    elif 100 <= int(salida.detach().cpu().sum().numpy()) < 999:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Modelo Multitudes Densas-Dispersas Alta")
    elif 1000 <= int(salida.detach().cpu().sum().numpy()) < 9999:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        NuevaSalidaNormalizada(transform)
        print("Modelo Multitudes Densas-Dispersas Alta")
