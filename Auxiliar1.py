import os
import h5py
from natsort import natsorted
import PIL.Image as Image
from model import CSRNet
import torch
from torchvision import transforms
import numpy as np

rootImages = "Dataset/part_A/test_data/images/"  # Ruta de las images en el dataset.
rootGroundTruth = "Dataset/part_A/test_data/ground_truth/"  # Ruta de las images en el dataset.
dataImages = natsorted(os.listdir(rootImages))  # Lista a las imagenes dentro del dataset.

for i in range(0, len(dataImages)):
    images = dataImages[i]
    dataGT = dataImages[i].replace('.jpg', '.h5')
    groundRoot = rootGroundTruth + dataGT
    imagen = rootImages + images
    print(imagen)

    modeloentrenado = 'Modelos Entrenados/Multitudes_Densas.pth.tar'
    # modeloentrenado = 'Modelos Entrenados/Multitudes_Dispersas.pth.tar'
    # modeloentrenado = 'Modelos Entrenados/Multitudes_Densas-Dispersas.tar'
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
    model = CSRNet().cuda()
    cargarModelo = torch.load(modeloentrenado)
    model.load_state_dict(cargarModelo['state_dict'])
    image = Image.open(imagen)
    salida = model(transform(image.convert('RGB')).cuda().unsqueeze(0))
    print(int(salida.detach().cpu().sum().numpy()))
    groundtruth = h5py.File(groundRoot, 'r')
    groundtruth = np.asarray(groundtruth['density'])
    print(int(np.sum(groundtruth)))
