import numpy as np
import cv2

path = "images/bear.png"

imgColor = cv2.imread(path,1)
imgGray = cv2.imread(path,0)


h,w = imgColor.shape[:2] # Se obtiene el tamaño de la imagen en pixeles (alto, ancho)
newImgColor=np.zeros_like(imgColor)
R, G, B = cv2.split(imgColor) # Se obtienen los canales de color de la imagen
# Se crea una imagen con los canales de color separados
imgColor = cv2.merge((R,G,B)) # Se unen los canales de color para formar la imagen original
#print(imgColor[h-1,w-1]) # el error index 221 is put of bounds significa que me pase del tamaño de la imagen

#Primer Ejemplo: Pintar la imagen solo cambiando aquellos pixeles que cumplan con el color verde mayor a 100 bits

"""for a in range (0,h):
    for b in range (0,w):
        if imgColor[a,b,1] <= 100:
            #print(imgColor[a,b])
            imgColor[a,b]=(255,255,255)
cv2.imshow("imgColor", imgColor)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
            


#Segundo Ejemplo: Borrar o pintar como negro aquellos pixeles que tenga un color verde menor o igual a 100bits

for a in range (0,h):
    for b in range (0,w):
        if imgColor[a,b,1] <= 100:
            #print(imgColor[a,b])
            imgColor[a,b] = (0,0,0)

cv2.imshow("imgColor", imgColor)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Se usa para cerrar todas las ventas que se hallan generado
