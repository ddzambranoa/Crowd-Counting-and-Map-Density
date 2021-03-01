# Estimación de Densidad de Multitudes de Personas a Través de Visión Por Computador

Sistema basado en la versión de CSRNet escrita en PyTorch del artículo [CSRNet: Dilated Convolutional Neural Networks for Understanding the Highly Congested Scenes].

# Datasets

El siguiente conjunto de datos fue modificado para realizar pruebas a escala de grises y la combinación de multitudes.

  - [ShanghaiTech Dataset Modificado].
 
  - [ShanghaiTech Dataset Original].

# Requisitos de Hardware

  - Tarjeta Gráfica Nvidia GTX 1050 4GB o Superior.

# Requisitos de Software

  - Ubuntu: 20.10. 
    - [Link de descarga Ubuntu 20.10].
  - Python: 3.8 o Superior.
    - Lenguaje de programación instalado en Ubuntu 20.10.
  - CUDA: 11.1.74 o Superior.
    - [Link de descarga e instalación].
  - PyCharm.
    -  [Link de descarga IDE]

  **Instalación de Bibliotecas de Python3**

```sh
sudo pip3 install -r requirements.txt
```
  
# Entrenamiento

Para iniciar el entrenamiento emplear el siguiente comando en la terminal:
```sh
python3 train.py train.json val.json 0 0
```
En caso de interrupción del entrenamiento emplear el siguiente comando en la terminal:
```sh
python3 train.py -p 0checkpoint.pth.tar train.json val.json 0 0
```
  ***Asegurese que los archivos .json tengan el mismo nombre que en el comando***
  
# Modelos Entrenados

  - [Modelo Multitudes Densas].
  - [Modelo Multitudes Dispersas].
  - [Modelo Combinación Multitudes Densas y Dispersas].

# Implementación

Si desea utilizar este sistema deberá clonar este repositorio y ejecutar el script InterfazGrafica.py. Asegure tener instalado todas las bibliotecas empleadas en cada script.

# Referencias
Utilización del código fuente con permiso de los siguientes autores:

CSRNet: Dilated convolutional neural networks for understanding the highly congested scenes.

```sh
@inproceedings{li2018csrnet,
  title={CSRNet: Dilated convolutional neural networks for understanding the highly congested scenes},
  author={Li, Yuhong and Zhang, Xiaofan and Chen, Deming},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  pages={1091--1100},
  year={2018}}
```

ShanghaiTech Dataset: Single-image crowd counting via multi-column convolutional neural network
  
```sh
@inproceedings{zhang2016single,
  title={Single-image crowd counting via multi-column convolutional neural network},
  author={Zhang, Yingying and Zhou, Desen and Chen, Siqin and Gao, Shenghua and Ma, Yi},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={589--597},
  year={2016}}
```

   [PyTorch]: <https://github.com/leeyeehoo/CSRNet-pytorch/tree/master>
   [CSRNet: Dilated Convolutional Neural Networks for Understanding the Highly Congested Scenes]: <https://arxiv.org/abs/1802.10062>
   [ShanghaiTech Dataset Original]: <https://www.kaggle.com/tthien/shanghaitech-with-people-density-map>
   [ShanghaiTech Dataset Modificado]: <https://drive.google.com/drive/folders/1lxkuwtL1e0vdKTJG1pJbTK8DpENKN6CX?usp=sharing>
   [Modelo Multitudes Densas]: <https://drive.google.com/file/d/1rrI4ihhroJsLmJ0FY1NokfsmIwti71t_/view?usp=sharing>
   [Modelo Multitudes Dispersas]: <https://drive.google.com/file/d/1iFhVVBF-GwErBH9FAqM77cU23iJ2iUPC/view?usp=sharing>
   [Modelo Combinación Multitudes Densas y Dispersas]: <https://drive.google.com/file/d/1z5BkYcCFAmX-AFTeNcL6f54J9DRwLdXL/view?usp=sharing>
   [Link de descarga e instalación]: <https://developer.nvidia.com/cuda-downloads>
   [Link de descarga Ubuntu 20.10]: <https://ubuntu.com/download/desktop>
   [Link de descarga IDE]: <https://www.jetbrains.com/es-es/pycharm/>
