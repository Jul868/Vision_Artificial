from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font 
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk, ImageDraw, ImageFont
from glob import glob
import joblib
# from ultralytics import YOLO
# import torch
import depthai as dai

import cv2
import numpy as np
import reportlog
import runCamera
import time
import math

class Application(ttk.Frame):
    def __init__(self,master=None):
        try:
            super().__init__(master)
            self.logReport = reportlog.ReportLog()

            # Para video 
            self.camera = runCamera.RunCamera(src="output.mp4", name="video_1")

            # Para cámara en tiempo real
            # self.camera = runCamera.RunCamera(0)

            # Funciones
            # self.function = functions.Functions()

            self.master = master
            self.width = 1280 # Ancho de la ventana
            self.height = 400
            self.master.geometry("%dx%d" % (self.width, self.height))
            self.pack
            self.panel = None

            self.cajas = 0

            # Listas para almacenar los datos de detección por clase
            self.boxes_data = []
            self.abb_data = []
            self.abb_base_data = []

            self.anguloFovMed=18.3
            self.anguloFovMed2=30.11

            # Load the YOLOv8 model
            # self.model = YOLO('runs/detect/train/weights/best.pt')


            self.createWidgets()
            self.createFrameZeros()
            self.logReport.logger.info("GUI created")
            self.master.mainloop()
        
        except Exception as e:
            self.logReport.logger.error("GUI no created " + str(e))

    def createFrameZeros(self):
        try:
            self.lblVideo = tk.Label(self.master, borderwidth=2, relief="solid")
            self.lblVideo.place(x=20, y=25)

            # Frame original 
            frame = np.zeros([240,320,3], dtype=np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgArray = Image.fromarray(frame)
            imgTk = ImageTk.PhotoImage(image=imgArray)
            self.lblVideo.configure(image=imgTk)
            self.lblVideo.image = imgTk

            # Frame Video Profundidad
            self.lblVideoDepth = tk.Label(self.master, borderwidth=2, relief="solid")
            self.lblVideoDepth.place(x=370, y=25)
            self.lblVideoDepth.configure(image = imgTk) # Le paso las propiedades de imgTk
            self.lblVideoDepth.image = imgTk

            # Frame ROI 1 - ROI ABB
            self.lbl1 = tk.Label(self.master, borderwidth=2, relief="solid")
            self.lbl1.place(x=720, y = 25)
            self.lbl1.configure(image=imgTk)
            self.lbl1.image = imgTk
        
        except Exception as e:
            self.logReport.logger.error("Error in createFrameZeros " + str(e))

    def createWidgets(self):
        try:
            self.fontText = font.Font(family='Helvetica', size=8, weight='normal') 
            self.fontText1 = font.Font(family='Helvetica', size=10, weight='bold')

            self.lblNameCamera = tk.Label(self.master, text="Video en Tiempo real", fg="#000000")
            self.lblNameCamera['font'] = self.fontText  
            self.lblNameCamera.place(x=20, y=5)  

            self.lblNameDepth = tk.Label(self.master, text="Video Profundidad", fg="#000000")
            self.lblNameDepth['font'] = self.fontText  
            self.lblNameDepth.place(x=370, y=5) 

            self.lblRoi1 = tk.Label(self.master, text="ABB", fg="#000000")
            self.lblRoi1['font'] = self.fontText  
            self.lblRoi1.place(x=720, y=5) 

            self.lblContador = tk.Label(self.master, text="Contador de cajas", fg="#000000")
            self.lblContador['font'] = self.fontText1
            self.lblContador.place(x=20, y=290)

            self.lblCajas = tk.Label(self.master, text="Total cajas: ", fg="#000000")
            self.lblCajas['font'] = self.fontText  
            self.lblCajas.place(x=20, y=310)

            self.lblCajas1 = tk.Label(self.master, text=str(self.cajas), fg="#000000")
            self.lblCajas1['font'] = self.fontText  
            self.lblCajas1.place(x=70, y=310)

            self.btnInitCamera = tk.Button(self.master,
                                       text="Iniciar",
                                       bg = '#45B39D',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.initCameraProcess)
            self.btnInitCamera.place(x=20, y=350)

            self.btnStopCamera = tk.Button(self.master,
                                       text="Parar",
                                       bg = '#5DADE2',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.stopCameraProcess)
            self.btnStopCamera.place(x=170, y=350)

            self.btnStopCamera = tk.Button(self.master,
                                        text="Cerrar",
                                        bg = '#C0392B',
                                        fg='#FFFFFF',
                                        width=12,
                                        command=self.exit)
            self.btnStopCamera.place(x=320, y=350)

        except Exception as e:
            self.logReport.logger.error("Error in createWidgets " + str(e))

    def initCameraProcess(self):
        self.camera.start()
        self.camera.startCamera()
        self.predict()
        self.getFrameInLabel()

        self.cajas = 0

    def stopCameraProcess(self):
        self.camera.stop()
        print("stop")

    def exit(self):
        respuesta = messagebox.askyesno("Confirmar salida", "¿Está seguro de que desea salir?")
        if respuesta:
            self.master.destroy()

    def getFrameInLabel(self):
        try:
            if (self.camera.grabbed):
                frameCamera = self.camera.frame
                self.frame = cv2.resize(frameCamera, (320,240))
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
                imgArray = Image.fromarray(self.frame)  
                imgTk = ImageTk.PhotoImage(image=imgArray) 
                self.lblVideo.configure(image = imgTk)
                self.lblVideo.image = imgTk

                self.lblVideoDepth.configure(image=imgTk)
                self.lblVideoDepth.image = imgTk

                self.getFrameDepth()
                self.roi_abb()
                self.actualizarContador()

                self.lblVideo.after(90, self.getFrameInLabel)

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabel" + str(e)) 

    def getFrameDepth(self):
        try:
            """self.frameC = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frameHSV = cv2.cvtColor(self.frameC, cv2.COLOR_BGR2HSV)
            lower_bound = np.array([(0, 0, 25)])
            upper_bound = np.array([(255, 255, 255)])

            self.frameBinary = cv2.inRange(self.frameHSV, lower_bound, upper_bound)
            self.frame2 = cv2.resize(self.frameHSV, (320,240))
            self.frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)"""

            """frameCameraDepth = self.camera.depthFrame
            self.frame2 = cv2.resize(frameCameraDepth, (320,240))
            self.frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB) 
            imgArray2 = Image.fromarray(self.frame2)
            imgTk2 = ImageTk.PhotoImage(image=imgArray2)
            self.lblVideoDepth.configure(image=imgTk2)
            self.lblVideoDepth.image = imgTk2"""
            
        except Exception as e:
            self.logReport.logger.error("Error in getFrameBinary" + str(e))

    def roi_abb(self):
        try:
            self.frameC = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frameHSV = cv2.cvtColor(self.frameC, cv2.COLOR_BGR2HSV)
            lower_bound = np.array([(0, 70, 25)])
            upper_bound = np.array([(220, 255, 255)])

            self.frameBinary = cv2.inRange(self.frameHSV, lower_bound, upper_bound)
            self.frame2 = cv2.resize(self.frameHSV, (320,240))
            self.frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)

            self.img_color_aux = cv2.resize(self.frame, (320, 240))
            imgContours = self.img_color_aux.copy()
            
            cv2.drawContours(imgContours, self.contours, -1, (255, 0, 0), 2)
            
            imgContResized = Image.fromarray(cv2.cvtColor(imgContours, cv2.COLOR_BGR2RGB))
            self.photo_contour = ImageTk.PhotoImage(image=imgContResized)
            self.lbl1.configure(image=self.photo_contour)

            imgArray2 = Image.fromarray(self.frameBinary)  
            imgTk2 = ImageTk.PhotoImage(image=imgArray2) 
            self.lbl1.configure(image = imgTk2)
            self.lbl1.image = imgTk2


        except Exception as e:
            self.logReport.logger.error("Error in roi_abb" + str(e))
    

    def actualizarContador(self):
        self.lblCajas1.config(text=str(self.cajas))

    


    def predict(self):
        try: 
            # Realizar predicciones con YOLOv8 en el frame de color
            results = self.model.predict(self.camera.colorFrame, conf=0.65)
            self.annotated_frame = results[0].plot()

            # Resetear las listas de detecciones por clase en cada frame
            self.boxes_data.clear()
            self.abb_data.clear()
            self.abb_base_data.clear()

            # Procesar detecciones
            for detection in results[0].boxes:
                class_id = int(detection.cls[0])
                class_name = self.model.names[class_id]
                x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy().astype(int)
                #print(f"Detected {class_name} at ({x1}, {y1}) ({x2}, {y2})")
                centroid_x = (x1 + x2) // 2
                centroid_y = (y1 + y2) // 2
                theta_y = (self.anguloFovMed/180)*(centroid_y-180)
                theta_x = (self.anguloFovMed2/320)*(centroid_x-320)

                # Obtener el valor de profundidad en el centroide
                if 0 <= centroid_x < self.camera.depthFrame.shape[1] and 0 <= centroid_y < self.camera.depthFrame.shape[0]:
                    z_value = self.camera.depthFrame[centroid_y, centroid_x]/1000
                    if class_name == 'ABB':
                        h=z_value/1000
                    else:
                        h=2.4
                    x=h*np.tan(np.deg2rad(theta_x))*(1/0.8887)-0.0102
                    y=h*np.tan(np.deg2rad(theta_y))
                    # Dibujar un círculo en el centroide y mostrar la distancia en Z
                    cv2.circle(self.annotated_frame, (centroid_x, centroid_y), 5, (0, 255, 0), -1)
                    cv2.putText(self.annotated_frame, f"Z: {round(z_value, 2)} m", (centroid_x + 10, centroid_y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                    cv2.putText(self.annotated_frame, f"X: {round(x, 2)} m", (centroid_x + 10, centroid_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                    cv2.putText(self.annotated_frame, f"Y: {round(y, 2)} m", (centroid_x + 10, centroid_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

                    cv2.line(self.annotated_frame,(320,0),(320,360),(0,0,255),2)
                    cv2.line(self.annotated_frame,(0,180),(640,180),(0,0,255),2)
                    # Almacenar la detección en la lista adecuada
                    detection_info = {"class": class_name, "x":x, "y": y, "z": z_value}
                    if class_name == 'BOX':
                        self.boxes_data.append(detection_info)
                    elif class_name == 'ABB':
                        self.abb_data.append(detection_info)
                    elif class_name == 'ABB_BASE':
                        self.abb_base_data.append(detection_info)
                    
                            # Imprimir las listas de detecciones después del procesamiento
            print("Boxes data:", self.boxes_data)
            print("ABB data:", self.abb_data)
            #print("ABB_BASE data:", abb_base_data)

            # Mostrar el frame anotado
            # cv2.imshow("YOLOv8 Inference with Depth", annotated_frame)
            

        except Exception as e:
            self.logReport.logger.error("Error in getFrameBinary" + str(e))

def main():
    root = tk.Tk() # Crear una instancia de tkinter -> todo lo que yo defina se va a quedar dentro de la raiz 
    root.title("Project")
    appRunCamera = Application(master=root)
