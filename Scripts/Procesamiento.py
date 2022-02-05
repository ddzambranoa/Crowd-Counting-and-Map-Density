from time import strftime, time
import cv2
import numpy as np
import torch
from PIL import Image
from matplotlib import pyplot as plt
from skimage.transform import rescale
from torchvision import transforms
from Scripts.BD_almacenarDatos import almacenarDatos
from Scripts.BD_crearContenedores import ruta_de_almacenamiento
from Scripts.cuadrosDialogos import *
from model import CSRNet
import locale

locale.setlocale(locale.LC_TIME, '')
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
imgFondo = os.path.join(path, r'Recursos/Blanco')
modDispersas = os.path.join(path, r'Modelos Entrenados/Multitudes_Dispersas.pth.tar')
modDensas = os.path.join(path, r'Modelos Entrenados/Multitudes_Densas.pth.tar')
modCombinadas = os.path.join(path, r'Modelos Entrenados/Multitudes_Densas-Dispersas.pth.tar')
carpModelos = os.path.join(path, r'Modelos Entrenados/')
carpMapas = os.path.join(path, r'Mapas_De_Densidad/')
carpGuardar = os.path.join(path, r'')
carpDB = os.path.join(path, r'Database/')
global use_cuda, img, start_time, cv_img, img_mapa, aproximacion, zonas, busqueda_contornos, conteo, modeloentrenado


def procesar(name, multitudes, file):
    try:

        _time = time()
        verificar_modelo = comprobar_modelos(multitudes)
        cuda_or_cpu = comprobar_cuda(name, verificar_modelo)
        predecir = predecir_aproximacion(cuda_or_cpu)
        almacenar_en_ruta = ruta_de_almacenamiento(file)
        generar_mapa_densidad(cuda_or_cpu, almacenar_en_ruta)
        binarizacion = binarizar(name, almacenar_en_ruta)
        busqueda_contorno = encontrar_contornos(binarizacion[3])
        dibujar_contorno(busqueda_contorno[0], binarizacion[1], binarizacion[2])
        cv_guardar_imagen(almacenar_en_ruta, binarizacion)
        elapsed_time = round(((time() - _time) + 1)) * 10
        print("elapsed_time: " + str(int(elapsed_time)))
        almacenar_informacion = enviar_a_database(almacenar_en_ruta, predecir, busqueda_contorno, verificar_modelo)
        return almacenar_informacion[0], almacenar_informacion[1], almacenar_informacion[2]
    except (ValueError, Exception):
        error_modelo()


def comprobar_modelos(multitudes):
    global modeloentrenado
    try:
        try:
            os.stat(carpModelos)
        except (ValueError, Exception):
            os.mkdir(carpModelos)
        if multitudes == "Multitudes Dispersas":
            modeloentrenado = modDispersas
        elif multitudes == "Multitudes Densas":
            modeloentrenado = modDensas
        elif multitudes == "Multitudes Combinadas":
            modeloentrenado = modCombinadas
        else:
            modeloentrenado = modDispersas
    except (ValueError, Exception):
        pass
    return multitudes, modeloentrenado


def comprobar_cuda(name, verificar_modelo):
    global use_cuda, img
    use_cuda = torch.cuda.is_available()
    if use_cuda:
        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        model = CSRNet()
        model = model.cuda()
        checkpoint = torch.load(verificar_modelo[1])
        model.load_state_dict(checkpoint['state_dict'])
        img = transform(Image.open(name).convert('RGB')).cuda()
    else:
        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
        model = CSRNet()
        checkpoint = torch.load(verificar_modelo[1], map_location=torch.device('cpu'))
        model.load_state_dict(checkpoint['state_dict'])
        img = transform(Image.open(name).convert('RGB'))
    output = model(img.unsqueeze(0))
    return img, output


def generar_mapa_densidad(cuda_or_cpu, almacenar_en_ruta):
    try:
        gen_mapa_densidad = np.asarray(
            cuda_or_cpu[1].detach().cpu().reshape(cuda_or_cpu[1].detach().cpu().shape[2],
                                                  cuda_or_cpu[1].detach().cpu().shape[3]))
        gen_mapa_densidad = rescale(gen_mapa_densidad, 8, anti_aliasing=True)
        plt.imsave(almacenar_en_ruta[0], gen_mapa_densidad, cmap='jet', vmin=0, vmax=0.07)
    except (ValueError, Exception):
        pass


def predecir_aproximacion(cuda_or_cpu):
    global conteo
    try:
        conteo = str(int(cuda_or_cpu[1].detach().cpu().sum().numpy()))
    except (ValueError, Exception):
        pass
    return conteo


def binarizar(name, almacenar_en_ruta):
    hsv_rojo_bajo_lim_inf = np.array([0, 50, 20], np.uint8)
    hsv_rojo_alto_lim_inf = np.array([30, 255, 255], np.uint8)
    hsv_rojo_bajo_lim_sup = np.array([150, 50, 20], np.uint8)
    hsv_rojo_alto_lim_sup = np.array([180, 255, 255], np.uint8)
    imagen = cv2.imread(almacenar_en_ruta[0])
    imagen_2 = cv2.imread(almacenar_en_ruta[0])
    imagen_o = cv_imread(name)
    bordersize = 30
    imagen = cv2.copyMakeBorder(imagen, top=bordersize, bottom=bordersize, left=bordersize,
                                right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[127, 0, 0])
    imagen_2 = cv2.copyMakeBorder(imagen_2, top=bordersize, bottom=bordersize, left=bordersize,
                                  right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[127, 0, 0])
    imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    masc_rojo_inf = cv2.inRange(imagen_hsv, hsv_rojo_bajo_lim_inf, hsv_rojo_alto_lim_inf)
    masc_rojo_sup = cv2.inRange(imagen_hsv, hsv_rojo_bajo_lim_sup, hsv_rojo_alto_lim_sup)
    masc_rojo = cv2.add(masc_rojo_inf, masc_rojo_sup)
    return imagen_o, imagen, imagen_2, masc_rojo


def encontrar_contornos(masc_rojo):
    global busqueda_contornos
    try:
        busqueda_contornos = cv2.findContours(masc_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    except (ValueError, Exception):
        pass
    return busqueda_contornos


def dibujar_contorno(contornos, imagen, imagen_2):
    try:
        for (i, c) in enumerate(contornos):
            m = cv2.moments(c)
            if m["m00"] != 0:
                x = int(m["m10"] / m["m00"])
                y = int(m["m01"] / m["m00"])
            else:
                x, y = 0, 0
            cv2.drawContours(imagen, [c], 0, (0, 0, 255), 2)
            cv2.drawContours(imagen_2, [c], 0, (0, 255, 255), 4)
            cv2.putText(imagen, str(i + 1), (x, y), 5, 1, (0, 0, 0), 2)
    except (ValueError, Exception):
        pass


def cv_imread(filepath):
    global cv_img
    try:
        cv_img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), -1)
    except (ValueError, Exception):
        pass
    return cv_img


def cv_guardar_imagen(almacenar_en_ruta, binarizacion):
    try:
        cv2.imwrite(almacenar_en_ruta[1], binarizacion[0])
        cv2.imwrite(almacenar_en_ruta[2], binarizacion[3])
        cv2.imwrite(almacenar_en_ruta[3], binarizacion[1])
        cv2.imwrite(almacenar_en_ruta[4], binarizacion[2])
        cv2.imwrite(almacenar_en_ruta[5], cv2.applyColorMap(binarizacion[2], cv2.COLORMAP_JET))
    except (ValueError, Exception):
        pass


def enviar_a_database(almacenar_en_ruta, predecir, busqueda_contorno, verificar_modelo):
    global img_mapa, aproximacion, zonas
    try:
        img_mapa = str(almacenar_en_ruta[4])
        imagen_original = os.path.basename(almacenar_en_ruta[1])
        aproximacion = str(predecir)
        zonas = str(len(busqueda_contorno[0]))
        modelo = verificar_modelo[0]
        hora = str(strftime("%H:%M:%S"))
        fechas = str(strftime("%B %d, %Y").capitalize())
        mapa_de_densidad = str(os.path.basename(almacenar_en_ruta[0]))
        imagen_binaria = str(os.path.basename(almacenar_en_ruta[2]))
        imagen_numerada = str(os.path.basename(almacenar_en_ruta[3]))
        imagen_contorno = str(os.path.basename(almacenar_en_ruta[4]))
        mapa_cv2 = str(os.path.basename(almacenar_en_ruta[5]))
        ruta = str(almacenar_en_ruta[6])
        almacenarDatos(imagen_original, aproximacion, zonas, modelo, hora, fechas, mapa_de_densidad, imagen_binaria,
                       imagen_numerada, imagen_contorno, mapa_cv2, ruta)
    except (ValueError, Exception):
        pass
    return img_mapa, aproximacion, zonas
