import cv2
import numpy as np
import time

def getPath():
    name = input("Ingrese el nombre de la imagen: ")
    path = "Images/" + name
    return path

def getImage(path, ch):
    image = cv2.imread(path,ch)
    return image

def showImage(nameW, img):
    cv2.imshow(nameW, img)

def destroy():
    cv2.destroyAllWindows()

def sizeImage(img):
    h,w = img.shape[:2]
    return h,w

def resize():
    measures = int(input("Ingrese el tamaño de imagen que desea (ancho, alto): ")) 
    measures = 

def main():
    imgColor = getImage(getPath(),1)
    


if __name__ == "__main__":
    main()