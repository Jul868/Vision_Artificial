import cv2
import numpy as np
from glob import glob
import joblib


mlpNum = joblib.load('ModelNum.joblib') # Carga del modelo. 
sklNum = joblib.load('ScalerNum.joblib') # Carga del modelo.
# mlpLet = joblib.load('ModelLet.joblib') # Carga del modelo.
# sklLet = joblib.load('ScalerLet.joblib') # Carga del modelo.

print("Modelo cargado...", mlpNum)
pathNum = 'Placas/'
imgPath = glob(pathNum +'*.png')
print("imgPath: ", imgPath)

cadenaNum = []
cadenaLet = []
CadenaFull = []

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
                cv2.waitKey(0)
                cv2.destroyAllWindows()            
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
                    # vectorSKL = sklLet.transform(vectorReshape)
                    # result = mlpLet.predict(vectorSKL)
                    cadenaLet = np.append(cadenaLet, result)
                    print("result: ", result)
                    print("---------------------")
                    if len(cadenaLet) == 3:
                        #vamos a inverir el orden de la cadena
                        cadenaLet = cadenaLet[::-1]
                        print("Placa: ", cadenaLet)
                        

    print("Fin...")             
    print("Placa: ", cadenaLet, cadenaNum)

            
