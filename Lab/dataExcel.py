import numpy as np
import cv2
import glob
import xlsxwriter

workbook = xlsxwriter.Workbook('dataDientes.xlsx') # Se crea un archivo de excel 
worksheet = workbook.add_worksheet()

row = 0
col = 1

pathNumImages = "rotadas/"
vectorNums = ['cad', 'cai', 'cd', 'ci', 'ld', 'li']
vectorCount = [0, 0, 0, 0, 0, 0]

for indice, num in enumerate (vectorNums): # Recorro el vector y lo voy ennumeradno, es decir, extrae el índice de la posición 
    pathNum = pathNumImages + num # Entro a la carpeta Num y se extrae la carpeta 0, 1, 2...
    pathImages = glob.glob(pathNum + '/*.jpg') # glob: busca la ruta y un patrón -> saca la ruta y crea un vector de rutas
    for pathImg in pathImages: # se va por el vector y lee cada ruta de las imagenes
        imgColor = cv2.imread(pathImg)
        imgGray = cv2.imread(pathImg, 0)
        ret, imgBinary = cv2. threshold(imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        print(ret)
        cnts, hier = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if (len(cnts) > 0): # Se extraen caracteristicas si solo si hay contornos
            vectorCaract = []
            for cnt in cnts: # Recorro contornos
                x, y, w, h = cv2.boundingRect(cnt)
                areaHW = w*h
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                #maxrect = max(rect[1])/min(rect[1])
                area = cv2.contourArea(cnt) # Extraigo patrones
                p = cv2.arcLength(cnt, True) # Extraigo patrones
                m = cv2.moments(cnt) # Extraigo patrones
                hu = cv2.HuMoments(m) # Extraigo patrones
                #extent = area/(rect[1][0]*rect[1][1])
                aspecto = w/h
                excentricidad = np.sqrt(np.square(w) + np.square(h))/2
                #compacidad = (p**2)/(4*np.pi*area)
                imgRoi = imgBinary[y:y+h, x:x+w]
                imgRoiResize = cv2.resize(imgRoi, (40,60))
                
                if (areaHW > 1000):

                    vectorCaract = imgRoiResize.flatten()
                    # vectorCaract.append(area)
                    # vectorCaract.append(p)
                    # vectorCaract.append(w)
                    # vectorCaract.append(h)
                    # vectorCaract.append(hu[0])
                    # vectorCaract.append(hu[1])
                    # vectorCaract.append(hu[2])
                    # vectorCaract.append(hu[3])
                    # vectorCaract.append(aspecto)
                    # vectorCaract.append(excentricidad)  
                    

                    for c in vectorCaract: # Lo recorro y lo guardo en el excel 
                        worksheet.write(row, 0, indice) # En la columna 0 siempre me guardará la clase 
                        worksheet.write(row, col, c) # A partir de ahí, va guardando las características por filas y columnas 
                        col = col + 1
                    col = 1
                    row = row + 1

        
# cv2.imshow("img", imgBinary)
# cv2.waitKey(0)
cv2.destroyAllWindows()
workbook.close()

