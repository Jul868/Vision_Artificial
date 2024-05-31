# Graphic user interface (gui)
# Graphic user interface (gui)
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font 
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk, ImageDraw, ImageFont
from glob import glob
import joblib

import cv2
import numpy as np
import reportlog
import runCamera
import time
import math

class Application(ttk.Frame): # Se le da estructura de un frame
    def __init__(self,master=None):
        try:
            super().__init__(master)
            self.logReport = reportlog.ReportLog()
            
            #self.camera = runCamera.RunCamera(0)
            self.direction = "video/CAD.mp4"
            self.camera = runCamera.RunCamera(src=self.direction, name="video_1")

            self.master = master
            self.width = 1280 # Ancho de la ventana
            self.height = 600
            self.master.geometry("%dx%d" % (self.width, self.height))
            self.pack
            self.panel = None

            self.total_objetos = 0
            self.objeto = True
            self.objeto2 = True
            self.cambio = True
            
            self.anillo = 0
            self.tensor = 0
            self.anillo2 = 0
            self.tensor2 = 0
            
            self.CD = 0
            self.CI = 0
            self.CED = 0
            self.CEI = 0
            self.LD = 0
            self.LI = 0
            
            self.bandera_anillo1=False
            self.bandera_Tensor1=True
            self.bandera_anillo2=False
            self.bandera_Tensor2=True
            
            self.array = np.array([1,1])
            
            self.x1 = -1
            self.y1 = -1
            self.x2 = -1
            self.y2 = -1
            self.xx = -1
            self.yy = -1
            self.ww = -1
            self.hh = -1
            
            self.detected_object_image = None

            self.createWidgets()
            self.createFrameZeros()
            self.logReport.logger.info("GUI created")
            self.master.mainloop()
            

        except Exception as e:
            self.logReport.logger.error("GUI no created" + str(e)) 

        
    def createFrameZeros(self):
        self.lblVideo = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideo.place(x=20, y=25)

        # Frame Video Original
        frame = np.zeros([240,320,3], dtype=np.uint8) # 480 de alto, 640 de ancho y una imagen de 3 colores (creo un recuadro negro)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # tkinter es RGB y cv2 es BGR (conversión para el formato de tkinter)
        imgArray = Image.fromarray(frame) # Extracción del formato 
        imgTk = ImageTk.PhotoImage(image=imgArray) # Array convetido a la propiedad de PhotoImage 
        self.lblVideo.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lblVideo.image = imgTk

        # Frame Video Bin
        self.lblVideoBinary = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideoBinary.place(x=370, y=25)
        self.lblVideoBinary.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lblVideoBinary.image = imgTk
        
        # Frame Machine Learning
        self.lbl3 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lbl3.place(x=20, y=320)
        self.lbl3.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lbl3.image = imgTk

        #Frame Deep Learning
        self.lbl4 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lbl4.place(x=370, y=320)
        self.lbl4.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lbl4.image = imgTk
    
    def createWidgets(self):
        # crear un font centrado y con negrilla
        self.fontText = font.Font(family='Helvetica', size=12, weight='bold') # Tipo de letra y tamaño que se quiere usar 
        self.lblNameCamera = tk.Label(self.master, text="Video en Tiempo real", fg="#000000")
        self.lblNameCamera['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCamera.place(x=20, y=5) # Ubico el texto 

        self.lblNameCameraBinary = tk.Label(self.master, text="Video Binarizada", fg="#000000")
        self.lblNameCameraBinary['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCameraBinary.place(x=370, y=5) # Ubico el texto

        self.lblNameCameraROI= tk.Label(self.master, text="Analisis Machine Learning", fg="#000000")
        self.lblNameCameraROI['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCameraROI.place(x=20, y=300) # Ubico el texto 

        self.lblNameCameraCONT = tk.Label(self.master, text="Analisis Deep Learning", fg="#000000")
        self.lblNameCameraCONT['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCameraCONT.place(x=370, y=300) # Ubico el texto

        #Referencia
        self.lblReferencia = tk.Label(self.master, text="Referencia", fg="#000000")
        self.lblReferencia['font'] = self.fontText # Toma la propiedad del texto
        self.lblReferencia.place(x=720, y=30) # Ubico el texto

        #Cantidad
        self.lblCantidad = tk.Label(self.master, text="Cantidad", fg="#000000")
        self.lblCantidad['font'] = self.fontText # Toma la propiedad del texto
        self.lblCantidad.place(x=880, y=30) # Ubico el texto


        # Canino Derecho 
        self.lblCaninoDerecho = tk.Label(self.master, text="Canino Derecho: "+ str(self.CD), fg="#000000")
        self.lblCaninoDerecho['font'] = self.fontText # Toma la propiedad del texto 
        self.lblCaninoDerecho.place(x=720, y=60) # Ubico el texto
        
        # Canino Izquierdo
        self.lblCaninoIzquierdo = tk.Label(self.master, text="Canino Derecho: "+ str(self.CI), fg="#000000")
        self.lblCaninoIzquierdo['font'] = self.fontText # Toma la propiedad del texto
        self.lblCaninoIzquierdo.place(x=720, y=80) # Ubico el texto
        
        # Central Derecho
        self.lblCentralDerecho = tk.Label(self.master, text="Central Derecho: "+ str(self.CED), fg="#000000")
        self.lblCentralDerecho['font'] = self.fontText # Toma la propiedad del texto
        self.lblCentralDerecho.place(x=720, y=100) # Ubico el texto
        
        # Central Izquierdo
        self.lblCentralIzquierdo = tk.Label(self.master, text="Central Izquierdo: "+ str(self.CEI), fg="#000000")
        self.lblCentralIzquierdo['font'] = self.fontText # Toma la propiedad del texto
        self.lblCentralIzquierdo.place(x=720, y=120) # Ubico el texto
        
        # Lateral Derecho
        self.lblLateralDerecho = tk.Label(self.master, text="Lateral Derecho: "+ str(self.LD), fg="#000000")
        self.lblLateralDerecho['font'] = self.fontText # Toma la propiedad del texto
        self.lblLateralDerecho.place(x=720, y=140) # Ubico el texto
        
        # Lateral Izquierdo
        self.lblLateralIzquierdo = tk.Label(self.master, text="Lateral Izquierdo: "+ str(self.LI), fg="#000000")
        self.lblLateralIzquierdo['font'] = self.fontText # Toma la propiedad del texto
        self.lblLateralIzquierdo.place(x=720, y=160) # Ubico el texto


        self.btnInitCamera = tk.Button(self.master,
                                       text="Iniciar",
                                       bg = '#45B39D',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.initCameraProcess)
        self.btnInitCamera.place(x=800, y=400)

        self.btnStopCamera = tk.Button(self.master,
                                       text="Parar",
                                       bg = '#5DADE2',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.stopCameraProcess)
        self.btnStopCamera.place(x=950, y=400)

        self.btnStopCamera = tk.Button(self.master,
                                       text="Cerrar",
                                       bg = '#C0392B',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.exit)
        self.btnStopCamera.place(x=800, y=450)
        

    def initCameraProcess(self):
        self.camera.start()
        self.getFrameInLabel()
        self.mlp = joblib.load('ModelF.joblib') # Carga del modelo.q
        self.skl = joblib.load('modelScalerF.joblib') # Carga del modelo.
        self.net = cv2.dnn.readNet("model.weights","model.cfg")
        print("Modelo cargado...", self.mlp)

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

                # self.identificarMonedas()
                self.getFrameInLabelBinary()
                self.actualizarContadoresGUI()
                #self.identificarPiezas()
                
                
                self.lblVideo.after(60, self.getFrameInLabel) # Cada cuanto se va a pedir un label 

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabel" + str(e)) 


    def getFrameInLabelBinary(self):
        try:
            # Realiza la detección del objeto
            self.camera.getFrameBinary((0, 0, 25), (255, 255, 255))
            frameCamera = self.camera.frameBinary
            self.frame2 = cv2.resize(frameCamera, (320,240))
            self.frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
            imgArray2 = Image.fromarray(self.frame2)
            imgTk2 = ImageTk.PhotoImage(image=imgArray2)
            self.lblVideoBinary.configure(image=imgTk2)
            self.lblVideoBinary.image = imgTk2
            
            self.getFrameML()
            self.getFrameDL()
        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabelBinary" + str(e))
            
    def getFrameML(self):
        self.camera.MachineLearning(self.mlp, self.skl)
        #self.result = self.camera.result
        frameML = self.camera.imgRoiResize
        self.frame3 = cv2.resize(frameML, (320,240))
        self.frame3 = cv2.cvtColor(self.frame3, cv2.COLOR_BGR2RGB)
        imgArray3 = Image.fromarray(self.frame3)
        imgTk3 = ImageTk.PhotoImage(image=imgArray3)
        self.lbl3.configure(image=imgTk3)
        self.lbl3.image = imgTk3
        
        self.CD = self.camera.CD
        self.CI = self.camera.CI
        self.CED = self.camera.CED
        self.CEI = self.camera.CEI
        self.LD = self.camera.LD
        self.LI = self.camera.LI
            
    def getFrameDL(self):
        self.camera.DeepLearning(self.net)
        self.labelDP = self.camera.label
        frameDL = self.camera.saveFrame
        self.frame4 = cv2.resize(frameDL, (320,240))
        self.frame4 = cv2.cvtColor(self.frame4, cv2.COLOR_BGR2RGB)
        imgArray4 = Image.fromarray(self.frame4)
        imgTk4 = ImageTk.PhotoImage(image=imgArray4)
        self.lbl4.configure(image=imgTk4)
        self.lbl4.image = imgTk4
        
        if self.labelDP == "a":
            print("Canino Derecho")
        elif self.labelDP == "b":
            print("Canino Izquierdo")
        elif self.labelDP == "c":
            print("Central Derecho")
        elif self.labelDP == "d":
            print("Central Izquierdo")
        elif self.labelDP == "p":
            print("Lateral Derecho")
        elif self.labelDP == "r":
            print("Lateral Izquierdo")
            
            
    def actualizarContadoresGUI(self):
        self.lblCaninoDerecho.config(text="Canino Derecho: " + str(self.CD))
        self.lblCaninoIzquierdo.config(text="Canino Izquierdo: " + str(self.CI))
        self.lblCentralDerecho.config(text="Central Derecho: " + str(str(self.CED)))
        self.lblCentralIzquierdo.config(text="Central Izquierdo: " + str(self.CEI))
        self.lblLateralDerecho.config(text="Lateral Derecho: " + str(self.LD))
        self.lblLateralIzquierdo.config(text="Lateral Izquierdo: " + str(self.LI))
                  

def main():
    root = tk.Tk() # Crear una instancia de tkinter -> todo lo que yo defina se va a quedar dentro de la raiz 
    root.title("Project")
    appRunCamera = Application(master=root)