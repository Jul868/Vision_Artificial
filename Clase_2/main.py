import numpy as np
import cv2

x1 = 0
y1 = 0
x2 = 0
y2 = 0
bandClick = False

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

def mouseClick(event,x,y,flags,param):  
    global x1,y1,x2,y2,bandClick
    if(event == cv2.EVENT_LBUTTONDOWN):
        # print(x,y) # Imprimo coordenadas x y
        x1 = x
        y1 = y
        
    elif(event == cv2.EVENT_LBUTTONUP):
        x2 = x
        y2 = y
        bandClick = True # Bandera
        
        if (x1>x2 and y1>y2):
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        elif (x1<x2 and y1>y2):
            y1, y2 = y2, y1
        
        elif (x1>x2 and y1<y2):
            x1, x2 = x2, x1
        
        elif (x1<x2 and y1<y2):
            pass

# Obtener imagen de interes recortada
def getRoi(x1, y1, x2, y2, img):
    imgRoi = img[y1:y2,x1:x2] #defino la region de interes
    return imgRoi

# Binarizar una imagen y convertirla a blanco o negro
def binaryImg(imgGray,u):
    ret, imgBinary = cv2.threshold(imgGray,u,255, cv2.THRESH_BINARY_INV)
    #print(ret)
    return imgBinary

def nothing(x):
    pass

def main():
    global bandClick
    cv2.namedWindow("imgColor")
    cv2.namedWindow("imgGray")
    cv2.setMouseCallback("imgColor", mouseClick)
    cv2.createTrackbar('u1',"imgGray", 0, 255, nothing)
    cv2.createTrackbar('u2', "imgGray",0, 255, nothing)
    imgColor = getImage(getPath(),1)
    imgGray = getImage(getPath(),0)
    #y2, x2 = sizeImage(imgColor)

    while True:
        #print(x1,y1)
        #print(x2,y2)
        #print(imgColor[x1,y1])
        if (bandClick):
            imageRoi = getRoi(x1,y1,x2,y2, imgColor)
            showImage("imgRoi", imageRoi)
            bandClick = False
            
        #Obtener umbral para binarizar una Imagen de forma semiautomatica
        u = cv2.getTrackbarPos('u1',"imgGray")
        u2 = cv2.getTrackbarPos('u2', "imgGray")
        imgBinary = binaryImg(imgGray,u)
        imgBinary2 = cv2.inRange(imgGray,u,u2)

        ## otra forma de binarizar mucho más avanzada

        showImage("imgColor", imgColor)
        showImage("imgGray", imgGray)
        #showImage("imgBinary", imgBinary)
        #showImage("imgBinary2", imgBinary2)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    destroy()

if __name__ == "__main__":
    main()


