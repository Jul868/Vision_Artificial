import cv2
import numpy as np
from glob import glob
import joblib



mlp = joblib.load('modelMLP2.joblib') # Carga del modelo. 
skl = joblib.load('modelScaler.joblib') # Carga del modelo.
print("Modelo cargado...", mlp)
pathNum = 'num/test/'
imgPath = glob(pathNum +'*.jpg')
print("imgPath: ", imgPath)
for iP in imgPath:



    imgColor = cv2.imread(iP,1)
    img = cv2.imread(iP,0)
    img = cv2.resize(img, (25,50))
    imgColor = cv2.resize(imgColor, (25,50))

    ret, imgBin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

    # Encontrar y almacenar contornos
    contours,hierarchy = cv2.findContours(imgBin.copy(), \
                                                cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        a = cv2.contourArea(cnt)            
        if(a>10):
            cv2.rectangle(imgColor, (x,y),(x+w, y+h), (255,0,0), 2)
            cv2.imshow("imgColor",imgColor)
            imgRoi = imgBin[y:y+h, x:x+w]
            imgRoiResize = cv2.resize(imgRoi, (40, 60))
            vectorCaract = imgRoiResize.flatten()
            cv2.waitKey(0)
            cv2.destroyAllWindows()            
            # area = cv2.contourArea(cnt)
            # p = cv2.arcLength(cnt, True)
            # M = cv2.moments(cnt)
            # Hu = cv2.HuMoments(M)
            # vectorCaract = np.array([area,p,w/h,w,h,Hu[0][0], Hu[1][0], Hu[2][0]], dtype = np.float32)
            vectorReshape = vectorCaract.reshape(1, -1)
            vectorSKL = skl.transform(vectorReshape)
            result = mlp.predict(vectorSKL)
            print("result: ", result)
            if(int(result[0]) == 0):
                print("el número es: ", 0)
            elif(int(result[0]) == 1): 
                print("el número es: ", 1)
            elif(int(result[0]) == 2):
                print("el número es: ", 2)
            elif(int(result[0]) == 3):
                print("el número es: ", 3)
            elif(int(result[0]) == 4):
                print("el número es: ", 4)
            elif(int(result[0]) == 5):
                print("el número es: ", 5)
            elif(int(result[0]) == 6):
                print("el número es: ", 6)
            elif(int(result[0]) == 7):
                print("el número es: ", 7)
            elif(int(result[0]) == 8):
                print("el número es: ", 8)
            elif(int(result[0]) == 9):
                print("el número es: ", 9)

    print("Fin...")             


            
#cv2.imshow("imgBin",imgBin)
#cv2.waitKey(0)