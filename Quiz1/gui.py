from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
# from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import os
import sys
from tkinter import messagebox

import cv2
import numpy as np
import reportLog
import loadImage

class App(ttk.Frame):
    def __init__(self, master=None):
        try:
            super().__init__(master)
            self.logReport = reportLog.ReportLog()
            if not os.path.isfile('app/images/arm_1.png'):
                print(f"Error: The file does not exist")
                sys.exit(1)

            self.loaderImage = loadImage.LoadImage(path='app/images/fracture.jpg')
            self.master = master
            self.width = 1080
            self.height = 720
            self.master.geometry("%dx%d" % (self.width, self.height))
            self.pack
            self.panel = None
            self.bandImage = False
            self.x1 = -1
            self.y1 = -1
            self.x2 = -1
            self.y2 = -1
            self.band1 = False
            self.band2 = True

            self.createWidgets()
            self.createFrameZeros()
            self.logReport.logger.info("GUI created")
            self.master.mainloop()            

        except Exception as e:
            self.logReport.logger.error("GUI no created" + str(e))

    def createFrameZeros(self):
        self.lblVideo1 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideo1.place(x=20, y=20)
        frame1 = np.zeros([300, 300, 3], dtype=np.uint8)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        imgArray1 = Image.fromarray(frame1)
        imgTk1 = ImageTk.PhotoImage(image=imgArray1)
        self.lblVideo1.configure(image = imgTk1)
        self.lblVideo1.image = imgTk1

        self.lblVideo2 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideo2.place(x=330, y=20)
        frame2 = np.zeros([300, 300, 3], dtype=np.uint8)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        imgArray2 = Image.fromarray(frame2)
        imgTk2 = ImageTk.PhotoImage(image=imgArray2)
        self.lblVideo2.configure(image = imgTk2)
        self.lblVideo2.image = imgTk2

        self.lblVideo3 = tk.Label(self.master, borderwidth=2, relief="solid")
        self.lblVideo3.place(x=640, y=20)
        frame3 = np.zeros([300, 300, 3], dtype=np.uint8)
        frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
        imgArray3 = Image.fromarray(frame3)
        imgTk3 = ImageTk.PhotoImage(image=imgArray3)
        self.lblVideo3.configure(image = imgTk3)
        self.lblVideo3.image = imgTk3
    
    def createWidgets(self):
        self.fontText = font.Font(family='Helvetica', size=8, weight = 'normal')
        self.lblNameCamera = tk.Label(self.master, text="Cámara 1", fg='#000000')
        self.lblNameCamera['font'] = self.fontText
        self.lblNameCamera.place(x=20, y=5)

        self.btnInitProcess = tk.Button(self.master,
                                       text="Iniciar",
                                       bg='#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.InitProcess)
        self.btnInitProcess.place(x=950, y=30)

        self.btnStopProcess = tk.Button(self.master,
                                       text="Limpiar",
                                       bg='#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.stopProcess)
        self.btnStopProcess.place(x=950, y=80)

        self.btnDilateProcess = tk.Button(self.master,
                                       text="Dilatar",
                                       bg='#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.dilateProcess)
        self.btnDilateProcess.place(x=950, y=130)

        self.btnFilterProcess = tk.Button(self.master,
                                       text="Filtrar",
                                       bg='#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.filterProcess)
        self.btnFilterProcess.place(x=950, y=180)

        self.btnCloseProcess = tk.Button(self.master,
                                       text="Salir",
                                       bg='#007A39',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.closeProcess)
        self.btnCloseProcess.place(x=950, y=230)

        self.sliderL = Scale(self.master, from_=0, to=256, orient=tk.HORIZONTAL, command=self.slider_callback)
        self.sliderL.place(x=20, y=330)

        self.sliderR = Scale(self.master, from_=0, to=256, orient=tk.HORIZONTAL, command=self.slider_callback)
        self.sliderR.place(x=130, y=330)
        self.sliderR.set(255)

        self.sliderScale = Scale(self.master, from_=1, to=10, orient=tk.HORIZONTAL, command=self.slider_callback)
        self.sliderScale.place(x=250, y=330)

    def slider_callback(self, value):
        print('value: ', value)
        print("Slider L:", self.sliderL.get())
        print("Slider R:", self.sliderR.get())
        print("Slider Scale:", self.sliderScale.get())  
               
        if(self.bandImage):
            if(self.loaderImage.imgGray.any() is not None):
                self.loaderImage.getBinaryImageIR(self.sliderL.get(), self.sliderR.get())
                self.drawBinaryImage()
    

    def InitProcess(self):
        print('init ', self.sliderR.get() )
        self.loaderImage.getColorImage()
        self.loaderImage.getGrayImage()
        self.bandImage = True
        self.drawRealImage()
    
    def stopProcess(self):
        print("stop")
        self.bandImage = False
        self.createFrameZeros()

    def dilateProcess(self):
        print('dilate')

    def filterProcess(self):
        print('filter')
    
    def closeProcess(self):
        response = messagebox.askquestion("Salir", "¿Estás seguro de que quieres salir?")
        if response == "yes":
            self.master.destroy()
    
    def drawRealImage(self):
        try:
            if(self.loaderImage.imgColor.any() is not None):
                img1 = self.loaderImage.imgColor
                frame1 = cv2.resize(img1, (300,300))
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                imgArray1 = Image.fromarray(frame1)
                imgTk1 = ImageTk.PhotoImage(image=imgArray1)
                self.lblVideo1.configure(image = imgTk1)
                self.lblVideo1.image = imgTk1
        except Exception as e:
            self.logReport.logger.info("Error in get image color " + str(e))

    def drawBinaryImage(self):
        try:
            if(self.loaderImage.imgBinaryIrColor.any() is not None):
                img2 = self.loaderImage.imgBinaryIrColor
                frame2 = cv2.resize(img2, (300,300))
                frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                imgArray2 = Image.fromarray(frame2)
                imgTk2 = ImageTk.PhotoImage(image=imgArray2)
                self.lblVideo2.configure(image = imgTk2)
                self.lblVideo2.image = imgTk2
                self.lblVideo2.bind("<Button-1>", self.event_click2)
        except Exception as e:
            self.logReport.logger.info("Error in get binary image " + str(e))
    
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
            self.loaderImage.drawROI(self.x1, self.y1, self.x2, self.y2, self.sliderScale.get())
            self.drawRoiImage()

    def drawRoiImage(self):
        try:
            if(self.loaderImage.imgROI.any() is not None):
                img3 = self.loaderImage.imgROI
                frame3 = cv2.resize(img3, (300,300))
                frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
                imgArray3 = Image.fromarray(frame3)
                imgTk3 = ImageTk.PhotoImage(image=imgArray3)
                self.lblVideo3.configure(image = imgTk3)
                self.lblVideo3.image = imgTk3
                #self.lblVideo3.bind("<Button-1>", self.event_click3)
        except Exception as e:
            self.logReport.logger.info("Error in get binary image " + str(e))
        


def main():
    root = tk.Tk()
    root.title("My first GUI")
    appRunCamera = App(master=root)