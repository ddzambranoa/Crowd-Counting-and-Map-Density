import os
import shutil

from PIL import Image


def promedio_peso():
    root = str(r'D:\archive\ShanghaiTech\part_B\test_data\images')
    data = os.listdir(root)
    pesos = []
    for i in range(len(data)):
        file_stats = os.stat(root + '/' + data[i])
        peso = file_stats.st_size
        pesos.append(peso)
    print(len(data))
    promedio = ((sum(pesos)/len(data)) / 1024)
    suma = (sum(pesos) / 1024)
    print(suma)
    print(promedio)


def jpg_to_png():
    try:
        root = str(r'C:\Users\ddzam\Downloads\Train\Persona')
        data = os.listdir(root)
        for i in range(len(data)):
            file_stats = data[i]
            name_root = (root + '/' + str(file_stats))
            file = os.path.splitext(file_stats)[0]
            print(file)
            # suma = 965+i
            im1 = Image.open(name_root)
            im1.save(r'C:\Users\ddzam\Downloads\Train\Persona' + '/' + str(i) + '.png')
    except ValueError:
        pass


def size_image():
    try:
        root = str(r'D:\archive\ShanghaiTech\part_B\test_data\images2')
        data = os.listdir(root)
        for i in range(len(data)):
            file_stats = data[i]
            name_root = (root + '/' + str(file_stats))
            image = Image.open(name_root).convert('RGB')
            width, height = image.size
            print(width, height)
    except ValueError:
        pass


def change_size_image():
    try:
        ruta = str(r'C:\Users\ddzam\Downloads\1024x768')
        listcont = os.listdir(ruta)
        for i in range(len(listcont)):
            file_stats = listcont[i]
            name_root = (ruta + '/' + str(file_stats))
            image = Image.open(name_root).convert('RGB')
            resized_image = image.resize((1024, 768))
            width, height = image.size
            resized_image.save(r'C:\Users\ddzam\Downloads\1000x1000' + '/' + str(i) + '.png')
            print(width, height)
    except ValueError:
        pass


def files():
    try:
        root = str(r'F:\Nueva carpeta')
        data = os.listdir(root)
        for i in range(len(data)):
            file_stats = data[i]
            print(i)
            file = os.path.splitext(file_stats)[0]
            print(file)
    except ValueError:
        pass


def change_name_image():
    try:
        ruta = str(r'D:\archive\shanghaitech_with_people_density_map\ShanghaiTech\part_A\test_data\ground-truth-h5')
        listcont = os.listdir(ruta)

        for i in range(len(listcont)):
            nameNumber = 317 + i

            file_stats = listcont[i]
            file = os.path.splitext(file_stats)[0]
            name_root = (ruta + '/' + str(file_stats))
            print(name_root)
            shutil.copy(str(name_root), r'D:\Mayo28\Descargas\TrabajoDeGrado\Conjunto de '
                                        r'Datos\Combinacion\Pruebas\Etiquetas' +
                        '/' + "IMG_" + str(nameNumber) + '.h5')

            # image = open(name_root)
            # image.save(r'D:\Mayo28\Descargas\TrabajoDeGrado\Conjunto de Datos\Combinacion\Pruebas\Etiquetas' +
            #            '/' + "GT_IMG_" + str(nameNumber) + '.mat')
    except ValueError:
        pass

change_name_image()