import reportlog
import cv2
import threading # Librería para subprocesos 

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
            