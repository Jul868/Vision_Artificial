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
import math

class Application(ttk.Frame): # Se le da estructura de un frame
    def __init__(self,master=None):
        try:
            super().__init__(master)
            self.logReport = reportlog.ReportLog()
            
            #self.camera = runCamera.RunCamera(0)
            self.camera = runCamera.RunCamera(src="video/video_1_7.avi", name="video_1")

            self.master = master
            self.width = 1280 # Ancho de la ventana
            self.height = 600
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
        self.lbl3.place(x=20, y=320)
        self.lbl3.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lbl3.image = imgTk

        self.lbl4 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lbl4.place(x=370, y=320)
        self.lbl4.configure(image = imgTk) # Le paso las propiedades de imgTk
        self.lbl4.image = imgTk
    
    def createWidgets(self):
        # crear un font centrado y con negrilla
        self.fontText = font.Font(family='Helvetica', size=12, weight='bold') # Tipo de letra y tamaño que se quiere usar 
        self.lblNameCamera = tk.Label(self.master, text="Imagen en Tiempo real", fg="#000000")
        self.lblNameCamera['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCamera.place(x=20, y=5) # Ubico el texto 

        self.lblNameCameraBinary = tk.Label(self.master, text="Imagen Binarizada", fg="#000000")
        self.lblNameCameraBinary['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCameraBinary.place(x=370, y=5) # Ubico el texto

        self.lblNameCameraROI= tk.Label(self.master, text="Imagen ROI a analizar", fg="#000000")
        self.lblNameCameraROI['font'] = self.fontText # Toma la propiedad del texto 
        self.lblNameCameraROI.place(x=20, y=300) # Ubico el texto 

        self.lblNameCameraCONT = tk.Label(self.master, text="ROI - Detección Circulo Interno", fg="#000000")
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


        # Monedas 100 
        moneda100 = str(self.moneda_100)
        self.lblMoneda100 = tk.Label(self.master, text="Tensor 1: "+ moneda100, fg="#000000")
        self.lblMoneda100['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda100.place(x=720, y=60) # Ubico el texto 

        # Monedas 200 
        moneda200 = str(self.moneda_200)
        self.lblMoneda200 = tk.Label(self.master, text="Tensor 2: "+ moneda200, fg="#000000")
        self.lblMoneda200['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda200.place(x=720, y=80) # Ubico el texto 

        # Monedas 500 
        moneda500 = str(self.moneda_500)
        self.lblMoneda500 = tk.Label(self.master, text="Argolla 1: "+ moneda500, fg="#000000")
        self.lblMoneda500['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda500.place(x=720, y=100) # Ubico el texto 

        # Monedas 1000 
        moneda1000 = str(self.moneda_1000)
        self.lblMoneda1000 = tk.Label(self.master, text="Argolla 2: "+ moneda1000, fg="#000000")
        self.lblMoneda1000['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda1000.place(x=720, y=120) # Ubico el texto

        # Total de Piezas
        total = str(self.moneda_100 + self.moneda_200 + self.moneda_500 + self.moneda_1000)
        self.lblTotalMoneda = tk.Label(self.master, text="Total de Piezas: "+ total, fg="#000000")
        self.lblTotalMoneda['font'] = self.fontText # Toma la propiedad del texto 
        self.lblTotalMoneda.place(x=720, y=150) # Ubico el texto


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
        self.getFrameInLabelBinary()
        self.getFrameCont()
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
                self.lblVideo.after(180, self.getFrameInLabel) # Cada cuanto se va a pedir un label 

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabel" + str(e)) 


    def getFrameInLabelBinary(self):
        try:
            if (self.camera.grabbed):
                self.camera.getFrameBinary((0, 0, 50), (229, 255, 255))
                frameCamera = self.camera.frameBinary
                self.frame2 = cv2.resize(frameCamera, (320,240))
                imgArray2 = Image.fromarray(self.frame2)  
                imgTk2 = ImageTk.PhotoImage(image=imgArray2) 
                self.lblVideoBinary.configure(image = imgTk2)
                self.lblVideoBinary.image = imgTk2
                self.lblVideoBinary.bind("<Button-1>", self.event_click2)

                self.totalMonedas()
                self.identificarPiezas()
                self.lblVideoBinary.after(180, self.getFrameInLabelBinary)

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
            #self.camera.getimgROI(self.x1, self.y1, self.x2, self.y2, 1)
            #self.getFrameROI()
            
            
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

    def getFrameCont(self):
        try:
            if self.camera.grabbed:
                self.imgContours = self.camera.imgContours
                # Verificar si es necesario convertir la imagen a BGR o RGB dependiendo del número de canales
                if len(self.imgContours.shape) == 2:  # Si es imagen en escala de grises
                    self.frame4 = cv2.cvtColor(self.imgContours, cv2.COLOR_GRAY2RGB)
                else:  # Si es imagen a color
                    self.frame4 = cv2.cvtColor(self.imgContours, cv2.COLOR_BGR2RGB)
                self.frame4 = cv2.resize(self.frame4, (320, 240))
                imgArray4 = Image.fromarray(self.frame4)
                imgTk4 = ImageTk.PhotoImage(image=imgArray4)
                self.lbl4.configure(image=imgTk4)
                self.lbl4.image = imgTk4
                self.lbl4.after(200, self.getFrameCont)
                #lets calculate circle area of the imgCountours
                self.circArea = self.camera.areaCirc
                circ = str(self.circArea)
                self.lblTotalMoneda = tk.Label(self.master, text="area: "+ circ, fg="#000000")
                self.lblTotalMoneda['font'] = self.fontText # Toma la propiedad del texto 
                self.lblTotalMoneda.place(x=720, y=200)
                
        except Exception as e:
            self.logReport.logger.error("Error in getFrameCont: " + str(e))




    
    def totalMonedas(self):
        try:
            self.frameBinary = self.camera.frameBinary
            franja = np.sum(self.frameBinary[:,159])
            franja = franja/255
            # print(franja)

            if (franja > 100 and self.moneda):
                print("se detecto un objeto")
                #self.total_monedas += 1
                self.actualizarContadoresGUI()
                self.moneda = False
                
            if(franja < 100):
                self.moneda = True
            
            # print(self.moneda)
        
        except Exception as e:
            self.logReport.logger.error("Error in totalMonedas" + str(e)) 

    def identificarPiezas(self):
        try: 
            franja = np.sum(self.frameBinary[:,0:320])
            franja = franja/255

            # Encontrar los contornos en la imagen binaria
            contours, _ = cv2.findContours(self.frameBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            if len(contours) > 0:
                for contour in contours:
                    area = cv2.contourArea(contour)
                    xx,yy,ww,hh = cv2.boundingRect(contour)
                    #print("xx", xx, "yy", yy, "ww", ww, "hh", hh)
                    self.array=np.append(self.array,area)
                    print("area", area)
            else:
                area = 0
            
            if (franja>100 and self.bandera):
                print("se detecto un objeto")
                self.bandera=False
                self.camera.getimgROI(xx-50, yy-50, xx+ww-100, yy+hh-100, 1)
                self.getFrameROI()
                self.camera.imgCont()
                self.getFrameCont()
            
            elif (franja<100 and not self.bandera):
                maximo_pixeles = np.max(self.array)
                print("el maximo de pixeles es", maximo_pixeles)

                # Monedas 1000
                if maximo_pixeles>9000 and maximo_pixeles<13000:
                    self.moneda_1000 = self.moneda_1000+1
                    self.total_monedas += 1
                    self.actualizarContadoresGUI()
                    

                # Monedas 500
                if maximo_pixeles>13000 and maximo_pixeles<18000:
                    self.moneda_500 = self.moneda_500+1
                    self.total_monedas += 1
                    self.actualizarContadoresGUI()

                    

                # Monedas 200
                if maximo_pixeles>1800 and maximo_pixeles<6000:
                    self.moneda_200 = self.moneda_200+1
                    self.total_monedas += 1
                    self.actualizarContadoresGUI()

                    

                # Monedas 100
                if maximo_pixeles>18000 and maximo_pixeles<35000:
                    self.moneda_100 = self.moneda_100+1
                    self.total_monedas += 1
                    self.actualizarContadoresGUI()

                    

                self.array=np.array([1,1])
                self.bandera = True

        except Exception as e:
            self.logReport.logger.error("Error in identificarMonedas" + str(e))  
            
    def actualizarContadoresGUI(self):
        self.lblMoneda100.config(text="Tensor 1: " + str(self.moneda_100))
        self.lblMoneda200.config(text="Tensor 2: " + str(self.moneda_200))
        self.lblMoneda500.config(text="Argolla 1: " + str(self.moneda_500))
        self.lblMoneda1000.config(text="Argolla 2: " + str(self.moneda_1000))
        self.lblTotalMoneda.config(text="Total de Piezas: " + str(self.total_monedas))
                  

def main():
    root = tk.Tk() # Crear una instancia de tkinter -> todo lo que yo defina se va a quedar dentro de la raiz 
    root.title("Project")
    appRunCamera = Application(master=root)