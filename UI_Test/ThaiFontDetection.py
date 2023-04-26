from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizeGrip
from PyQt5.QtGui import QPixmap, QImage
import sys

import numpy as np
import cv2

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(80, 10, 641, 71))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.header.setFont(font)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")

        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(30, 100, 241, 81))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.browseButton.setFont(font)
        self.browseButton.setObjectName("browseButton")

        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setGeometry(QtCore.QRect(30, 300, 241, 81))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.checkButton.setFont(font)
        self.checkButton.setObjectName("checkButton")

        self.switchButton = QtWidgets.QPushButton(self.centralwidget)
        self.switchButton.setGeometry(QtCore.QRect(30, 200, 241, 81))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.switchButton.setFont(font)
        self.switchButton.setObjectName("switchButton")

        self.picture = QtWidgets.QLabel(self.centralwidget)
        self.picture.setGeometry(QtCore.QRect(299, 99, 470, 280))
        self.picture.setMinimumSize(QtCore.QSize(470, 280))
        self.picture.setMaximumSize(QtCore.QSize(470, 280))
        self.picture.setText("")
        self.picture.setPixmap(QtGui.QPixmap("cat.jpg"))
        self.picture.setScaledContents(True)
        self.picture.setObjectName("picture")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 390, 641, 71))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 460, 641, 71))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.picture.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.header.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.adjustSize()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.browseButton.clicked.connect(self.browseImg)
        self.switchButton.clicked.connect(self.switchImg)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.header.setText(_translate("MainWindow", "Thai Font Detection"))
        self.browseButton.setStatusTip(_translate("MainWindow", "Browse Image"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.checkButton.setStatusTip(_translate("MainWindow", "Check the font and show confidence score"))
        self.checkButton.setText(_translate("MainWindow", "Check"))
        self.switchButton.setStatusTip(_translate("MainWindow", "Switch to showing bounding box"))
        self.switchButton.setText(_translate("MainWindow", "Switch"))
        self.label_2.setText(_translate("MainWindow", "Prediction : TestOne"))
        self.label_4.setText(_translate("MainWindow", "Confidence : 100%"))
    
    index = 0
    imgs = 0

    def switchImg(self):
        if self.index:
            self.index = 0
        else:
            self.index = 1
        
        self.showImg(self.imgs[self.index])


    def browseImg(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '','All Files (*);;PNG Files (*.png);;Jpg Files (*.jpg)')
        if filename[0]:
            image = filename[0]
            img = cv2.imread(image)
            cropImg = self.getImgCorner(img)
            self.imgs = [cropImg, self.showContour(cropImg)[0]]
            self.showImg(self.imgs[self.index])
        else:
            return
    
    def showImg(self,img):
        height, width, ch = img.shape
        bytesPerLine = 3 * width
        # Convert np array to QImage
        qImage = QImage(img.data, width, height, bytesPerLine, QImage.Format_BGR888)

        # Open the image
        self.pixmap = QPixmap.fromImage(qImage)
        self.picture.setPixmap(self.pixmap) # Show image
        self.picture.adjustSize()
    
    def getImgCorner(self,img):  # Cropping image
        # Initialize global variables
        clicked = False
        x_pos, y_pos = [-1,-1,-1,-1], [-1,-1,-1,-1]
        i = 0
        mark_img = img.copy()


        # Define the callback function
        def mouse_callback(event, x, y, flags, param):
            nonlocal clicked
            if event == cv2.EVENT_LBUTTONUP and i<4:
                x_pos[i], y_pos[i] = x, y
                clicked = True

        # Create a named window and register the mouse callbackction
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", mouse_callback)

        # Wait for a mouse click   
        while True:
            key = cv2.waitKey(1)
            cv2.imshow("Image", mark_img)
            if clicked:
                cv2.circle(mark_img, (x_pos[i], y_pos[i]), 5, (0, 0, 255), -1)
                if i>0:
                    cv2.line(mark_img, (x_pos[i-1], y_pos[i-1]), (x_pos[i], y_pos[i]), (0, 0, 255), 2)
                if i==3:
                    cv2.line(mark_img, (x_pos[i], y_pos[i]), (x_pos[0], y_pos[0]), (0, 0, 255), 2)
                clicked = False
                i+=1

            elif key == 27:
                cv2.destroyAllWindows()
                return img

            elif key == 13 and i==4:
                cv2.destroyAllWindows()
                break
                
            elif key == 8:
                clicked = False
                x_pos, y_pos = [-1,-1,-1,-1], [-1,-1,-1,-1]
                i = 0
                mark_img = img.copy()

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

        copium = cv2.getPerspectiveTransform(pts1,pts2)
        cropImage = cv2.warpPerspective(img, copium, (rows,cols), borderValue=(255,255,255))
        return cropImage

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



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
