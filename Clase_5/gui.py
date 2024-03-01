from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
# from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
import reportLog
import runCamera

class Application (ttk.Frame):

    def __init__(self, master=None):
        try:
            super().__init__(master) # se construya primero la jerarquía de la clase padre
            self.logReport = reportLog.ReportLog()
            self.camera = runCamera.runCamera(name="Camera_1") # Para camara web
            #self.camera = runCamera.runCamera(src= "C:/Users/julia/OneDrive/Escritorio/Vision_Artificial/Clase_5/video1.mp4", name="Camera_1") # para video
            self.master = master
            self.width = 1080
            self.height = 720
            self.master.geometry("%dx%d" % (self.width, self.height))
            self.pack
            self.panel = None

            self.createFrameZeros()
            self.createWidgets()
            self.logReport.logger.info("GUI created")
            self.master.mainloop()

        except Exception as e:
            self.logReport.logger.error("GUI no created: " + str(e)) 

    def createWidgets(self):
        self.fontText = font.Font(family="Helvetica", size=8, weight="normal") #Se crea una fuente para el texto
        self.lblNameCamera = tk.Label(self.master, text="Cámara 1", fg = '#000000') #Se crea un label para el nombre de la cámara
        self.lblNameCamera['font'] = self.fontText
        self.lblNameCamera.place(x=20, y=10)

        self.btnInitCamera = tk.Button(self.master, 
                                       text="Iniciar", 
                                       bg='#000000',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.initCameraProcess)
        self.btnInitCamera.place(x=150, y=560)

        self.btnStopCamera = tk.Button(self.master, 
                                       text="Parar", 
                                       bg='#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.stopCameraProcess)
        self.btnStopCamera.place(x=350, y=560)

    def initCameraProcess(self):
        self.camera.start()
        self.getFrameInlabel()
    
    def stopCameraProcess(self):
        self.camera.stop()
        self.createFrameZeros()
        

    def getFrameInlabel(self):
        try:
            if self.camera.grabbed:
                frameCamera = self.camera.frame #Se obtiene el frame de la cámara
                frame = cv2.resize(frameCamera, (640, 480)) #Se redimensiona el frame a 640x480 pixeles
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Se convierte el color de BGR a RGB
                imgArray = Image.fromarray(frame) #Extracción de la matriz de pixeles a un array
                imgTk = ImageTk.PhotoImage(image=imgArray) #Es para obtener un frame de tkinter
                self.lblVideo.configure(image=imgTk) #Se pasan las propiedades del frame al label
                self.lblVideo.image = imgTk #Se actualiza el label 
                self.lblVideo.after(10, self.getFrameInlabel) #Se actualiza el label cada 10 ms
                
        except Exception as e:
            self.logReport.logger.error("Error in getFrameInlabel: " + str(e))


    def createFrameZeros(self):
        self.lblVideo = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideo.place(x=20, y=20)
        frame = np.zeros((480, 640, 3), dtype=np.uint8) #Se crea un frame de 640x480 pixeles con 3 canales de color (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Se convierte el color de BGR a RGB
        imgArray = Image.fromarray(frame) #Extracción de la matriz de pixeles a un array
        imgTk = ImageTk.PhotoImage(image=imgArray) #Es para obtener un frame de tkinter
        self.lblVideo.configure(image=imgTk) #Se pasan las propiedades del frame al label
        self.lblVideo.image = imgTk #Se actualiza el label 

def main():
    root = tk.Tk() 
    root.title("My first GUI")
    appRunCamera = Application(master = root) #Se crea un objeto de la clase Application

