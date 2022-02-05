import cv2
imagen = cv2.imread(r'C:\Users\ddzam\Downloads\TrabajoDeGrado\Mapas_De_Densidad\IMG_9_02-04-2021_16_17_46/IMG_9_Densidad.png', cv2.IMREAD_GRAYSCALE)
# im_gray = cv2.imread(r'C:\Users\ddzam\Downloads\TrabajoDeGrado\Mapas_De_Densidad\IMG_9_02-04-2021_16_17_46/IMG_9_Densidad.png', cv2.IMREAD_GRAYSCALE)
imagen = cv2.applyColorMap(imagen, cv2.COLORMAP_JET)
bordersize = 30
border = cv2.copyMakeBorder(
    imagen,
    top=bordersize,
    bottom=bordersize,
    left=bordersize,
    right=bordersize,
    borderType=cv2.BORDER_CONSTANT,
    value=[196, 0, 0]
)
# cv2.imshow('Imagen', imagen)
# cv2.imshow('bottom',bottom)
cv2.imshow('border', border)
cv2.imwrite('Map.png', border)
cv2.waitKey(0)
cv2.destroyAllWindows()
