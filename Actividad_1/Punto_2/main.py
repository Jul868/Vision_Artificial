import numpy as np
import cv2 
import math

bandClick = False
cont = 0
x2 = 0
y2 = 0 
pixel_blanco = 0
pixel_blanco_roi = 0

# Dirección de la imagen 
def getPath(): 
    path =  "images/monedas.jpg" 
    return path

# Leer la imagen y definir si la quierp a color o a escala de grises con 1 y 0
def getImage(path, ch): 
    image = cv2.imread(path, ch) 
    return image

# Mostrar imagen
def showImage(nameW, img):  
    cv2.imshow(nameW, img) 

# Cerrar ventanas 
def destroy(): 
    cv2.destroyAllWindows()

# Obtener el largo y el ancho de la imagen 
def sizeImage(img): 
    h,w = img.shape[:2]
    return h,w

# Obtener las coordenadas del mouse cuando se haga clik en un punto específico
def mouseClick(event,x,y,flags,param):  
    global x1,y1,x2,y2,bandClick
    if(event == cv2.EVENT_LBUTTONDOWN):
        x1 = x
        y1 = y
    elif(event == cv2.EVENT_LBUTTONUP):
        x2 = x
        y2 = y
        bandClick = True # Bandera
    return x2, y2

# Obtener imagen recortada (región de interés)
def getRoi(x1,y1,x2,y2, img):
    imgRoi = img[y1:y2,x1:x2] 
    return imgRoi

# Binarizar una imagen: convertirla a blanco y negro (cada pixel se clasifica como blanco o negro basándose en un umbral)
def binaryImg(imgGray, u):
    ret, imgBinary = cv2.threshold(imgGray, u, 255, cv2.THRESH_BINARY_INV) 
    return imgBinary 

# Binarizar imagen en un rango
def binaryImg_range (imgGray, u1, u2):
    imgBin = cv2.inRange(imgGray, u1, u2)
    return imgBin 

# Una función que no hace nada literalmente
def nothing(x):
    pass

def main():
    global x2, y2, bandClick, cont, pixel_blanco, pixel_blanco_roi

    imgColor = getImage(getPath(), 1)
    imgGray = getImage(getPath(), 0)

    cv2.namedWindow("imgBinary")
    cv2.setMouseCallback("imgBinary", mouseClick)
    imgBinary = binaryImg_range(imgGray, 0, 190)

    h, w = sizeImage(imgBinary) 
    for row in range(0,h):
            for col in range(0,w):
                if imgBinary[row,col] == 255:
                    pixel_blanco +=1 

    while True:
        showImage("imgColor", imgColor)
        showImage("imgGray", imgGray)
        showImage("imgBinary", imgBinary)

        if (bandClick):
            imgRoi = getRoi(x1,y1,x2,y2,imgBinary)
            showImage("imgRoi", imgRoi)
            bandClick = False
        
            h1, w1 = sizeImage(imgRoi)
            for row in range(0,h1):
                for col in range(0,w1):
                    if imgRoi[row,col] == 255:
                        pixel_blanco_roi += 1

        if pixel_blanco_roi > 0:
            monedas = round(pixel_blanco/pixel_blanco_roi)
            tamaño = round(math.sqrt(pixel_blanco_roi),0)

            # Escribir en la imagen 
            texto = "Se tienen aproximadamente {} monedas".format(monedas)
            texto2 = "con un tamano aproximado de {}x{} pixeles".format(tamaño,tamaño)
            posicion = (20,305) # coordenadas
            posicion2 = (20,320)
            fuente = cv2.FONT_HERSHEY_SIMPLEX
            escala = 0.4
            color = (255,255,255)
            grosor = 1
            cv2.putText(imgBinary,texto,posicion,fuente,escala,color,grosor)
            cv2.putText(imgBinary,texto2,posicion2,fuente,escala,color,grosor)
            showImage("imgBinary", imgBinary)

        elif pixel_blanco_roi == 0:
            nothing

        if(cv2.waitKey(1) & 0xFF == ord('q')): 
            break
    
    destroy()


if __name__=="__main__":
    main()