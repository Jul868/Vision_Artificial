import numpy as np
import cv2
import glob
import xlsxwriter

workbook = xlsxwriter.Workbook('dataFrutas.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 1

pathNumImages = 'Train/'
vectorNums = ['CebollaB', 'CebollaM', 'LimonB', 'LimonM', 'PapaB', 'PapaM', 'TomateB', 'TomateM']

for indice, num in  enumerate(vectorNums): #recorre el vector VectorNums y enumera devolviendo el indice y el valor
    pathNum =pathNumImages + num #concatena el pathNumImages con el valor de num para obtener la ruta de la carpeta de las imagenes
    pathImages = glob.glob(pathNum + '/*.jpg')
    for pathImg in pathImages:
        
        imgColor = cv2.imread(pathImg)
        imgGray = cv2.imread(pathImg, 0)
        frameHsv = cv2.cvtColor(imgColor, cv2.COLOR_BGR2HSV)
        imgBinary = cv2.inRange(frameHsv, (0, 0, 0), (225, 44, 255))
        imgBinary = cv2.bitwise_not(imgBinary)
        imgBinary = cv2.resize(imgBinary, (320, 210))
        cnts, hier = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(cnts) > 0:
            vectorCaract = []
            for cnt in cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                areaWH = w*h
                area = cv2.contourArea(cnt)
                p = cv2.arcLength(cnt, True)
                extent = float(area) / (w * h)
                M = cv2.moments(cnt)
                Hu = cv2.HuMoments(M)
                imgRoi = imgBinary[y:y+h, x:x+w]
                imgRoiResize = cv2.resize(imgRoi, (40, 60))
                zeros = cv2.countNonZero(imgRoi)
                if (areaWH > 1000):
                    vectorCaract = imgRoiResize.flatten()
                    
                    # vectorCaract.append(area)
                    # vectorCaract.append(p)
                    # vectorCaract.append(w/h)
                    # vectorCaract.append(w)  
                    # vectorCaract.append(h)
                    # vectorCaract.append(Hu[0][0])
                    # vectorCaract.append(Hu[1][0])
                    # vectorCaract.append(Hu[2][0])
                    # vectorCaract.append(Hu[3][0])
                    # vectorCaract.append(extent)
                    # vectorCaract.append(zeros)

                    for c in vectorCaract: #recorre el vector de caracteristicas y lo guarda en el archivo de excel fila por fila cada caracteristica (3 columnas por caracteristica)
                        worksheet.write(row, 0, indice)
                        worksheet.write(row, col, c)
                        col += 1
                    col = 1
                    row += 1
        cv2.imshow('imgGray', imgBinary)
        cv2.waitKey(1)
cv2.destroyAllWindows()
workbook.close()