from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from tkinter import messagebox
import os
import joblib
import numpy as np
import tkinter.font as font 

contador = 1
escala = 1
AREA_THRESHOLD = 30  # Definir un umbral de área mínima para los contornos

class Application(ttk.Frame):
    def __init__(self, master=None):
        global contador, escala
        super().__init__(master)
        self.master = master
        self.width = 1280
        self.height = 600
        self.master.geometry("%dx%d" % (self.width, self.height))
        self.pack()

        self.PapaB = 0
        self.PapaM = 0
        self.TomateB = 0
        self.TomateM = 0
        self.cebollaB = 0
        self.cebollaM = 0
        self.LimonB = 0
        self.LimonM = 0

        self.image_list = [f for f in os.listdir("images") if f.lower().endswith(".jpeg")]  # Lista de imágenes
        if not self.image_list:
            messagebox.showinfo("Info", "No hay imágenes para mostrar.")
            self.master.destroy()
            return
        
        self.image_index = 0
        self.contour_index = 0
        self.contours = []
        self.nameImg = self.image_list[self.image_index]
        self.image_path = "images/" + self.nameImg

        self.createWidgets()
        self.loadImage()

        self.master.bind("<Right>", self.next_image)
        self.master.bind("<c>", self.next_contour)

    def createWidgets(self):
        global escala
        self.btnSalir = Button(self.master,
                                       text="Cerrar",
                                       bg = '#C0392B',
                                       fg='#FFFFFF',
                                       width=12,
                                       command=self.Salir)
        self.btnSalir.place(x=800, y=450)

        self.fontText = font.Font(family='Helvetica', size=12, weight='bold') # Tipo de letra y tamaño que se quiere usar 
        self.lblOriginalImage = Label(self.master, borderwidth=2, relief="solid")
        self.lblOriginalImage.place(x=20, y=25)
        self.lblOriginalName = Label(self.master, text="Imagen Original", fg='#000000')
        self.lblOriginalName.place(x=20, y=5)

        self.lblBinImage = Label(self.master, borderwidth=2, relief="solid")
        self.lblBinImage.place(x=380, y=20)
        self.lblBinName = Label(self.master, text="Binarizada", fg='#000000')
        self.lblBinName.place(x=370, y=5)

        self.lblContourImage = Label(self.master, borderwidth=2, relief="solid")
        self.lblContourImage.place(x=20, y=320)
        self.lblContourName = Label(self.master, text="Contorno", fg='#000000')
        self.lblContourName.place(x=20, y=300)
        
        # self.lblNumContours = Label(self.master, text="Número de contornos: 0", fg='#000000')
        # self.lblNumContours.place(x=370, y=320)

        # Canino Derecho 
        self.lblCebollaB = Label(self.master, text="Cebolla Buena: "+ str(self.cebollaB), fg="#000000")
        self.lblCebollaB['font'] = self.fontText # Toma la propiedad del texto 
        self.lblCebollaB.place(x=720, y=60) # Ubico el texto
        
        # Canino Izquierdo
        self.lblCebollaM = Label(self.master, text="Cebolla Mala: "+ str(self.cebollaM), fg="#000000")
        self.lblCebollaM['font'] = self.fontText # Toma la propiedad del texto
        self.lblCebollaM.place(x=720, y=80) # Ubico el texto
        
        # Central Derecho
        self.lblLimonB = Label(self.master, text="Limon Bueno: "+ str(self.LimonB), fg="#000000")
        self.lblLimonB['font'] = self.fontText # Toma la propiedad del texto
        self.lblLimonB.place(x=720, y=100) # Ubico el texto
        
        # Central Izquierdo
        self.lblLimonM = Label(self.master, text="Limon malo: "+ str(self.LimonM), fg="#000000")
        self.lblLimonM['font'] = self.fontText # Toma la propiedad del texto
        self.lblLimonM.place(x=720, y=120) # Ubico el texto
        
        # Lateral Derecho
        self.lblPapaB = Label(self.master, text="Papa Buena: "+ str(self.PapaB), fg="#000000")
        self.lblPapaB['font'] = self.fontText # Toma la propiedad del texto
        self.lblPapaB.place(x=720, y=140) # Ubico el texto
        
        # Lateral Izquierdo
        self.lblPapaM = Label(self.master, text="Papa Mlaa: "+ str(self.PapaM), fg="#000000")
        self.lblPapaM['font'] = self.fontText # Toma la propiedad del texto
        self.lblPapaM.place(x=720, y=160) # Ubico el texto

        #Tomate Bueno
        self.lblTomateB = Label(self.master, text="Tomate Bueno: "+ str(self.TomateB), fg="#000000")
        self.lblTomateB['font'] = self.fontText # Toma la propiedad del texto
        self.lblTomateB.place(x=720, y=180)

        #Tomate Malo
        self.lblTomateM = Label(self.master, text="Tomate Malo: "+ str(self.TomateM), fg="#000000")
        self.lblTomateM['font'] = self.fontText # Toma la propiedad del texto
        self.lblTomateM.place(x=720, y=200)

    def Salir(self):
        respuesta = messagebox.askyesno("Confirmar salida", "¿Está seguro de que desea salir?")
        if respuesta:
            self.master.destroy()

    def next_image(self, event):
        self.image_index += 1
        if self.image_index >= len(self.image_list):
            self.Salir()
        else:
            self.contour_index = 0
            self.nameImg = self.image_list[self.image_index]
            self.image_path = "images/" + self.nameImg
            self.loadImage()

    def next_contour(self, event):
        if self.contours:
            self.contour_index += 1
            if self.contour_index >= len(self.contours):
                self.next_image(event)
            else:
                self.show_contour()

    def loadImage(self):
        global escala
        print(self.image_path)
        try:
            # Cargar y mostrar imagen original
            self.img_color = cv2.imread(self.image_path)
            img = Image.fromarray(cv2.cvtColor(self.img_color, cv2.COLOR_BGR2RGB))
            img = img.resize((320, 210))
            self.photo_original = ImageTk.PhotoImage(img)
            self.lblOriginalImage.configure(image=self.photo_original)
            
            # Convertir la imagen de BGR a HSV
            img_hsv = cv2.cvtColor(self.img_color, cv2.COLOR_BGR2HSV)

            # Definir el rango de HSV para la binarización
            lower_hsv = np.array([0, 0, 0])
            upper_hsv = np.array([225, 44, 255])

            # Aplicar la máscara
            self.img_bin = cv2.inRange(img_hsv, lower_hsv, upper_hsv)
            self.img_bin_resized = cv2.resize(self.img_bin, (320, 210))
            self.img_bin_resized=cv2.bitwise_not(self.img_bin_resized)
            self.photo_bin = ImageTk.PhotoImage(Image.fromarray(self.img_bin_resized))
            self.lblBinImage.configure(image=self.photo_bin)

            # Detectar contornos
            contours, _ = cv2.findContours(self.img_bin_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            self.contours = [cnt for cnt in contours if cv2.contourArea(cnt) > AREA_THRESHOLD]
            self.contour_index = 0
            #self.lblNumContours.config(text=f"Número de contornos: {len(self.contours)}")
            self.show_contour()

        except Exception as e:
            print("Error loading image:", str(e))

    def show_contour(self):
        if not self.contours:
            return

        self.img_color_aux = cv2.resize(self.img_color, (320, 210))
        img_with_contours = self.img_color_aux.copy()

        # Dibujar contornos en la imagen a color
        cv2.drawContours(img_with_contours, self.contours, -1, (0, 0, 255), 2)

        img_with_contours_resized = Image.fromarray(cv2.cvtColor(img_with_contours, cv2.COLOR_BGR2RGB))
        self.photo_contour = ImageTk.PhotoImage(img_with_contours_resized)
        self.lblContourImage.configure(image=self.photo_contour)

        # Ejecutar predicción del tipo de fruta para cada contorno
        self.MachineLearning()
        self.actualizarContadoresGUI()

    def MachineLearning(self):
        print("Machine Learning")
        self.mlp = joblib.load('ModelFrutas.joblib')  # Carga del modelo Machine Learning
        self.skl = joblib.load('ScalerFrutas.joblib')  # Carga del modelo Deep Learning.

        try:
            for cnt in self.contours:
                x, y, w, h = cv2.boundingRect(cnt)
                area = cv2.contourArea(cnt)  # Extraer patrones
                p = cv2.arcLength(cnt, True)  # Extraer patrones
                m = cv2.moments(cnt)  # Extraer patrones
                Hu = cv2.HuMoments(m)  # Extraer patrones
                aspecto = w / h
                excentricidad = np.sqrt(np.square(w) + np.square(h)) / 2
                if w > 30 and h > 30:
                    cv2.rectangle(self.img_color_aux, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    imgRoi = self.img_bin[y:y + h, x:x + w]
                    self.imgRoiResize = cv2.resize(imgRoi, (40, 60))
                    # Dibujar contornos en imagen a color
                    cv2.drawContours(self.img_color_aux, [cnt], -1, (0, 255, 0), 2)

                    # vectorCaract = np.array([area,p,w,h,Hu[0][0], Hu[1][0], Hu[2][0], Hu[3][0],aspecto,excentricidad], dtype = np.float32)
                    vectorCaract = self.imgRoiResize.flatten()
                    vectorReshape = vectorCaract.reshape(1, -1)
                    vectorSKL = self.skl.transform(vectorReshape)
                    self.result = self.mlp.predict(vectorSKL)

                    if int(self.result[0]) == 0:
                        print("La fruta es: ", 'Cebolla')
                        self.cebollaB = self.cebollaB + 1

                    elif int(self.result[0]) == 1:
                        print("La fruta es: ", 'Cebolla')
                        self.cebollaM = self.cebollaM + 1

                    elif int(self.result[0]) == 2:
                        print("La fruta es:", "Limón")
                        self.LimonB = self.LimonB + 1

                    elif int(self.result[0]) == 3:
                        print("La fruta es:", "Limón")
                        self.LimonM = self.LimonM + 1

                    elif int(self.result[0]) == 4:
                        print("La fruta es:", "Papa")
                        self.PapaB = self.PapaB + 1

                    elif int(self.result[0]) == 5:
                        print("La fruta es:", "Papa")
                        self.PapaM = self.PapaM + 1

                    elif int(self.result[0]) == 6:
                        print("La fruta es:", "Tomate")
                        self.TomateB = self.TomateB + 1

                    elif int(self.result[0]) == 7:
                        print("La fruta es:", "Tomate")
                        self.TomateM = self.TomateM + 1

        except Exception as e:
            self.logReport.logger.error("Error in MachineLearning: " + str(e))



    def actualizarContadoresGUI(self):
        self.lblCebollaB.config(text="Cebolla Buena: " + str(self.cebollaB))
        self.lblCebollaM.config(text="Cebolla Mala: " + str(self.cebollaM))
        self.lblLimonB.config(text="Limon Bueno: " + str(str(self.LimonB)))
        self.lblLimonM.config(text="Limon Malo: " + str(self.LimonM))
        self.lblPapaB.config(text="Papa Buena: " + str(self.PapaB))
        self.lblPapaM.config(text="Papa Mala: " + str(self.PapaM))
        self.lblTomateB.config(text="Tomate Bueno: " + str(self.TomateB))
        self.lblTomateM.config(text="Tomate Malo: " + str(self.TomateM))

def main():
    root = Tk()
    root.title("My first GUI")
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
