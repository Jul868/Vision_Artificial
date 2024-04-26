import csv
import cv2
import numpy as np
import os.path
import shutil

fileCSV = 'train.csv'
folder = 'imagesTrain\\'

folder_YOLO = 'imagesYOLO\\'
fileList = 'trainList.txt'
path = os.getcwd() + '\\'



def convert(size, box, label):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (label, x, y, w, h)

def readCSV():
    global ii
    with open(fileCSV) as File:
        reader = csv.reader(File)
        for row in reader:
            File = folder + row[0]
            #print (File)
            if row[0] != 'filename':
                if os.path.isfile(File):
                    img = cv2.imread(File)
                    H, W = img.shape[:2]

                    labeled = 0
                    if row[3] == 'a':
                        labeled = 0
                    elif row[3] == 'b':
                        labeled = 1
                    elif row[3] == 'd':
                        labeled = 2
                    elif row[3] == 'e':
                        labeled = 3
                    elif (row[3] == 'f'):
                        labeled = 4
                    elif row[3] == 'p':
                        labeled = 5                    
                    else:
                        labeled = 6
                       
                    box = (float(row[4]), float(row[6]), float(row[5]), float(row[7]))
                    bb = convert((W, H), box, labeled)
                    imgRoi = img[int(row[5]):int(row[7]),int(row[4]):int(row[6])]
                    
                    
                    #cv2.imshow("imgRoi",imgRoi)
                    #cv2.waitKey(0)
                                 
                    writeCSV(folder_YOLO + row[0], bb)

                    if not os.path.isfile(folder_YOLO + row[0]):
                        shutil.copy(File, folder_YOLO + row[0])
                        writeCSV(fileList, [path + folder_YOLO + row[0]])
                        
##                    cv2.rectangle(img, (int(row[4]), int(row[5])), (int(row[6]), int(row[7])), (255, 0, 0), 2)
##                    cv2.circle(img, (int(bb[1]*W), int(bb[2]*H)), 5, (0, 255, 0), -1)
##                    cv2.imshow("image", cv2.resize(img, (640, 480)))                  
                    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()
        
def writeCSV(fileTXT, data):
    fileTXT = fileTXT[:fileTXT.find('.')] + '.txt'
    #print(fileTXT)
    myFile = open(fileTXT, 'a', newline = '')
    with myFile:
        writer = csv.writer(myFile, delimiter=' ')
        writer.writerow(data)
    #print("Writing complete")

if not os.path.exists(folder_YOLO):
    os.mkdir(folder_YOLO)

readCSV()
print("FIN")
