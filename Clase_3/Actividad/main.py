import cv2
import numpy as np
import time
import imutils
import requests
import urllib.request


def getPath():
    path = "images/figures.png"
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

def mouseClick(event, x, y, flags, param):
    global x1, y1, x2, y2, bandClick
    if(event == cv2.EVENT_LBUTTONDOWN):
        imgColor = getImage(getPath(),1)
        #print(imgColor[x,y]) #Imprimir de las coordenadas X y Y los valore RGB
        x1 = x
        y1 = y

    elif(event == cv2.EVENT_LBUTTONUP):
        x2 = x
        y2 = y
        bandClick = True

def getRoi(x1, y1, x2, y2, img):
    imgRoi = img[y1:y2,x1:x2]
    return imgRoi

def binaryImg(imgGray,u):
    ret, imgBinary = cv2.threshold(imgGray,u,255, cv2.THRESH_BINARY_INV)
    print(ret)
    return imgBinary

def nothing(x):
    pass


#pathVideo = "videos/Sea.mp4"
#pathCamUsb = 0
pathCameraPhone = "http://192.168.80.219:8080/shot.jpg"
cv2.namedWindow("frameHsv")
cv2.createTrackbar('Low',"frameHsv", 0, 255, nothing)
cv2.createTrackbar('High',"frameHsv", 0, 255, nothing)
cv2.createTrackbar('Low2',"frameHsv", 0, 255, nothing)
cv2.createTrackbar('High2',"frameHsv", 0, 255, nothing)
cv2.createTrackbar('Low3',"frameHsv", 0, 255, nothing)
cv2.createTrackbar('High3',"frameHsv", 0, 255, nothing)


while(True):
    Hmin = cv2.getTrackbarPos('Low',"frameHsv")
    Hmax = cv2.getTrackbarPos('High',"frameHsv")
    Smin = cv2.getTrackbarPos('Low2',"frameHsv")
    Smax = cv2.getTrackbarPos('High2',"frameHsv")
    Vmin = cv2.getTrackbarPos('Low3',"frameHsv")
    Vmax = cv2.getTrackbarPos('High3',"frameHsv")
    
    imgUrl = urllib.request.urlopen(pathCameraPhone)
    imgNp = np.array(bytearray(imgUrl.read()),dtype=np.uint8) 
    frame = cv2.imdecode(imgNp, -1)
    frame = cv2.resize(frame, (640,480))
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    
    imgBinary = cv2.inRange(frameHsv, (Hmin, Smin, Vmin), (Hmax, Smax, Vmax))
    imgBinary2 = cv2.bitwise_and(frame, frame, mask=imgBinary)
    cv2.imshow("frame", frame)
    cv2.imshow("frameGray", imgBinary2)
    cv2.imshow("frameHsv", frameHsv)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()