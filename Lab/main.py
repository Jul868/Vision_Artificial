import cv2
import numpy as np
import time 

bandClick = False
img_counter = 64

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

"""for i in range(10):  # Probamos hasta el índice 10
    capture = cv2.VideoCapture(i)
    if not capture.isOpened():
        print(f"No se encontró una cámara en el índice {i}.")
    else:
        print(f"Cámara encontrada en el índice {i}.")
        capture.release()"""

pathCamUsb = 0
capture = cv2.VideoCapture(pathCamUsb, cv2.CAP_DSHOW)


#capture = cv2.VideoCapture(pathVideo)
time.sleep(2)

while(capture.isOpened()): 
    ret, frame = capture.read() 

    if (not ret): 
        break 

    # Cambiar el color del video 
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Cambiar video a escala de gris
    frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow("frame", frame) # Solo se reproduce imagen, no sonido 
    # cv2.imshow("frameGray", frameGray)
    # cv2.imshow("frameHsv", frameHsv)

    # Escribir el frame en el archivo de video
    # video_writer.write(frame)

    videoBinary = cv2.inRange(frameHsv, (0, 0, 16), (255, 73, 255))
    # BinaryColor = cv2.bitwise_and(frame, frame, mask=videoBinary) # Fondo a color y lo otro no 
    # cv2.imshow("videoBinary", videoBinary)

    key = cv2.waitKey(30)
    if key == ord('q'):
        break
    elif key == ord('e'):
        img_name = "imagenes/img_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} guardado".format(img_name))
        img_counter += 1

# cv2.imwrite('imagenes/img_1.jpg', frame)
capture.release()
# video_writer.release()
cv2.destroyAllWindows()