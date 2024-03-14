from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font 
# from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

import cv2
import numpy as np
import reportlog
import runCamera

class Application(ttk.Frame): # Se le da estructura de un frame
    def _init_(self,master=None):
        try:
            super()._init_(master)
            self.logReport = reportlog.ReportLog()

            self.master = master
            self.width = 1080
            self.height = 720
            self.master.geometry("%dx%d" % (self.width, self.height))
            self.pack
            self.panel = None

            self.btnPath()
            self.createWidgets()
            self.on_button_click()
            self.logReport.logger.info("GUI created")
            self.master.mainloop()

        except Exception as e:
            self.logReport.logger.error("GUI no created" + str(e)) 
    
    def btnPath(self):
        self.path = tk.Entry(self.master, width=30)
        self.path.place(x=20, y=470)

        self.size = tk.Entry(self.master, width=30)
        self.size.place(x=20, y=520)

        self.boton = tk.Button(self.master,
                                text="Aceptar", 
                                bg = '#007A39',
                                fg='#FFFFFF',
                                command=self.on_button_click)
        self.boton.place(x=350, y=470)
        
        self.MedianBlur = tk.Button(self.master, 
                                       text="MedianBlur", 
                                       bg='#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.MBlur)
        self.Erode = tk.Button(self.master, 
                                       text="Erode", 
                                       bg='#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.Erd)
    
    def on_button_click(self):
        try:
            entered_img = self.path.get()
            entered_size = int(self.size.get())

            Path = 'images/'+entered_img
        
            img = cv2.imread(Path)
            h, w = self.img.shape[:2]
            img = cv2.resize(img, (w, h), interpolation = cv2.INTER_CUBIC)
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            self.label_imagen = tk.Label(self.master, image=img)
            self.label_imagen.image = img 
            self.label_imagen.pack()

            print("Texto ingresado:", entered_img, "size", entered_size)

        except Exception as e:
            self.logReport.logger.error("Error in on_button_click " + str(e))
    
    
    def createWidgets(self):
        self.fontText = font.Font(family='Helvetica', size=15, weight='normal') 
        self.lblNameConf = tk.Label(self.master, text="Parámetros de configuración", fg="#000000")
        self.lblNameConf['font'] = self.fontText 
        self.lblNameConf.place(x=20, y=400) 
        
        self.fontText1 = font.Font(family='Helvetica', size=8, weight='normal')
        self.lblNameImg = tk.Label(self.master, text="Nombre de la imagen a procesar", fg="#000000")
        self.lblNameImg['font'] = self.fontText1
        self.lblNameImg.place(x=20, y=450)

        self.lblNameImg = tk.Label(self.master, text="Escala a redimensionar", fg="#000000")
        self.lblNameImg['font'] = self.fontText1
        self.lblNameImg.place(x=20, y=500)

        """self.btnInitCamera = tk.Button(self.master,
                                       text="Iniciar",
                                       bg = '#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.initCameraProcess)
        self.btnInitCamera.place(x=150, y=560)

        self.btnStopCamera = tk.Button(self.master,
                                       text="Parar",
                                       bg = '#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.stopCameraProcess)
        self.btnStopCamera.place(x=350, y=560)"""


    def initCameraProcess(self):
        self.camera.start()
        self.getFrameInLabel()
        print("init")

    def stopCameraProcess(self):
        print("stop")

    def getFrameInLabel(self):
        try:
            if (self.camera.grabbed):
                frameCamera = self.camera.frame 
                frame = cv2.resize(frameCamera, (640,480))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                imgArray = Image.fromarray(frame)  
                imgTk = ImageTk.PhotoImage(image=imgArray) 
                self.lblVideo.configure(image = imgTk)
                self.lblVideo.image = imgTk
                self.lblVideo.after(30, self.getFrameInLabel) 

        except Exception as e:
            self.logReport.logger.error("Error in getFrameInLabel" + str(e))


def main():
    root = tk.Tk() # Crear una instancia de tkinter -> todo lo que yo defina se va a quedar dentro de la raiz 
    root.title("My first GUI")
    appRunCamera = Application(master=root)