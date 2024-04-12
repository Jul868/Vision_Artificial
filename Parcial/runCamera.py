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
        imgROI = self.frame3[y1:y2, x1:x2]
        h, w = imgROI.shape[:2]
        self.imgROI = cv2.resize(imgROI, (w*scale,h*scale))
        #cv2.imshow('imgROI: ', self.imgROI)

    def imgCont(self):
        try:
            #print("imgCont")
            self.contours, self.hie = cv2.findContours(self.imgROI, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            self.imgBinRsize = cv2.resize(self.frame, (320,240))
            self.imgContours = np.zeros(self.imgBinRsize.shape[:], dtype=np.uint8)
            if (len(self.contours) > 0):
                for cnt in self.contours:
                    x,y,w,h = cv2.boundingRect(cnt)
                    area = cv2.contourArea(cnt)
                    if ( area > 100):
                        cv2.rectangle(self.imgBinRsize, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        p = cv2.arcLength(cnt, True)
                        c = 4*np.pi*area/(p*p)
                        # area del circulo
                        self.areaCirc = np.pi*(w/2)*(h/2)
                        if (c > 0.1):
                            cv2.drawContours(self.imgContours, cnt, -1, (255, 0, 0), 2)
                            cv2.imshow('imgContours', self.imgContours)
        except Exception as e:
            self.logReport.logger.error("Error imgContours " + str(e))
        
            


            