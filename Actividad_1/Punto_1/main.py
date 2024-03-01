import numpy as np
import cv2 

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
    imgColor = getImage(getPath(),1)
    imgGray= getImage(getPath(),0)
    cv2.namedWindow("imgColor")
    cv2.namedWindow("imgGray")
    showImage("imgColor", imgColor)
    showImage("imgGray", imgGray)

    # Umbrales 
    moneda_1 = [0,94]
    moneda_2 = [95,121]
    moneda_3 = [121,200]

    h,w = sizeImage(imgGray)

    for row in range(h-1):
        for col in range(w-1):
            if imgGray[row,col] >= moneda_1[0] and imgGray[row,col] <= moneda_1[1]:
                imgGray[row,col] = 0
                imgColor[row,col] = [0,0,255]
            elif imgGray[row,col] >= moneda_2[0] and imgGray[row,col] <= moneda_2[1]:
                imgGray[row,col] = 100
                imgColor[row,col] = [0,255,0]
            elif imgGray[row,col] >= moneda_3[0] and imgGray[row,col] <= moneda_3[1]:
                imgGray[row,col] = 255
                imgColor[row,col] = [255,0,0]

    showImage("imgGray", imgGray)
    showImage("imgColor", imgColor)
    cv2.waitKey()


if __name__=="__main__":
    main()


