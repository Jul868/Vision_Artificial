import reportlog
import cv2
import threading # Librería para subprocesos
import numpy as np
from glob import glob
import joblib
import depthai as dai


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

            # Crear pipeline para la cámara y la profundidad
            self.pipeline = dai.Pipeline()

            # Crear nodos de cámara y profundidad
            self.monoLeft = self.pipeline.create(dai.node.MonoCamera)
            self.monoRight = self.pipeline.create(dai.node.MonoCamera)
            self.stereo = self.pipeline.create(dai.node.StereoDepth)
            self.color = self.pipeline.create(dai.node.ColorCamera)
            self.xoutDepth = self.pipeline.create(dai.node.XLinkOut)
            self.xoutColor = self.pipeline.create(dai.node.XLinkOut)

            # Configurar cámaras
            self.monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
            self.monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
            self.monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
            self.monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
            self.color.setPreviewSize(640, 360)
            self.color.setBoardSocket(dai.CameraBoardSocket.RGB)

            # Configurar nodo de profundidad
            self.stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
            self.stereo.setSubpixel(True)
            self.stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
            self.stereo.setOutputSize(self.monoLeft.getResolutionWidth(), self.monoLeft.getResolutionHeight())

            # Configurar XLinkOut
            self.xoutDepth.setStreamName("depth")
            self.xoutColor.setStreamName("color")

            # Enlazar nodos
            self.monoLeft.out.link(self.stereo.left)
            self.monoRight.out.link(self.stereo.right)
            self.stereo.depth.link(self.xoutDepth.input)
            self.color.preview.link(self.xoutColor.input)

            self.label = None

        except Exception as e:
            self.logReport.logger.error("Error runCamera process " + str(e))

    def start(self):
        try: 
            # Para video
            self.capture = cv2.VideoCapture(self.src)

            # Para cámara
            # self.capture = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
            
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

    def startCamera(self):
        try:
            # Ejecutar pipeline
            with dai.Device(self.pipeline, usb2Mode=True) as device:
                depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
                colorQueue = device.getOutputQueue(name="color", maxSize=4, blocking=False)

                while True:
                    self.depthFrame = depthQueue.get().getFrame()  # Obtener el frame de profundidad
                    self.colorFrame = colorQueue.get().getCvFrame()  # Obtener el frame de color


        except Exception as e:
            self.logReport.logger.error("Error startCamera " + str(e))


    def stop(self):
        try: 
            self.running = False
        except Exception as e:
            self.logReport.logger.error("Error runCamera stop " + str(e))
        