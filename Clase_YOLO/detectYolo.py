import cv2
import numpy as np
import glob

#Load YOLO
net = cv2.dnn.readNet("model.weights","model.cfg") #Aqui se carga el modelo preentrenado de YOLO con los pesos y la configuracion del modelo 
classes = []
with open("model.names","r") as f: #Aqui se cargan las clases que se pueden detectar con el modelo YOLO 
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames() #Aqui se obtienen los nombres de las capas del modelo YOLO
outputlayers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()] #Aqui se obtienen las capas de salida del modelo YOLO 

colors= np.random.uniform(0,255,size=(len(classes) + 1 ,3))
print(colors)

#loading image
pathImages = glob.glob("imagesTrain/*.jpg")

for pathImg in pathImages: #Aqui se recorren todas las imagenes que se encuentran en la carpeta imagesTrain
    print(pathImg)
    img = cv2.imread(pathImg)
    img = cv2.resize(img,None,fx=0.4,fy=0.3)
    height,width,channels = img.shape

    #detecting objects
    blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False) #Aqui se crea un blob de la imagen para poder pasarsela al modelo YOLO

    net.setInput(blob) #Aqui se le pasa la imagen al modelo YOLO
    outs = net.forward(outputlayers) #Aqui se obtienen las detecciones que se hicieron en la imagen

    #print(outs[1])


    #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
    class_ids=[]
    confidences=[]
    boxes=[]
    for out in outs: #Aqui se recorren todas las detecciones que se hicieron en la imagen
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                #print(confidence)
                #onject detected
                center_x= int(detection[0]*width)
                center_y= int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                #cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                #rectangle co-ordinaters
                x=int(center_x - w/2)
                y=int(center_y - h/2)
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                boxes.append([x,y,w,h]) #put all rectangle areas
                confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
                class_ids.append(class_id) #name of the object tha was detected

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6) #Aqui se aplica el algoritmo Non-Maximum Suppression para eliminar las detecciones que no son necesarias
    # print("Indexes", indexes)
    # print("class_ids", class_ids)


    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)): #Aqui se dibujan los rectangulos y las etiquetas de las detecciones que se hicieron en la imagen
        if i in indexes:
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img,(x,y),(x+w,y+h),color,1)
            cv2.putText(img,label,(x,y+30),font,1,(255,255,255),2)

    cv2.imshow("Image",cv2.resize( img, (1020, 920)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
