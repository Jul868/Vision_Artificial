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


def main():
    capture = cv2.VideoCapture(pathVideo)
    time.sleep(2)

    cv2.namedWindow("frameHsv")
    cv2.createTrackbar('Low',"frameHsv", 0, 255, nothing)
    cv2.createTrackbar('High',"frameHsv", 0, 255, nothing)
    cv2.createTrackbar('Low2',"frameHsv", 0, 255, nothing)
    cv2.createTrackbar('High2',"frameHsv", 0, 255, nothing)
    cv2.createTrackbar('Low3',"frameHsv", 0, 255, nothing)
    cv2.createTrackbar('High3',"frameHsv", 0, 255, nothing)


    moneda=True
    num_monedas=0  

    while(capture.isOpened()):
        Hmin = cv2.getTrackbarPos('Low',"frameHsv")
        Hmax = cv2.getTrackbarPos('High',"frameHsv")
        Smin = cv2.getTrackbarPos('Low2',"frameHsv")
        Smax = cv2.getTrackbarPos('High2',"frameHsv")
        Vmin = cv2.getTrackbarPos('Low3',"frameHsv")
        Vmax = cv2.getTrackbarPos('High3',"frameHsv")
        ret, frame = capture.read() 
    

        if (not ret): 
            break 

        # Cambiar el color del video 
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Cambiar video a escala de gris
        frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # cv2.imshow("frame", frame) # Solo se reproduce imagen, no sonido 
        # cv2.imshow("frameGray", frameGray)
        # cv2.imshow("frameHsv", frameHsv)

        # Escribir el frame en el archivo de video
        # video_writer.write(frame)

        videoBinary = cv2.inRange(frameHsv, (0, 0, 16), (255, 73, 255))

        cv2.imshow("videoBinary", videoBinary)
        key = cv2.waitKey(30)

        franja=np.sum(videoBinary[:,330:360])
        franja=franja/255
        print(franja)

        if (franja>100 and moneda):
            print("se detecto un objeto")
            num_monedas+=1
            moneda=False
            print("numero de monedas",num_monedas)
        if (franja<10):
            moneda=True


        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # cv2.imwrite('imagenes/1000_3.jpg', frame)
    capture.release()
    # video_writer.release()
    destroy()

if __name__=="__main__":
    main()
