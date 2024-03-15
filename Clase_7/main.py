import cv2
import numpy as np

path = 'imagenes/fig.png'

imgColor = cv2.imread(path, 1)
imgGray = cv2.imread(path, 0)

ret, imgBinary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) # Otsu's thresholding compared with binary thresholding makes the image more clear
cv2.imshow('imgBinary', imgBinary)
cv2.waitKey(1)
contours, hie = cv2.findContours(imgBinary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) #cv2.RETR_LIST: devuelve todos los contornos sin jerarquía 
                                                                                    #cv2.CHAIN_APPROX_SIMPLE: comprime los segmentos horizontales, verticales y diagonales y deja solo sus puntos finales
                                                                                    #cv2.RETR_TREE: devuelve todos los contornos con jerarquía
                                                                                    #cv2.CHAIN_APPROX_NONE: devuelve todos los puntos del contorno
                                                                                    #cv2.RETR_EXTERNAL: devuelve solo los contornos externos
                                                                                    #hie es la jerarquía de los contornos
imgContours = np.zeros(imgColor.shape[:], dtype=np.uint8) # crear una imagen vacia para ubicar los contornos
print(len(contours))
if (len(contours) > 0):
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt) # Devuelve las coordenadas de la esquina superior izquierda y el ancho y alto del rectángulo que rodea al contorno
        area = cv2.contourArea(cnt)
        if ( area > 500):
            cv2.rectangle(imgColor, (x, y), (x+w, y+h), (255, 0, 0), 2)
            p = cv2.arcLength(cnt, True)
            c = 4*np.pi*area/(p*p) # circularity
            if (c > 0.8):
                #cv2.drawContours(imgColor, cnt, -1, (255, 0, 0), 2)
                cv2.drawContours(imgContours, cnt, -1, (255, 0, 0), 2)
                cv2.imshow('imgColor', imgColor)
                cv2.imshow('imgContours', imgContours)
                cv2.waitKey(0)
cv2.destroyAllWindows()
