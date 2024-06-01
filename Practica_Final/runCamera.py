import reportlog
import cv2
import threading # Librería para subprocesos
import numpy as np
from glob import glob
import joblib


class RunCamera():
    def __init__(self, src=0, name="CameraThread"):
        try:
            self.name = name
            self.src = src
            self.capture = None
            self.grabbed = None
            self.frame = None
            self.logReport = reportlog.ReportLog()
            self.logReport.logger.info("Init runCamera process")
            self.CD = 0
            self.CI = 0
            self.CED = 0
            self.CEI = 0
            self.LD = 0
            self.LI = 0
            self.label = None

        except Exception as e:
            self.logReport.logger.error("Error runCamera process " + str(e))

    def start(self):
        try: 
            self.capture = cv2.VideoCapture(self.src)
            self.grabbed, self.frame = self.capture.read()
            
            if (self.capture.isOpened()): 
                self.running = True
                # Hilo -> subproceso que siempre se está ejecutando, un hilo no se puede quedar abierto 
                # Este hilo se encarga de leer el video 
                self.cameraThread = threading.Thread( # Thread es una función que me ayuda a crear y configurar un hilo 
                                                     target = self.get, name=self.name, daemon=True) # Lo que corre dentro del hilo 
                self.cameraThread.start()

        except Exception as e:
            self.logReport.logger.error("Error runCamera start " + str(e))
    
    def get(self):
        try: 
            while self.running and self.grabbed:
                self.grabbed, self.frame = self.capture.read()
                cv2.waitKey(30)
                if not self.grabbed:
                    break

        except Exception as e:
            self.logReport.logger.error("Error get frame " + str(e))

    def stop(self):
        try: 
            self.running = False
        except Exception as e:
            self.logReport.logger.error("Error runCamera stop " + str(e))
            
    def getFrameBinary(self, u1, u2):
        try:
            self.frameC = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frameHSV = cv2.cvtColor(self.frameC, cv2.COLOR_BGR2HSV)
            lower_bound = np.array([u1])
            upper_bound = np.array([u2])
            self.frameBinary = cv2.inRange(self.frameHSV, lower_bound, upper_bound)
        except Exception as e:
            self.logReport.logger.error("Error get frame binary " + str(e))
            
    def MachineLearning(self, mlp, skl):
        diente = True
        try:
            franja = np.sum(self.frameBinary[:, 120:200])
            franja = franja / 255
            contours, _ = cv2.findContours(self.frameBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if franja > 1000 and diente:
                diente = False
                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    area = cv2.contourArea(cnt) # Extraigo patrones
                    p = cv2.arcLength(cnt, True) # Extraigo patrones
                    m = cv2.moments(cnt) # Extraigo patrones
                    Hu = cv2.HuMoments(m) # Extraigo patrones
                    aspecto = w/h
                    excentricidad = np.sqrt(np.square(w) + np.square(h))/2
                    if w > 30 and h > 30:
                        cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        imgRoi = self.frameBinary[y:y + h, x:x + w]
                        self.imgRoiResize = cv2.resize(imgRoi, (40, 60))
                        
                        #vectorCaract = np.array([area,p,w,h,Hu[0][0], Hu[1][0], Hu[2][0], Hu[3][0],aspecto,excentricidad], dtype = np.float32)
                        vectorCaract = self.imgRoiResize.flatten()
                        vectorReshape = vectorCaract.reshape(1, -1)
                        vectorSKL = skl.transform(vectorReshape)
                        self.result = mlp.predict(vectorSKL)
                        
                        if int(self.result[0]) == 0:
                            print("el diente es: ", 'canino derecho')
                            self.CD = self.CD + 1
                            print("CD: ", self.CD)
                            
                        elif int(self.result[0]) == 1:
                            print("el diente es: ", 'canino izquierdo')
                            self.CI = self.CI + 1
                            
                        elif int(self.result[0]) == 2:
                            print("el diente es: ", 'central derecho')
                            self.CED = self.CED + 1

                        elif int(self.result[0]) == 3:
                            print("el diente es: ", 'central izquierdo')
                            self.CEI = self.CEI + 1
                            
                        elif int(self.result[0]) == 4:
                            print("el diente es: ", 'lateral derecho')
                            self.LD = self.LD + 1
                            
                        elif int(self.result[0]) == 5:
                            print("el diente es: ", 'lateral izquierdo')
                            self.LI = self.LI + 1
                        
                            
            elif franja < 500:
                diente = True
                        
        except Exception as e:
            self.logReport.logger.error("Error in MachineLearning: " + str(e))
            
    def DeepLearning(self, net):
        try:
            classes = []
            with open("model.names","r") as f: #Aqui se cargan las clases que se pueden detectar con el modelo YOLO 
                classes = [line.strip() for line in f.readlines()]

            layer_names = net.getLayerNames() #Aqui se obtienen los nombres de las capas del modelo YOLO
            outputlayers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()] #Aqui se obtienen las capas de salida del modelo YOLO 

            colors= np.random.uniform(0,255,size=(len(classes) + 1 ,3))

            #print(pathImg)
            img = self.frame
            self.imgDP = cv2.resize(img,None,fx=0.4,fy=0.3)
            height,width,channels = self.imgDP.shape

            #detecting objects
            blob = cv2.dnn.blobFromImage(self.imgDP,0.00392,(416,416),(0,0,0),True,crop=False) #Aqui se crea un blob de la imagen para poder pasarsela al modelo YOLO

            net.setInput(blob) #Aqui se le pasa la imagen al modelo YOLO
            outs = net.forward(outputlayers) #Aqui se obtienen las detecciones que se hicieron en la imagen

            #print(outs[1])


            #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
            class_ids=[]
            confidences=[]
            boxes=[]
            # if not outs:
            #     self.saveFrame = None
            for out in outs: #Aqui se recorren todas las detecciones que se hicieron en la imagen
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x= int(detection[0]*width)
                        center_y= int(detection[1]*height)
                        w = int(detection[2]*width)
                        h = int(detection[3]*height)

                        x=int(center_x - w/2)
                        y=int(center_y - h/2)

                        boxes.append([x,y,w,h]) #put all rectangle areas
                        self.saveFrame = self.imgDP[y:y+h+20, x:x+w+20]
                        confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
                        class_ids.append(class_id) #name of the object tha was detected

            indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6) #Aqui se aplica el algoritmo Non-Maximum Suppression para eliminar las detecciones que no son necesarias


            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)): #Aqui se dibujan los rectangulos y las etiquetas de las detecciones que se hicieron en la imagen
                if i in indexes:
                    x,y,w,h = boxes[i]
                    self.label = str(classes[class_ids[i]])
                    print(self.label)
                    color = colors[class_ids[i]]
                    cv2.rectangle(self.imgDP,(x,y),(x+w,y+h),color,1)
                    cv2.putText(self.imgDP,self.label,(x,y+30),font,1,(255,255,255),2)
                    self.imgDP = cv2.resize(self.imgDP, (320,240))
        except Exception as e:
            self.logReport.logger.error("Error in DeepLearnig " + str(e))
        
    
    def getimgROI(self,x1,y1,x2,y2, scale):
        self.frame3 = cv2.resize(self.frameBinary, (320,240))
        self.frame = cv2.resize(self.frame, (320,240))
        self.imgROI = self.frame3[y1:y2, x1:x2]
        self.imgROIColor = self.frame[y1:y2, x1:x2]
        #cv2.imshow('imgROI: ', self.imgROI)
        
    def areaC(self, cnt):
            # Encuentra el círculo mínimo que encierra el contorno
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            # Calcula el área del círculo
            area = np.pi * (radius ** 2)
            return area

    def imgCont(self):
        try:
            mgRoi = cv2.resize(self.imgROI, (320, 240))  # Asegúrate de que esta es la imagen binaria necesaria para encontrar contornos
            self.contours, self.hie = cv2.findContours(mgRoi, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            self.imgBinRsize = cv2.resize(self.imgROIColor, (320, 240))  # Asegúrate de que esta es la imagen a color escalada correctamente
            self.imgContours = self.imgBinRsize.copy()  # Crear una copia de la imagen a color para dibujar los contornos

            if self.contours:
                for idx, (cnt, hier) in enumerate(zip(self.contours, self.hie[0])):
                    if hier[3] != -1 and hier[2] == -1:  # Filtra solo contornos internos
                        area = cv2.contourArea(cnt)
                        if area > 100:
                            # Dibujar solo contornos internos directamente sobre la imagen a color
                            cv2.drawContours(self.imgContours, [cnt], -1, (255, 0, 0), 2)
                            self.areaCirc = self.areaC(cnt)

        except Exception as e:
            self.logReport.logger.error("Error in imgCont: " + str(e))


        
            


            