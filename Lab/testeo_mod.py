import cv2
import numpy as np
from glob import glob
import joblib
from Motor import MotorController

resultados = []
path = []
contar = 0

# Variables Servo
motor_controller = MotorController(host='192.168.132.209', port=502)  # Usa la IP y puerto de tu ESP32
motor_controller.connect()

mlp = joblib.load('modelMLP.joblib') # Carga del modelo.
skl = joblib.load('modelScaler.joblib') # Carga del modelo.
print("Modelo cargado...", mlp)
pathNum = 'test/'
imgPath = glob(pathNum +'*.jpg')
print("imgPath: ", imgPath)


for iP in imgPath:
    imgColor = cv2.imread(iP,1)
    img = cv2.imread(iP,0)
    img = cv2.resize(img, (800,400))
    imgColor = cv2.resize(imgColor, (800,400))

    ret, imgBin = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY) 

    # Encontrar y almacenar contornos
    contours,hierarchy = cv2.findContours(imgBin.copy(), \
                                                cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    """min_contour_area = 70
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0]) # Ordenar contornos de izquierda a derecha"""

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        a = cv2.contourArea(cnt)            
        if(a>10):
            cv2.rectangle(imgColor, (x,y),(x+w, y+h), (255,0,0), 2)
            cv2.imshow("imgColor",imgColor)
            imgRoi = imgBin[y:y+h, x:x+w]
            imgRoiResize = cv2.resize(imgRoi, (40, 60))
            vectorCaract = imgRoiResize.flatten()         
            # area = cv2.contourArea(cnt)
            # p = cv2.arcLength(cnt, True)
            # M = cv2.moments(cnt)
            # Hu = cv2.HuMoments(M)
            # vectorCaract = np.array([area,p,w/h,w,h,Hu[0][0], Hu[1][0], Hu[2][0]], dtype = np.float32)

            vectorReshape = vectorCaract.reshape(1, -1) # Redimensionar el vector de características
            vectorSKL = skl.transform(vectorReshape) # Escalar el vector de características
            result = mlp.predict(vectorSKL) # Realizar la predicción
            
            resultados.append(int(result[0])) 
            print(path)

            print("result: ", result)
            # print(resultados)

            if int(result[0]) == 0:
                print("el diente es: ", 'canino derecho')
                motor_controller.rotate_servo(30)
                print("path: ", imgPath[contar])
            elif int(result[0]) == 1:
                print("el diente es: ", 'canino izquierdo')
                motor_controller.rotate_servo(60)
                print("path: ", imgPath[contar])
            elif int(result[0]) == 2:
                print("el diente es: ", 'central derecho')
                motor_controller.rotate_servo(90)
                print("path: ", imgPath[contar])
            elif int(result[0]) == 3:
                print("el diente es: ", 'central izquierdo')
                motor_controller.rotate_servo(120)
                print("path: ", imgPath[contar])
            elif int(result[0]) == 4:
                print("el diente es: ", 'lateral derecho')
                motor_controller.rotate_servo(150)
                print("path: ", imgPath[contar])
            elif int(result[0]) == 5:
                print("el diente es: ", 'lateral izquierdo')
                motor_controller.rotate_servo(180)
                print("path: ", imgPath[contar])


    print("Fin...")             
    contar = contar + 1    
    # cv2.imshow("imgColor",imgColor)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if contar == 12:
        motor_controller.close()