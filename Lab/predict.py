import cv2
import numpy as np
from glob import glob
import joblib
from Motor import MotorController

resultados = []
diente = True
bandera = True

# Variables Servo
motor_controller = MotorController(host='192.168.132.209', port=502)  # Usa la IP y puerto de tu ESP32
motor_controller.connect()

mlp = joblib.load('modelMLP.joblib')  # Carga del modelo.
skl = joblib.load('modelScaler.joblib')  # Carga del modelo.
print("Modelo cargado...", mlp)

pathCamUsb = 1
capture = cv2.VideoCapture(pathCamUsb, cv2.CAP_DSHOW)


while capture.isOpened(): 
    ret, frame = capture.read() 

    if not ret: 
        break
    
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Cambiar video a escala de gris
    frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Cambiar video a escala de HSV

    cv2.imshow("frame", frame) 
    videoBinary = cv2.inRange(frameHsv, (0, 0, 16), (255, 73, 255))
    cv2.imshow("videoBinary", videoBinary)

    frameCamera = frame
    frame = cv2.resize(frameCamera, (320, 240))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frameBinary = cv2.inRange(frameHSV, (0, 0, 30), (255, 255, 255))

    franja = np.sum(frameBinary[:, 100:200])
    franja = franja / 255

    contours, _ = cv2.findContours(frameBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if franja > 1000 and diente:
        diente = False
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 30 and h > 30:
                cv2.rectangle(frameCamera, (x, y), (x + w, y + h), (255, 0, 0), 2)
                imgRoi = frameBinary[y:y + h, x:x + w]
                imgRoiResize = cv2.resize(imgRoi, (40, 60))
                vectorCaract = imgRoiResize.flatten()
                vectorReshape = vectorCaract.reshape(1, -1)
                vectorSKL = skl.transform(vectorReshape)
                result = mlp.predict(vectorSKL)
                resultados.append(int(result[0]))
                print("result: ", result)

                if int(result[0]) == 0:
                    print("el diente es: ", 'canino derecho')
                    motor_controller.rotate_servo(30)
                elif int(result[0]) == 1:
                    print("el diente es: ", 'canino izquierdo')
                    motor_controller.rotate_servo(60)
                elif int(result[0]) == 2:
                    print("el diente es: ", 'central derecho')
                    motor_controller.rotate_servo(90)
                elif int(result[0]) == 3:
                    print("el diente es: ", 'central izquierdo')
                    motor_controller.rotate_servo(120)
                elif int(result[0]) == 4:
                    print("el diente es: ", 'lateral derecho')
                    motor_controller.rotate_servo(150)
                elif int(result[0]) == 5:
                    print("el diente es: ", 'lateral izquierdo')
                    motor_controller.rotate_servo(180)
    

    elif franja < 100:
        diente = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
motor_controller.close()
