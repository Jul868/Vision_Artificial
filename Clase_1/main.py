import numpy as np
import cv2

path = "images/bear.png"

imgColor = cv2.imread(path,1)
imgGray = cv2.imread(path,0)


h,w = imgColor.shape[:2]
newImgColor=np.zeros_like(imgColor)
#print(imgColor[h-1,w-1]) # el eror index 221 is put of bounds significa que me pase del tamaño de la imagen

#Primer Ejemplo: Pintar la imagen solo si el pixel cumple con el color verde mayor a 100 bits

"""for a in range (0,h):
    for b in range (0,w):
        if imgColor[a,b,1] <= 100:
            print(imgColor[a,b])
            imgColor[a,b]=(255,255,255)
cv2.imshow("imgColor", imgColor)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
            


#Segundo Ejemplo: Borrar o pintar como negro aquellos pixeles que tenga un color verde menor o igual a 100bits

"""for a in range (0,h):
    for b in range (0,w):
        if imgColor[a,b,1] <= 100:
            print(imgColor[a,b])
            imgColor[a,b] = (0,0,0)

cv2.imshow("imgColor", imgColor)
cv2.waitKey(0)
cv2.destroyAllWindows()"""


# Se usa para cerrar todas las ventas que se hallan generado
