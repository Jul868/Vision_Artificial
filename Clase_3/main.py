import cv2
import numpy as np
import time
import imutils
import requests
import urllib.request


#pathVideo = "videos/Sea.mp4"
#pathCamUsb = 0
pathCameraPhone = "http://192.168.80.219:8080/shot.jpg"

#capture = cv2.VideoCapture(pathCameraPhone) # Se pone 0 en vez de pathCamUsb para usar la cámara de la laptop
#time.sleep(2)

#while(capture.isOpened()):
    #ret, frame =capture.read()
while(True):
    imgUrl = urllib.request.urlopen(pathCameraPhone)
    imgNp = np.array(bytearray(imgUrl.read()),dtype=np.uint8) 
    frame = cv2.imdecode(imgNp, -1)
    #if(not ret):
    #    break
    frame = cv2.resize(frame, (640,480))
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("frame", frame)
    cv2.imshow("frameGray", frameGray)
    cv2.imshow("frameHsv", frameHsv)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()