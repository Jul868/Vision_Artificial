import cv2
import numpy as np
from glob import glob
import joblib


mlpNum = joblib.load('ModelNum2.joblib') # Carga del modelo. 
sklNum = joblib.load('ScalerNum.joblib') # Carga del modelo.
mlpLet = joblib.load('ModelLet.joblib') # Carga del modelo.
sklLet = joblib.load('ScalerLet.joblib') # Carga del modelo.

print("Modelo cargado...", mlpNum)
pathNum = 'Placas/'
imgPath = glob(pathNum +'*.png')
print("imgPath: ", imgPath)

cadenaNum = []
cadenaLet = []
CadenaFull = []
resultLet = ''

for iP in imgPath:
    cadenaNum = []
    cadenaLet = []
    imgColor = cv2.imread(iP,1)
    img = cv2.imread(iP,0)
    img = cv2.resize(img, (138,81))
    ret, imgBin = cv2.threshold(img, 0, 250, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) # otsu hace la binarización de la imagen automáticamente
    
    contours,hierarchy = cv2.findContours(imgBin.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    hh,ww = imgBin.shape[:2] # Se obtiene el tamaño de la imagen en pixeles (alto, ancho) (H = 81, W = 138)
    
    
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        a = cv2.contourArea(cnt)

        
        if(a>100):
            
            imgRoi = imgBin[y:y+h, x:x+w]
            imgRoiResize = cv2.resize(imgRoi, (40, 60))
            pixelWhite = cv2.countNonZero(imgRoi)
            if pixelWhite > 140 and pixelWhite < 600:
                cv2.rectangle(imgBin, (x,y),(x+w, y+h), (255,0,0), 2)
                cv2.imshow("imgColor",imgBin)
                #print('Area:', a)
                #print('Pixel White:', pixelWhite)
                #print('x:', x)


                vectorCaract = imgRoiResize.flatten()
            
                # area = cv2.contourArea(cnt)
                # p = cv2.arcLength(cnt, True)
                # M = cv2.moments(cnt)
                # Hu = cv2.HuMoments(M)
                # vectorCaract = np.array([area,p,w/h,w,h,Hu[0][0], Hu[1][0], Hu[2][0]], dtype = np.float32)
                if x > 50:
                    vectorReshape = vectorCaract.reshape(1, -1)
                    vectorSKL = sklNum.transform(vectorReshape)
                    result = mlpNum.predict(vectorSKL)
                    cadenaNum = np.append(cadenaNum, result)
                    print("result: ", result)
                    print("---------------------")
                    if len(cadenaNum) == 3:
                        #vamos a inverir el orden de la cadena
                        cadenaNum = cadenaNum[::-1]
                        print("Placa: ", cadenaNum)
                else:
                    vectorReshape = vectorCaract.reshape(1, -1)
                    vectorSKL = sklLet.transform(vectorReshape)
                    result = mlpLet.predict(vectorSKL)
                    # print("result: ", result)
                    print("---------------------")
                    if(result == 0):
                        resultLet = 'A'
                        print("result: ", resultLet)
                    elif(result == 1):
                        resultLet = 'B'
                        print("result: ", resultLet)
                    elif(result == 2):
                        resultLet = 'C'
                        print("result: ", resultLet)
                    elif(result == 3):
                        resultLet = 'D'
                        print("result: ", resultLet)
                    elif(result == 4):
                        resultLet = 'E'
                        print("result: ", resultLet)
                    elif(result == 5):
                        resultLet = 'F'
                        print("result: ", resultLet)
                    elif(result == 6):
                        resultLet = 'G'
                        print("result: ", resultLet)
                    elif(result == 7):
                        resultLet = 'H'
                        print("result: ", resultLet)
                    elif(result == 8):
                        resultLet = 'I'
                        print("result: ", resultLet)
                    elif(result == 9):
                        resultLet = 'J'
                        print("result: ", resultLet)
                    elif(result == 10):
                        resultLet = 'K'
                        print("result: ", resultLet)
                    elif(result == 11):
                        resultLet = 'L'
                        print("result: ", resultLet)
                    elif(result == 12):
                        resultLet = 'M'
                        print("result: ", resultLet)
                    elif(result == 13):
                        resultLet = 'N'
                        print("result: ", resultLet)
                    elif(result == 14):
                        resultLet = 'O'
                        print("result: ", resultLet)
                    elif(result == 15):
                        resultLet = 'P'
                        print("result: ", resultLet)
                    elif(result == 16):
                        resultLet = 'Q'
                        print("result: ", resultLet)
                    elif(result == 17):
                        resultLet = 'R'
                        print("result: ", resultLet)
                    elif(result == 18):
                        resultLet = 'S'
                        print("result: ", resultLet)
                    elif(result == 19):
                        resultLet = 'T'
                        print("result: ", resultLet)
                    elif(result == 20):
                        resultLet = 'U'
                        print("result: ", resultLet)
                    elif(result == 21):
                        resultLet = 'V'
                        print("result: ", resultLet)
                    elif(result == 22):
                        resultLet = 'W'
                        print("result: ", resultLet)
                    elif(result == 23):
                        resultLet = 'X'
                        print("result: ", resultLet)
                    elif(result == 24):
                        resultLet = 'Y'
                        print("result: ", resultLet)
                    elif(result == 25):
                        resultLet = 'Z'
                        print("result: ", resultLet)
                        
                    cadenaLet = np.append(cadenaLet, resultLet)
                    if len(cadenaLet) == 3:
                        #vamos a inverir el orden de la cadena
                        cadenaLet = cadenaLet[::-1]
                        print("Placa: ", cadenaLet)


    print("Fin...")             
    print("Placa: ", cadenaLet, cadenaNum)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
            
