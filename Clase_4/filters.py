import cv2
import numpy as np
import time

# Dirección de la imagen 
def getPath(): 
    path =  "Images/barras_cir.png" 
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

def main():
    imgColor =  getImage(getPath(), 1)
    imgGray = getImage(getPath(), 0)
    h, w = sizeImage(imgColor)

    #spatial filters
    imgFilteredMedia = cv2.blur(imgGray, (9,9))
    #imgFilteredMedian = cv2.medianBlur(imgGray, 9)

    # morfological filters
    #binarize img
    imgBinary = cv2.inRange(imgGray, 150, 240)
    #Define Kernel
    Kernel1 = np.ones((5, 9), np.uint8)
    imgDilate = cv2.dilate(imgBinary, kernel = Kernel1, iterations = 8)

    # filter erode
    #structured kernel
    Kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 6))
    imgErode = cv2.erode(imgGray, kernel = Kernel2, iterations = 1)
    imgFilteredMedian = cv2.medianBlur(imgErode, 9)


    #showImage("imgBinary", imgBinary)
    #showImage("imgDilate", imgDilate)
    #showImage("imgErode", imgErode)
    showImage("imgFilteredMedian", imgFilteredMedian)
    #showImage("imgGray", imgGray)
    cv2.waitKey(0)
    destroy()

if __name__=="__main__":
    main()