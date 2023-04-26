from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QScrollArea, QWidget, QFormLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
import sys

import numpy as np
import cv2

# Fix crashing when choosing no image after browsing - Done
# Fix cropped image dimensions after choosing image second time - ???
# Incorporate contour into the UI

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setGeometry(500,540,500,500)                   # (x, y, w, h)
        self.setWindowTitle('Font Detection')
        self.initUI()

    def initUI(self):
        self.labelTitle = QtWidgets.QLabel(self)
        self.labelTitle.setText('Choose an image to crop the text \n you want to detect the font')
        self.labelTitle.adjustSize()
        self.labelTitle.move(50,100)

        self.labelImageA = QtWidgets.QLabel(self)
        self.labelImageA.move(300,100)

        self.labelImageB = QtWidgets.QLabel(self)
        self.labelImageB.move(300,100)

        self.buttonA = QtWidgets.QPushButton(self)
        self.buttonA.setText('Browse')
        self.buttonA.move(50,200)
        self.buttonA.clicked.connect(self.browseImg)

        self.buttonB = QtWidgets.QPushButton(self)
        self.buttonB.setText('Check')
        self.buttonB.move(50,250)
        self.buttonB.clicked.connect(self.checkImg)

        
    def browseImg(self):
        # Browse folder for image
        filename = QFileDialog.getOpenFileName(self, 'Open File', ' ','All Files (*);;PNG Files (*.png);;Jpg Files (*.jpg)')

        if filename[0] == '':
            pass

        else:
            print(filename)
            image = filename[0]
            # img = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)

            cropImage = self.getImgCorner(image)  # Go to crop image
            height, width, ch = cropImage.shape
            bytesPerLine = 3 * width
            qImage1 = QImage(cropImage.data, width, height, bytesPerLine, QImage.Format_BGR888) # Convert np array to QImage
            self.pixmap = QPixmap.fromImage(qImage1) # Open the image
            self.labelImageA.setPixmap(self.pixmap) # Show image
            self.labelImageA.setGeometry(QtCore.QRect(0, 0, 320, 180))
            self.labelImageA.move(300,100)
            self.labelImageA.setScaledContents(True)
            #self.labelImageA.adjustSize()

        # Show contour image
            cntImage, rois = self.showContour(cropImage)
            height, width, ch = cntImage.shape
            bytesPerLine = 3 * width
            qImage2 = QImage(cntImage.data, width, height, bytesPerLine, QImage.Format_BGR888)
            self.pixmap = QPixmap.fromImage(qImage2)
            self.labelImageB.setPixmap(self.pixmap) # Show image
            self.labelImageB.setGeometry(QtCore.QRect(0, 0, 320, 180))
            self.labelImageB.move(350+width,100)
            self.labelImageB.setScaledContents(True)
            #self.labelImageB.adjustSize()
            
    def getImgCorner(self,image):  # Cropping image
        # Initialize global variables
        clicked = False
        x_pos, y_pos = [-1,-1,-1,-1], [-1,-1,-1,-1]
        i = 0
        img = cv2.imread(image)
        # Define the callback function
        def mouse_callback(event, x, y, flags, param):
            nonlocal clicked
            if event == cv2.EVENT_LBUTTONUP:
                x_pos[i], y_pos[i] = x, y
                clicked = True

        # Create a named window and register the mouse callbackction
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", mouse_callback)

        # Wait for a mouse click   
        while True:
            key = cv2.waitKey(10)
            cv2.imshow("Image", img)
            if clicked and i<4:
                cv2.circle(img, (x_pos[i], y_pos[i]), 5, (0, 0, 255), -1)
                if i > 0:
                    cv2.line(img, (x_pos[i-1], y_pos[i-1]), (x_pos[i], y_pos[i]), (0, 0, 255), 2)
                if i == 3:
                    cv2.line(img, (x_pos[i], y_pos[i]), (x_pos[0], y_pos[0]), (0, 0, 255), 2)
                clicked = False
                i+=1

            elif key == 27:  # Escape
                cv2.destroyAllWindows()
                return img

            elif key == 13 and i == 4: 
                cv2.destroyAllWindows()
                break

            elif clicked and i == 4:
                print('No')

            elif key == 8:
                clicked = False
                x_pos, y_pos = [-1,-1,-1,-1], [-1,-1,-1,-1]
                i = 0
                mark_img = img.copy()

        print(x_pos, y_pos)
        c_pos = []
        for a in range(i):
            c_pos.append([x_pos[a],y_pos[a]])

        c_pos = sorted(c_pos, key=lambda p: p[0] + p[1])

        if c_pos[1][1] > c_pos[2][1]:
            temp = c_pos[2]
            c_pos[2] = c_pos[1]
            c_pos[1] = temp

        rows = c_pos[3][0]-c_pos[0][0]
        cols = c_pos[3][1]-c_pos[0][1]

        
        pts1 = np.float32(c_pos)
        pts2 = np.float32([[0,0],[rows,0],[0,cols],[rows,cols]])

        img = cv2.imread(image)
        cropium = cv2.getPerspectiveTransform(pts1,pts2)
        cropImage = cv2.warpPerspective(img, cropium, (rows,cols), borderValue=(255,255,255))
        return cropImage

    def checkImg(self):
        print('placeholder')

    def update(self):               # Placehold in case of updating label, etc.
        self.label.adjustSize()
    
    def showContour(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Blur
        # blur = cv2.GaussianBlur(gray, (5,5), 0)
        # Threshold
        ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # ker = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        # thresh = cv2.erode(thresh, ker, iterations=1)
        # Find contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        im2 = img.copy()

        rois=[]
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # draw a rectangle to visualize the bounding rect
            cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # crop character
            roi = thresh[y:y + h, x:x + w]
            # show cropped image
            # display at middle of screen
            # move window to (20,20)

            rois.append(roi)
        return im2, rois

def window():
    app = QApplication(sys.argv)
    win = mainWindow()
    win.show()
    sys.exit(app.exec_())

window()