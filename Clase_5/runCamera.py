import reportLog
import cv2
import threading
import numpy as np

class runCamera:
    def __init__(self, src = 0, name = "CameraThread"):
        try:
            self.name = name
            print('src: ', src)
            self.src = src
            self.capture = None
            self.grabbed = None  #Se inicializa la variable en cero (none)
            self.logReport = reportLog.ReportLog()
            self.logReport.logger.info("Initializing runCamera Process")
        except Exception as e:
            self.logReport.logger.error("Error in runCamera Process: " + str(e))
    
    def start(self):
        try:
            self.capture = cv2.VideoCapture(self.src) #Se inicializa la cámara
            self.grabbed, self.frame = self.capture.read() #Se captura un frame
            if (self.capture.isOpened()):
                self.cameraThread = threading.Thread(
                    target=self.get, name=self.name, daemon=True) #Se crea un hilo para la cámara con el método get, y se usa daemon para que el hilo se cierre cuando se cierre el programa
                self.cameraThread.start() #Se inicia el hilo de la cámara con el método start de la clase Thread de threading 


        except Exception as e:
            self.logReport.logger.error("Error in runCamera Process: " + str(e))

    def get(self):
        try:
            while self.grabbed:
                self.grabbed, self.frame = self.capture.read() #Se captura un frame de la cámara y se guarda en la variable frame
                cv2.waitKey(10)
                if not self.grabbed:
                    break
        except Exception as e:
            self.logReport.logger.error("Error in get frame: " + str(e))  #Se captura un frame de la cámara y se guarda en la variable frame
    
    def stop(self):
        try:
            self.capture.release() #Se libera la cámara
            self.logReport.logger.info("Camera released")
        except Exception as e:
            self.logReport.logger.error("Error in stop camera: " + str(e))
