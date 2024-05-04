import cv2
import numpy as np
from glob import glob
import joblib



mlp = joblib.load('modelMLP.joblib') # Carga del modelo. 
skl = joblib.load('modelScaler.joblib') # Carga del modelo.
print("Modelo cargado...", mlp)
pathNum = 'Test/'
imgPath = glob(pathNum +'*.jpg')
print("imgPath: ", imgPath)
for iP in imgPath:



    imgColor = cv2.imread(iP,1)
    img = cv2.imread(iP,0)

    ret, imgBin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

    # Encontrar y almacenar contornos
    contours,hierarchy = cv2.findContours(imgBin.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        a = cv2.contourArea(cnt)            
        if(a>100):
            cv2.rectangle(imgColor, (x,y),(x+w, y+h), (255,0,0), 2)
            cv2.imshow("imgColor",imgBin)
            imgRoi = imgBin[y:y+h, x:x+w]
            imgRoiResize = cv2.resize(imgRoi, (40, 60))
            vectorCaract = imgRoiResize.flatten()
                        
            # area = cv2.contourArea(cnt)
            # p = cv2.arcLength(cnt, True)
            # M = cv2.moments(cnt)
            # Hu = cv2.HuMoments(M)
            # extent = float(area) / (w * h)
            # zeros = cv2.countNonZero(imgRoi)
            # vectorCaract = np.array([area,p,w/h,w,h,Hu[0][0], Hu[1][0], Hu[2][0], Hu[3][0], extent,zeros], dtype = np.float32)
            vectorReshape = vectorCaract.reshape(1, -1)
            vectorSKL = skl.transform(vectorReshape)
            result = mlp.predict(vectorSKL)
            print("result: ", result)
            if(result == 0):
                print("Letra: A")
            elif(result == 1):
                print("Letra: B")
            elif(result == 2):
                print("Letra: C")
            elif(result == 3):
                print("Letra: D")
            elif(result == 4):
                print("Letra: E")
            elif(result == 5):
                print("Letra: F")
            elif(result == 6):
                print("Letra: G")
            elif(result == 7):
                print("Letra: H")
            elif(result == 8):
                print("Letra: I")
            elif(result == 9):
                print("Letra: J")
            elif(result == 10):
                print("Letra: K")
            elif(result == 11):
                print("Letra: L")
            elif(result == 12):
                print("Letra: M")
            elif(result == 13):
                print("Letra: N")
            elif(result == 14):
                print("Letra: O")
            elif(result == 15):
                print("Letra: P")
            elif(result == 16):
                print("Letra: Q")
            elif(result == 17):
                print("Letra: R")
            elif(result == 18):
                print("Letra: S")
            elif(result == 19):
                print("Letra: T")
            elif(result == 20):
                print("Letra: U")
            elif(result == 21):
                print("Letra: V")
            elif(result == 22):
                print("Letra: W")
            elif(result == 23):
                print("Letra: X")
            elif(result == 24):
                print("Letra: Y")
            elif(result == 25):
                print("Letra: Z")
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()   
    print("Fin...")             


            
#cv2.imshow("imgBin",imgBin)
#cv2.waitKey(0)