import cv2
import numpy as np
from glob import glob
import joblib
from Motor import MotorController

resultados = []
#diente = True
# Variables Servo
# motor_controller = MotorController(host='192.168.132.209', port=502)  # Usa la IP y puerto de tu ESP32
# motor_controller.connect()

pathVideo = 'imagenes/videos/LI.mp4'
capture = cv2.VideoCapture(pathVideo)

mlp = joblib.load('modelF.joblib') # Carga del modelo.q
skl = joblib.load('modelScalerF.joblib') # Carga del modelo.
print("Modelo cargado...", mlp)


while capture.isOpened(): 
    ret, frame = capture.read() 

    if not ret: 
        break
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Cambiar video a escala de gris
    frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Cambiar video a escala de HSV

    cv2.imshow("frame", frame) 
    frameCamera = frame
    frame = cv2.resize(frameCamera, (320, 240))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #_, frameBinary = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    frameBinary = cv2.inRange(frameHSV, (15, 0, 55), (255, 255, 255))
    #cv2.waitKey(30)
    cv2.imshow("frameBinary", frameBinary)

    franja = np.sum(frameBinary[:, 120:200])
    franja = franja / 255

    contours, _ = cv2.findContours(frameBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if franja > 2000 and diente:
        diente = False
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt) # Extraigo patrones
            p = cv2.arcLength(cnt, True) # Extraigo patrones
            m = cv2.moments(cnt) # Extraigo patrones
            Hu = cv2.HuMoments(m) # Extraigo patrones
            aspecto = w/h
            excentricidad = np.sqrt(np.square(w) + np.square(h))/2
            if w > 30 and h > 30:
                cv2.rectangle(frameCamera, (x, y), (x + w, y + h), (255, 0, 0), 2)
                imgRoi = frameBinary[y:y + h, x:x + w]
                imgRoiResize = cv2.resize(imgRoi, (40, 60))
                
                #vectorCaract = np.array([area,p,w,h,Hu[0][0], Hu[1][0], Hu[2][0], Hu[3][0],aspecto,excentricidad], dtype = np.float32)
                vectorCaract = imgRoiResize.flatten()
                vectorReshape = vectorCaract.reshape(1, -1)
                vectorSKL = skl.transform(vectorReshape)
                result = mlp.predict(vectorSKL)
                resultados.append(int(result[0]))
                print("result: ", result)
                
                if int(result[0]) == 0:
                    print("el diente es: ", 'canino derecho')
                    # motor_controller.rotate_servo(30)
                    #print("path: ", imgPath[contar])
                elif int(result[0]) == 1:
                    print("el diente es: ", 'canino izquierdo')
                    # motor_controller.rotate_servo(60)
                    #print("path: ", imgPath[contar])
                elif int(result[0]) == 2:
                    print("el diente es: ", 'central derecho')
                    # motor_controller.rotate_servo(90)
                    #print("path: ", imgPath[contar])
                elif int(result[0]) == 3:
                    print("el diente es: ", 'central izquierdo')
                    # motor_controller.rotate_servo(120)
                    #print("path: ", imgPath[contar])
                elif int(result[0]) == 4:
                    print("el diente es: ", 'lateral derecho')
                    # motor_controller.rotate_servo(150)
                    #print("path: ", imgPath[contar])
                elif int(result[0]) == 5:
                    print("el diente es: ", 'lateral izquierdo')
                    # motor_controller.rotate_servo(180)
                    #print("path: ", imgPath[contar])


    elif franja < 500:
        diente = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
# motor_controller.close()