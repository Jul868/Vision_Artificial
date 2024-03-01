import cv2
import numpy as np
import time 

bandClick = False
x2 = 0
y2 = 0
pixel_blanco_roi = 0
h = 360
w = 640

pathVideo = "video/video1.mp4"

# Dirección de la imagen 
def getPath(): 
    path =  "imagenes/200_3.jpg" 
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
        # print(x,y) # Imprimo coordenadas x y
        x1 = x
        y1 = y
    elif(event == cv2.EVENT_LBUTTONUP):
        x2 = x
        y2 = y
        bandClick = True # Bandera

# Obtener imagen recortada (región de interés)
def getRoi(x1,y1,x2,y2, img):
    imgRoi = img[y1:y2,x1:x2] # Defino de que a que pixeles voy a obtener la imagen
    return imgRoi

# Binarizar una imagen: convertirla a blanco y negro (cada pixel se clasifica como blanco o negro basándose en un umbral)
def binaryImg(imgGray, u):
    ret, imgBinary = cv2.threshold(imgGray, u, 255, cv2.THRESH_BINARY) # Esta función me permite establecer un umbral de intensidad (u) y clasificarlos como blanco (255) o negro (0)
    # El 255 es el valor asignado a los pixeles que superen el umbral u 
    # cv2.THRESH_BINARY_INV -> aplica el umbral de manera inversa, los pixeles que superen el umbral serán negros y los demás blancos
    # cv2.THRESH_BINARY -> aplica el umbral normal, los pixeles que superen el umbral serán blancos 
    return imgBinary 

# Una función que no hace nada literalmente
def nothing(x):
    pass

for i in range(10):  # Probamos hasta el índice 10
    capture = cv2.VideoCapture(i)
    if not capture.isOpened():
        print(f"No se encontró una cámara en el índice {i}.")
    else:
        print(f"Cámara encontrada en el índice {i}.")
        capture.release()

pathCamUsb = 0
capture = cv2.VideoCapture(pathCamUsb, cv2.CAP_DSHOW)


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_width, output_height = 640, 360  # Tamaño del video de salida
video_writer = cv2.VideoWriter('video/video1.mp4', fourcc, 30, (output_width, output_height))



def main():
    global x2, y2, bandClick, pixel_blanco_roi

    imgColor = getImage(getPath(), 1)
    imgGray = getImage(getPath(), 0)

    cv2.namedWindow("imgColor")
    cv2.namedWindow("imgGray")
    cv2.createTrackbar('u1',"imgGray", 0, 255, nothing)

    cv2.namedWindow("imgBinary")
    cv2.setMouseCallback("imgBinary", mouseClick)
    imgBinary = binaryImg(imgGray, 45)

    h,w = sizeImage(imgGray)

    while True:
        showImage("imgColor", imgColor)
        showImage("imgGray", imgGray)

        # u = cv2.getTrackbarPos("u1", "imgGray")
        # imgBinary = binaryImg(imgGray, 45)
        showImage("imgBinary", imgBinary)

        if (bandClick):
            imgRoi = getRoi(x1,y1,x2,y2,imgBinary)
            showImage("imgRoi", imgRoi)
            bandClick = False

            h1, w1 = sizeImage(imgRoi)
            for row in range(0,h1):
                for col in range(0,w1):
                    if imgRoi[row,col] == 255:
                        pixel_blanco_roi += 1

        if(cv2.waitKey(1) & 0xFF == ord('q')): 
            break
    
    print(pixel_blanco_roi,h,w)
    
    # Pixeles moneda 50: 14147, 14863, 14051
    # Pixeles moneda 100: 17448, 20208, 15108
    # Pixeles moneda 200: 25073, 26220, 26535
    # Pixeles moneda 500: 27900, 27120, 29073
    # Pixeles moneda 1000: 37276, 36639, 37184

    if pixel_blanco_roi in range(14000,15000):
        print("La moneda es de 50")
    elif pixel_blanco_roi in range(15000,21000):
        print("La moneda es de 100")
    elif pixel_blanco_roi in range(21000,27000):
        print("La moneda es de 200")
    elif pixel_blanco_roi in range(27000,35000):
        print("La moneda es de 500")
    elif pixel_blanco_roi in range(35000,40000):
        print("La moneda es de 1000")


if __name__=="__main__":
    main()

