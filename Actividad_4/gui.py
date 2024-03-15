# Graphic user interface (gui)
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font 
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

import cv2
import numpy as np
import reportlog
import runCamera
import time

class Application(ttk.Frame): # Se le da estructura de un frame
    def __init__(self,master=None):
        try:
            super().__init__(master)
            self.logReport = reportlog.ReportLog()
            # pathCamUsb = 0
            # captureCamUsb = cv2.VideoCapture(pathCamUsb, cv2.CAP_DSHOW)
            self.camera = runCamera.RunCamera(src="video/video1.mp4", name="video_1") 

            self.master = master
            self.width = 1080
            self.height = 400
            self.master.geometry("%dx%d" % (self.width, self.height))
            self.pack
            self.panel = None

            self.num_monedas = 0
            self.moneda = True

            self.createWidgets()
            self.createFrameZeros()
            self.logReport.logger.info("GUI created")
            self.master.mainloop()

        except Exception as e:
            self.logReport.logger.error("GUI no created" + str(e)) 

        
    def createFrameZeros(self):
        self.lblVideo = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideo.place(x=20, y=25)

        # Poner un frame en el label (poner un objeto sobre el panel)
        frame = np.zeros([240,320,3], dtype=np.uint8) # 480 de alto, 640 de ancho y una imagen de 3 colores (creo un recuadro negro)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # tkinter es RGB y cv2 es BGR (conversión para el formato de tkinter)
        imgArray = Image.fromarray(frame) # Extracción del formato 
        imgTk = ImageTk.PhotoImage(image=imgArray) # Array convetido a la propiedad de PhotoImage 
        self.lblVideo.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lblVideo.image = imgTk

        self.lblVideoBinary = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideoBinary.place(x=370, y=25)
        self.lblVideoBinary.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lblVideoBinary.image = imgTk
    
    def createWidgets(self):
        self.fontText = font.Font(family='Helvetica', size=8, weight='normal') # Tipo de letra y tamaño que se quiere usar 
        self.lblNameCamera = tk.Label(self.master, text="Video Monedas", fg="#000000")
        self.lblNameCamera['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCamera.place(x=20, y=5) # Ubico el texto 

        self.lblNameCameraBinary = tk.Label(self.master, text="Video Monedas Binario", fg="#000000")
        self.lblNameCameraBinary['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCameraBinary.place(x=370, y=5) # Ubico el texto 

        # Monedas 50 
        moneda50 = str(0)
        self.lblMoneda50 = tk.Label(self.master, text="Monedas de 50: "+ moneda50, fg="#000000")
        self.lblMoneda50['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda50.place(x=720, y=30) # Ubico el texto 

        # Monedas 100 
        moneda100 = str(0)
        self.lblMoneda100 = tk.Label(self.master, text="Monedas de 100: "+ moneda100, fg="#000000")
        self.lblMoneda100['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda100.place(x=720, y=50) # Ubico el texto 

        # Monedas 200 
        moneda200 = str(0)
        self.lblMoneda200 = tk.Label(self.master, text="Monedas de 200: "+ moneda200, fg="#000000")
        self.lblMoneda200['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda200.place(x=720, y=70) # Ubico el texto 

        # Monedas 500 
        moneda500 = str(0)
        self.lblMoneda500 = tk.Label(self.master, text="Monedas de 500: "+ moneda500, fg="#000000")
        self.lblMoneda500['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda500.place(x=720, y=90) # Ubico el texto 

        # Monedas 1000 
        moneda1000 = str(0)
        self.lblMoneda1000 = tk.Label(self.master, text="Monedas de 1000: "+ moneda1000, fg="#000000")
        self.lblMoneda1000['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda1000.place(x=720, y=110) # Ubico el texto 

        self.btnInitCamera = tk.Button(self.master,
                                       text="Iniciar",
                                       bg = '#45B39D',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.initCameraProcess)
        self.btnInitCamera.place(x=20, y=300)

        self.btnStopCamera = tk.Button(self.master,
                                       text="Parar",
                                       bg = '#5DADE2',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.stopCameraProcess)
        self.btnStopCamera.place(x=150, y=300)

        self.btnStopCamera = tk.Button(self.master,
                                       text="Cerrar",
                                       bg = '#C0392B',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.exit)
        self.btnStopCamera.place(x=20, y=350)

    def initCameraProcess(self):
        self.camera.start()
        self.getFrameInLabel()
        self.getFrameInLabelBinary()
        self.num_monedas = 0 
        # print("init")

    def stopCameraProcess(self):
        self.camera.stop()
        print("stop")

    def getFrameInLabel(self):
        try:
            if (self.camera.grabbed):
                frameCamera = self.camera.frame 
                frame = cv2.resize(frameCamera, (320,240))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                imgArray = Image.fromarray(frame)  
                imgTk = ImageTk.PhotoImage(image=imgArray) 
                self.lblVideo.configure(image = imgTk)
                self.lblVideo.image = imgTk
                self.lblVideo.after(10, self.getFrameInLabel) # Cada cuanto se va a pedir un label 

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabel" + str(e)) 


    def getFrameInLabelBinary(self):
        try:
            if (self.camera.grabbed):
                frameCamera = self.camera.frame 
                frame = cv2.resize(frameCamera, (320,240))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                self.frameBinary = cv2.inRange(frameHSV, (0, 0, 16), (255, 150, 255))
                imgArray2 = Image.fromarray(self.frameBinary)  
                imgTk2 = ImageTk.PhotoImage(image=imgArray2) 
                self.lblVideoBinary.configure(image = imgTk2)
                self.lblVideoBinary.image = imgTk2

                self.totalMonedas()
                self.lblVideoBinary.after(10, self.getFrameInLabelBinary)

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabelBinary" + str(e)) 

        
    def exit(self):
        respuesta = messagebox.askyesno("Confirmar salida", "¿Está seguro de que desea salir?")
        if respuesta:
            self.master.destroy()
    
    def totalMonedas(self):
        try: 
            franja = np.sum(self.frameBinary[:,159])
            franja = franja/255
            # print(franja)

            if (franja>100 and self.moneda):
                print("se detecto un objeto")
                self.num_monedas += 1
                self.moneda = False
                
            if(franja<10):
                self.moneda = True
            
            print(self.moneda)
            total = str(self.num_monedas)
            self.lblTotalMoneda = tk.Label(self.master, text="Total monedas: "+ total, fg="#000000")
            self.lblTotalMoneda['font'] = self.fontText # Toma la propiedad del texto 
            self.lblTotalMoneda.place(x=720, y=130) # Ubico el texto
        
        except Exception as e:
            self.logReport.logger.error("Error in totalMonedas" + str(e)) 

def main():
    root = tk.Tk() # Crear una instancia de tkinter -> todo lo que yo defina se va a quedar dentro de la raiz 
    root.title("Project")
    appRunCamera = Application(master=root)