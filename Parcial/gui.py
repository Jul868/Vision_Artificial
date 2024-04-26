# Graphic user interface (gui)
# Graphic user interface (gui)
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font 
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk, ImageDraw, ImageFont

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
            self.direction = "video/video_1_7.avi"
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
        moneda100 = str(self.tensor)
        self.lblMoneda100 = tk.Label(self.master, text="Tensor 1: "+ moneda100, fg="#000000")
        self.lblMoneda100['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda100.place(x=720, y=60) # Ubico el texto 

        # Monedas 200 
        moneda200 = str(self.tensor2)
        self.lblMoneda200 = tk.Label(self.master, text="Tensor 2: "+ moneda200, fg="#000000")
        self.lblMoneda200['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda200.place(x=720, y=80) # Ubico el texto 

        # Monedas 500 
        moneda500 = str(self.anillo)
        self.lblMoneda500 = tk.Label(self.master, text="Argolla 1: "+ moneda500, fg="#000000")
        self.lblMoneda500['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda500.place(x=720, y=100) # Ubico el texto 

        # Monedas 1000 
        moneda1000 = str(self.anillo2)
        self.lblMoneda1000 = tk.Label(self.master, text="Argolla 2: "+ moneda1000, fg="#000000")
        self.lblMoneda1000['font'] = self.fontText # Toma la propiedad del texto 
        self.lblMoneda1000.place(x=720, y=120) # Ubico el texto

        # Total de Piezas



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
        #self.getFrameInLabelBinary()
        #self.totalMonedas()
        
        #self.getFrameCont()
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
                self.getFrameInLabelBinary()
                self.identificarPiezas()
                
                self.lblVideo.after(60, self.getFrameInLabel) # Cada cuanto se va a pedir un label 

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabel" + str(e)) 


    def getFrameInLabelBinary(self):
        try:
            # Realiza la detección del objeto
            self.camera.getFrameBinary((0, 0, 25), (255, 255, 255))
            frameCamera = self.camera.frameBinary
            self.frame2 = cv2.resize(frameCamera, (320,240))

            
            contours, _ = cv2.findContours(self.frame2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                for contour in contours:
                    area = cv2.contourArea(contour)
                    self.xx,self.yy,self.ww,self.hh = cv2.boundingRect(contour)
                    #print("xx", xx, "yy", yy, "ww", ww, "hh", hh)

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabelBinary" + str(e))
            
            
            
    def getFrameROI(self):
        try:
            if (self.camera.grabbed):
                self.camera.getimgROI(self.xx, self.yy, self.xx+self.ww, self.yy+self.hh, 1)
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
                self.camera.imgCont()
                frameCont = self.camera.imgContours
                self.frame4 = cv2.resize(frameCont, (320, 240))
                self.frame4 = cv2.cvtColor(self.frame4, cv2.COLOR_BGR2RGB)
                imgArray4 = Image.fromarray(self.frame4)

                # Crear un objeto para dibujar en la imagen
                draw = ImageDraw.Draw(imgArray4)

                # Calcular el área del círculo y preparar el texto
                self.circArea = self.camera.areaCirc
                self.circArea = round(self.circArea, 2)
                circ_text = "Area del circulo: " + str(self.circArea)

                # Intentar cargar una fuente personalizada o utilizar una por defecto
                try:
                    #font.Font(family='Helvetica', size=12, weight='bold')
                    font_path = "Helvetica-Bold.ttf"  # Asegúrate de que el path a la fuente es correcto
                    font = ImageFont.truetype(font_path, 40)
                except Exception as e:
                    print("Error loading font:", e)
                    font = ImageFont.load_default()

                # Calcular el tamaño del texto con el objeto 'draw' y la fuente seleccionada
                text_bbox = draw.textbbox((0, 0), circ_text, font=font)
                text_height = text_bbox[3] - text_bbox[1]
                position = (10, imgArray4.height - text_height - 220)
                draw.text(position, circ_text, font=font, fill="#FF0000")

                # Convertir la imagen PIL a un objeto PhotoImage para usar en Tkinter
                imgTk4 = ImageTk.PhotoImage(image=imgArray4)
                self.lbl4.configure(image=imgTk4)
                self.lbl4.image = imgTk4
                    
        except Exception as e:
            self.logReport.logger.error("Error en getFrameCont: " + str(e))




    def identificarPiezas(self):
        try:
            #print("identificarPiezas")
            franja = np.sum(self.frame2[:,0:320])
            franja = franja/255
            franja2 = np.sum(self.frame2[:,60:200])
            franja2= franja2/255
            #print("franja: ", franja)
            contours, _ = cv2.findContours(self.frame2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
            
            if len(contours) > 0:
                #print("entrando al for")
                for contour in contours:
                    epsilon = 0.01 * cv2.arcLength(contour, True)
                    aprox = cv2.approxPolyDP(contour, epsilon, True)
                    #cv2.drawContours(self.frameBinary, [aprox], 0, (255, 0, 0), 3)
                    area = cv2.contourArea(aprox)
                    perimetro = cv2.arcLength(aprox, True)
                    circularidad = 4 * math.pi * area / (perimetro ** 2)
                    print("area", area)
                    print("circularidad", circularidad)
                    
                    if self.direction == "video/video_1_7.avi":
                        if circularidad >0.90 and area>6500:
                            self.bandera_anillo2=True
                            self.bandera_Tensor2=False
                        elif circularidad >0.90 and area>4000:
                            self.bandera_anillo1=True
                            self.bandera_Tensor1=False
                        elif circularidad <0.90 and area>7000:
                            self.bandera_Tensor2=True
                            self.bandera_Tensor1=False
                        elif area>4000:
                            self.bandera_Tensor2=False
                            self.bandera_Tensor1=True
                            
                    elif self.direction == "video/video_1_12.avi":
                        if circularidad >0.90 and area>4000:
                            self.bandera_anillo1=True
                            self.bandera_Tensor1=False
                        elif circularidad >0.90 and area>5200:
                            self.bandera_anillo2=True
                            self.bandera_Tensor2=False
                        elif circularidad <0.90 and area>7000:
                            self.bandera_Tensor1=True
                            self.bandera_Tensor2=False
                        elif area>4000:
                            self.bandera_Tensor1=False
                            self.bandera_Tensor2=True
                            
                    if franja2>100 and self.objeto2==True:
                        imgArray2 = Image.fromarray(self.frame2)  
                        imgTk2 = ImageTk.PhotoImage(image=imgArray2)
                        self.detected_object_image = imgTk2
                        self.lblVideoBinary.configure(image=self.detected_object_image)
                        self.lblVideoBinary.image = self.detected_object_image
                        self.getFrameROI()
                        self.getFrameCont()
                        self.objeto2=False

            else:
                area = 0
            

            if (franja > 500 and self.objeto):
                print("se detecto un objeto")

                self.total_objetos += 1
                self.objeto = False
                
            elif(franja < 500) and not(self.objeto) :
                #print("No se detecto un objeto")
                self.objeto = True
                if self.bandera_anillo1==True:
                    self.anillo = self.anillo+1
                    self.actualizarContadoresGUI()
                    #self.motor_controller.rotate_servo(36)
                    print("se detecto un anillo", self.anillo)
                # 
                elif self.bandera_Tensor1==True:
                    self.tensor = self.tensor+1
                    self.actualizarContadoresGUI()
                    #self.motor_controller.rotate_servo(72)
                    print("se detecto un tensor", self.tensor)
                elif self.bandera_anillo2==True:
                    self.anillo= self.anillo2+1
                    self.actualizarContadoresGUI()
                    #self.motor_controller.rotate_servo(36)
                    print("se detecto un anillo", self.anillo2)
                # 
                elif self.bandera_Tensor2==True:
                    self.tensor = self.tensor +self.tensor2+1
                    self.actualizarContadoresGUI()
                    #self.motor_controller.rotate_servo(72)
                    print("se detecto un tensor", self.tensor)
                self.bandera_anillo1=False
                self.bandera_Tensor1=True
                self.bandera_anillo2=False
                self.bandera_Tensor2=True
                self.objeto2=True
                
                total = str(self.total_objetos)
                self.lblTotalMoneda = tk.Label(self.master, text="Total de Piezas: "+ total, fg="#000000")
                self.lblTotalMoneda['font'] = self.fontText # Toma la propiedad del texto 
                self.lblTotalMoneda.place(x=720, y=150) # Ubico el texto

        except Exception as e:
            self.logReport.logger.error("Error in identificarMonedas" + str(e))  
            
    def actualizarContadoresGUI(self):
        self.lblMoneda100.config(text="Tensor 1: " + str(self.tensor))
        self.lblMoneda200.config(text="Tensor 2: " + str(self.tensor2))
        self.lblMoneda500.config(text="Argolla 1: " + str(str(self.anillo)))
        self.lblMoneda1000.config(text="Argolla 2: " + str(self.anillo2))
                  

def main():
    root = tk.Tk() # Crear una instancia de tkinter -> todo lo que yo defina se va a quedar dentro de la raiz 
    root.title("Project")
    appRunCamera = Application(master=root)