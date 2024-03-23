# Graphic user interface (gui)
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
            
            #self.camera = runCamera.RunCamera(0)
            self.camera = runCamera.RunCamera(src="video/video1.mp4", name="video_1")

            self.master = master
            self.width = 1280 # Ancho de la ventana
            self.height = 400
            self.master.geometry("%dx%d" % (self.width, self.height))
            self.pack
            self.panel = None

            self.total_monedas = 0
            self.moneda = True
            self.bandera = True
            self.array = np.array([1,1])
            
            self.x1 = -1
            self.y1 = -1
            self.x2 = -1
            self.y2 = -1
            
            self.band1 = False
            self.band2 = True

            self.moneda_1000 = 0
            self.moneda_500 = 0
            self.moneda_100 = 0
            self.moneda_200 = 0
            self.moneda_50 = 0

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
        
        self.lbl3 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lbl3.place(x=870, y=25)
        self.lbl3.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lbl3.image = imgTk
    
    def createWidgets(self):
        self.fontText = font.Font(family='Helvetica', size=8, weight='normal') # Tipo de letra y tamaño que se quiere usar 
        self.lblNameCamera = tk.Label(self.master, text="Video Monedas", fg="#000000")
        self.lblNameCamera['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCamera.place(x=20, y=5) # Ubico el texto 

        self.lblNameCameraBinary = tk.Label(self.master, text="Video Monedas Binario", fg="#000000")
        self.lblNameCameraBinary['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCameraBinary.place(x=370, y=5) # Ubico el texto 

        # Monedas 50 
        moneda50 = str(self.moneda_50)
        self.lblMoneda50 = tk.Label(self.master, text="Monedas de 50: "+ moneda50, fg="#000000")
        self.lblMoneda50['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda50.place(x=720, y=30) # Ubico el texto 

        # Monedas 100 
        moneda100 = str(self.moneda_100)
        self.lblMoneda100 = tk.Label(self.master, text="Monedas de 100: "+ moneda100, fg="#000000")
        self.lblMoneda100['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda100.place(x=720, y=50) # Ubico el texto 

        # Monedas 200 
        moneda200 = str(self.moneda_200)
        self.lblMoneda200 = tk.Label(self.master, text="Monedas de 200: "+ moneda200, fg="#000000")
        self.lblMoneda200['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda200.place(x=720, y=70) # Ubico el texto 

        # Monedas 500 
        moneda500 = str(self.moneda_500)
        self.lblMoneda500 = tk.Label(self.master, text="Monedas de 500: "+ moneda500, fg="#000000")
        self.lblMoneda500['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda500.place(x=720, y=90) # Ubico el texto 

        # Monedas 1000 
        moneda1000 = str(self.moneda_1000)
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
        
        self.sliderL = Scale(self.master, from_=0, to=256, orient=tk.HORIZONTAL, length=100, label="Limite Inferior", command=self.slider_callback)
        self.sliderL.place(x=350, y=300)
        self.sliderL.set(15)

        self.sliderR = Scale(self.master, from_=0, to=256, orient=tk.HORIZONTAL, length=100, label="Limite Superior", command=self.slider_callback)
        self.sliderR.place(x=350, y=350)
        self.sliderR.set(255)
        
    def slider_callback(self, value):
        print('value: ', value)
        print("Slider L:", self.sliderL.get())
        print("Slider R:", self.sliderR.get())

    def initCameraProcess(self):
        self.camera.start()
        self.getFrameInLabel()
        self.getFrameInLabelBinary()
        self.num_monedas = 0 
        self.moneda_1000 = 0
        self.moneda_500 = 0
        self.moneda_100 = 0
        self.moneda_200 = 0
        self.moneda_50 = 0
        # print("init")

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
                self.lblVideo.after(90, self.getFrameInLabel) # Cada cuanto se va a pedir un label 

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabel" + str(e)) 


    def getFrameInLabelBinary(self):
        try:
            if (self.camera.grabbed):
                self.camera.getFrameBinary((0, 0, self.sliderL.get()), (229, 255, self.sliderR.get()))
                frameCamera = self.camera.frameBinary
                self.frame2 = cv2.resize(frameCamera, (320,240))
                imgArray2 = Image.fromarray(self.frame2)  
                imgTk2 = ImageTk.PhotoImage(image=imgArray2) 
                self.lblVideoBinary.configure(image = imgTk2)
                self.lblVideoBinary.image = imgTk2
                self.lblVideoBinary.bind("<Button-1>", self.event_click2)

                self.totalMonedas()
                self.identificarMonedas()
                self.lblVideoBinary.after(90, self.getFrameInLabelBinary)

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabelBinary" + str(e))
            
    def event_click2(self, event):
        if(self.band1 == False):
            self.x1 = event.x
            self.y1 = event.y
            self.band1 = True
            self.band2 = False
            print("Label clicked at x1={}, y1={}".format(self.x1, self.y1))
        elif(self.band2 == False):
            self.x2 = event.x
            self.y2 = event.y
            self.band2 = True
            self.band1 = False
            print("Label clicked at x2={}, y2={}".format(self.x2, self.y2))
            self.camera.getimgROI(self.x1, self.y1, self.x2, self.y2, 1)
            self.getFrameROI()
            
    def getFrameROI(self):
        try:
            if (self.camera.grabbed):
                frameROI = self.camera.imgROI
                self.frame3 = cv2.resize(frameROI, (320,240))
                self.frame3 = cv2.cvtColor(self.frame3, cv2.COLOR_BGR2RGB) 
                imgArray3 = Image.fromarray(self.frame3)  
                imgTk3 = ImageTk.PhotoImage(image=imgArray3) 
                self.lbl3.configure(image=imgTk3)  # Configura la imagen en el Label
                self.lbl3.image = imgTk3  # Actualiza la referencia a la imagen para evitar que Python la elimine de la memoria

        except Exception as e:
            self.logReport.logger.error("Error in getFrameROI" + str(e))

    
    def totalMonedas(self):
        try:
            self.frameBinary = self.camera.frameBinary
            franja = np.sum(self.frameBinary[:,159])
            franja = franja/255
            # print(franja)

            if (franja > 10 and self.moneda):
                # print("se detecto un objeto")
                self.total_monedas += 1
                self.moneda = False
                
            if(franja < 10):
                self.moneda = True
            
            # print(self.moneda)
            total = str(self.total_monedas)
            self.lblTotalMoneda = tk.Label(self.master, text="Total monedas: "+ total, fg="#000000")
            self.lblTotalMoneda['font'] = self.fontText # Toma la propiedad del texto 
            self.lblTotalMoneda.place(x=720, y=130) # Ubico el texto
        
        except Exception as e:
            self.logReport.logger.error("Error in totalMonedas" + str(e)) 

    def identificarMonedas(self):
        try: 
            franja = np.sum(self.frameBinary[:,0:320])
            franja = franja/255

            # Encontrar los contornos en la imagen binaria
            contours, _ = cv2.findContours(self.frameBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                for contour in contours:
                    area = cv2.contourArea(contour)
                    self.array=np.append(self.array,area)
            else:
                area = 0
            
            if (franja>1000 and self.bandera):
                print("se detecto un objeto")
                self.bandera=False
            
            elif (franja<1000 and not self.bandera):
                maximo_pixeles = np.max(self.array)
                print("el maximo de pixeles es", maximo_pixeles)

                # Monedas 1000
                if maximo_pixeles>28000 and maximo_pixeles<32000:
                    self.moneda_1000 = self.moneda_1000+1
                    self.actualizarContadoresGUI()
                    print("se detecto una moneda de 1000", self.moneda_1000)

                # Monedas 500
                if maximo_pixeles>5000 and maximo_pixeles<6000:
                    self.moneda_500 = self.moneda_500+1
                    self.actualizarContadoresGUI()

                    print("se detecto una moneda de 500", self.moneda_500)

                # Monedas 200
                if maximo_pixeles>4200 and maximo_pixeles<5000:
                    self.moneda_200 = self.moneda_200+1
                    self.actualizarContadoresGUI()

                    print("se detecto una moneda de 200", self.moneda_200)

                # Monedas 100
                if maximo_pixeles>3500 and maximo_pixeles<4200:
                    self.moneda_100 = self.moneda_100+1
                    self.actualizarContadoresGUI()

                    print("se detecto una moneda de 100", self.moneda_100)

                # Monedas 50 
                if maximo_pixeles>100 and maximo_pixeles<3500:
                    self.moneda_50 = self.moneda_50+1
                    self.actualizarContadoresGUI()
                    print("se detecto una moneda de 50", self.moneda_50)

                self.array=np.array([1,1])
                self.bandera = True

        except Exception as e:
            self.logReport.logger.error("Error in identificarMonedas" + str(e))  
            
    def actualizarContadoresGUI(self):
        self.lblMoneda50.config(text="Monedas de 50: " + str(self.moneda_50))
        self.lblMoneda100.config(text="Monedas de 100: " + str(self.moneda_100))
        self.lblMoneda200.config(text="Monedas de 200: " + str(self.moneda_200))
        self.lblMoneda500.config(text="Monedas de 500: " + str(self.moneda_500))
        self.lblMoneda1000.config(text="Monedas de 1000: " + str(self.moneda_1000))
                  

def main():
    root = tk.Tk() # Crear una instancia de tkinter -> todo lo que yo defina se va a quedar dentro de la raiz 
    root.title("Project")
    appRunCamera = Application(master=root)