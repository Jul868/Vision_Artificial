import numpy as np
import cv2 

cont = 0
distancia = 0
pixel = 0
pixel2 = 0 

# Dirección de la imagen 
def getPath(): 
    path =  "images/barras.png" 
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

# Obtener imagen recortada (región de interés)
def getRoi(x1,y1,x2,y2, img):
    imgRoi = img[y1:y2,x1:x2] 
    return imgRoi

# Binarizar una imagen: convertirla a blanco y negro (cada pixel se clasifica como blanco o negro basándose en un umbral)
def binaryImg(imgGray, u):
    ret, imgBinary = cv2.threshold(imgGray, u, 255, cv2.THRESH_BINARY) 
    return imgBinary 

# Una función que no hace nada literalmente
def nothing(x):
    pass

def main():
    global cont, distancia, pixel, pixel2

    imgColor = getImage(getPath(),1)
    imgGray = getImage(getPath(),0)

    h, w = sizeImage(imgColor)

    imgBinary = binaryImg(imgGray, 200)
    showImage("imgBinary",imgBinary)


    for col in range(0, w):
        if cont == 2:
            if imgBinary[round(h/2), col] == 255 and imgBinary[round(h/2), col-1] == 0:
                pixel2 = col
            elif imgBinary[round(h/2), col] == 0 and imgBinary[round(h/2), col-1] == 255: 
                pixel = col 

        if imgBinary[round(h/2), col] == 255 and imgBinary[round(h/2), col-1] == 0:
            cont += 1


    barras = cont
    distanciaProm = pixel2 - pixel
    print("Número de barras:", barras)
    print("La distancia promedio entre barras es de {} pixeles".format(distanciaProm))

    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__=="__main__":
    main()
