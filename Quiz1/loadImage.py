import reportLog
import cv2
import numpy as np


class LoadImage():
    def __init__(self, path= 'arm_1.png'):
        try:
            print(path)
            self.path = path
            self.imgColor = None
            self.imgGray = None
            self.imgBinaryIr = None
            self.imgBinaryIrColor = None
            self.imgROI = None
            self.logReport = reportLog.ReportLog()            
            self.logReport.logger.info("Init LoadImage process")
        except Exception as e:
            self.logReport.logger.error("Error Init LoadImage process " + str(e))

    def getColorImage(self):
        self.imgColor = cv2.imread(self.path, 1)
    
    def getGrayImage(self):
        self.imgGray = cv2.imread(self.path, 0)
    
    def getBinaryImageIR(self, u1, u2):
        if(self.imgGray.any() is not None):
            lower_bound = np.array([u1])
            upper_bound = np.array([u2])
            self.imgBinaryIr = cv2.inRange(self.imgGray, lower_bound, upper_bound)
            self.imgBinaryIrColor = cv2.cvtColor(self.imgBinaryIr, cv2.COLOR_GRAY2BGR)
    
    def drawROI(self,x1,y1,x2,y2, scale):
        frame3 = cv2.resize(self.imgColor, (300,300))
        imgROI = frame3[y1:y2, x1:x2]
        h, w = imgROI.shape[:2]
        self.imgROI = cv2.resize(imgROI, (w*scale,h*scale))
        cv2.imshow('imgROI: ', self.imgROI)