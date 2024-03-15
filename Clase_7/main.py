import cv2
import numpy as np

path = 'imagenes/fig.png'

imgColor = cv2.imread(path, 1)
imgGray = cv2.imread(path, 0)

ret, imgBinary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) # Otsu's thresholding compared with binary thresholding makes the image more clear

contours, hie = cv2.findContours(imgBinary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # i have to install opencv-contrib-python to use this function
print(len(contours))
cv2.imshow('imgBinary', imgBinary)
cv2.waitKey(0)
cv2.destroyAllWindows()