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

imagen = r'D:\Mayo28\Descargas\TrabajoDeGrado\CONSULTA_8.jpg'
modeloentrenado = 'Modelos Entrenados/Multitudes_Densas.pth.tar'
# modeloentrenado = 'Modelos Entrenados/Multitudes_Dispersas.pth.tar'
# modeloentrenado = 'Modelos Entrenados/Multitudes_Densas-Dispersas.pth.tar'
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
model = CSRNet()
model = model.cuda()
cargarModelo = torch.load(modeloentrenado)
model.load_state_dict(cargarModelo['state_dict'])
image = Image.open(imagen)
salida = model(transform(image.convert('RGB')).cuda().unsqueeze(0))
print("Aproximación de Personas: ", int(salida.detach().cpu().sum().numpy()))
img = model((image.convert('RGB')).cuda().unsqueeze(0))
MapaDensidad = np.array(salida.detach().cpu().reshape(img.detach().cpu().shape[2], img.detach().cpu().shape[3]))
MapaDensidad = rescale(MapaDensidad, 8, anti_aliasing=True)
plt.imshow(MapaDensidad, cmap='jet',vmin=0, vmax=0.04)
plt.show()


