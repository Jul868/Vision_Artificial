import reportlog
import cv2
import threading # Librería para subprocesos
import numpy as np


class RunCamera():
    def __init__(self, src=0, name="CameraThread"):
        try:
            self.name = name
            self.src = src
            self.capture = None
            self.grabbed = None
            self.frame = None
            self.logReport = reportlog.ReportLog()
            self.logReport.logger.info("Init runCamera process")

        except Exception as e:
            self.logReport.logger.error("Error runCamera process " + str(e))

    def start(self):
        try: 
            self.capture = cv2.VideoCapture(self.src)
            self.grabbed, self.frame = self.capture.read()
            
            if (self.capture.isOpened()): 
                self.running = True
                # Hilo -> subproceso que siempre se está ejecutando, un hilo no se puede quedar abierto 
                # Este hilo se encarga de leer el video 
                self.cameraThread = threading.Thread( # Thread es una función que me ayuda a crear y configurar un hilo 
                                                     target = self.get, name=self.name, daemon=True) # Lo que corre dentro del hilo 
                self.cameraThread.start()

        except Exception as e:
            self.logReport.logger.error("Error runCamera start " + str(e))
    
    def get(self):
        try: 
            while self.running and self.grabbed:
                self.grabbed, self.frame = self.capture.read()
                cv2.waitKey(30)
                if not self.grabbed:
                    break

        except Exception as e:
            self.logReport.logger.error("Error get frame " + str(e))

    def stop(self):
        try: 
            self.running = False
        except Exception as e:
            self.logReport.logger.error("Error runCamera stop " + str(e))
            
    def getFrameBinary(self, u1, u2):
        try:
            self.frameC = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frameHSV = cv2.cvtColor(self.frameC, cv2.COLOR_BGR2HSV)
            lower_bound = np.array([u1])
            upper_bound = np.array([u2])
            self.frameBinary = cv2.inRange(self.frameHSV, lower_bound, upper_bound)
        except Exception as e:
            self.logReport.logger.error("Error get frame binary " + str(e))
    
    def getimgROI(self,x1,y1,x2,y2, scale):
        self.frame3 = cv2.resize(self.frameBinary, (320,240))
        self.imgROI = self.frame3[y1:y2, x1:x2]
        self.imgROIColor = self.frame[y1:y2, x1:x2]
        #cv2.imshow('imgROI: ', self.imgROI)
        
    def areaC(self, cnt):
            # Encuentra el círculo mínimo que encierra el contorno
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            # Calcula el área del círculo
            area = np.pi * (radius ** 2)
            return area

    def imgCont(self):
        try:
            mgRoi = cv2.resize(self.imgROI, (320, 240))
            self.contours, self.hie = cv2.findContours(mgRoi, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            self.imgBinRsize = cv2.resize(self.frame, (320, 240))
            self.imgContours = np.zeros(self.imgBinRsize.shape[:], dtype=np.uint8)

            if self.contours:
                for idx, (cnt, hier) in enumerate(zip(self.contours, self.hie[0])):
                    if hier[3] != -1 and hier[2] == -1:
                        area = cv2.contourArea(cnt)
                        if area > 100:
                            # Dibujar solo contornos internos
                            cv2.drawContours(self.imgContours, [cnt], -1, (255, 0, 0), 2)
                            self.areaCirc = self.areaC(cnt)

        except Exception as e:
            self.logReport.logger.error("Error in imgCont: " + str(e))

        
            


            