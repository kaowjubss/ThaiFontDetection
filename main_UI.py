from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSizeGrip
from PyQt5.QtGui import QPixmap, QImage
import sys
from ImagePrediction import ImagePrediction

import numpy as np
import cv2

class UI_MainWindow(QMainWindow):
    def setupUI(self, MainWindow):
        self.prediction = ImagePrediction()
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

        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(151, 200, 120, 81))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.nextButton.setFont(font)
        self.nextButton.setObjectName("nextButton")

        self.prevButton = QtWidgets.QPushButton(self.centralwidget)
        self.prevButton.setGeometry(QtCore.QRect(30, 200, 120, 81))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.prevButton.setFont(font)
        self.prevButton.setObjectName("prevButton")

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
        self.nextButton.clicked.connect(self.nextImg)
        self.prevButton.clicked.connect(self.prevImg)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.header.setText(_translate("MainWindow", "Thai Font Detection"))
        self.browseButton.setStatusTip(_translate("MainWindow", "Browse Image"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.checkButton.setStatusTip(_translate("MainWindow", "Check the font and show confidence score"))
        self.checkButton.setText(_translate("MainWindow", "Check"))
        self.prevButton.setStatusTip(_translate("MainWindow", "Previous Image"))
        self.prevButton.setText(_translate("MainWindow", "Prev"))
        self.nextButton.setStatusTip(_translate("MainWindow", "Next Image"))
        self.nextButton.setText(_translate("MainWindow", "Next"))
        self.label_2.setText(_translate("MainWindow", "Prediction : TestOne"))
        self.label_4.setText(_translate("MainWindow", "Confidence : 100%"))
    
    index = 0
    imgs = 0

    def nextImg(self):
        if not self.imgs:
            return
        self.index += 1
        if self.index >= len(self.imgs):
            self.index = 0
        self.showImg(self.imgs[self.index])
        self.update_text()
    
    def prevImg(self):
        if not self.imgs:
            return
        _translate = QtCore.QCoreApplication.translate
        self.index -= 1
        if self.index < 0:
            self.index = len(self.imgs) - 1
        self.showImg(self.imgs[self.index])
        self.update_text()

    def update_text(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("MainWindow", "Prediction : {}:{}".format(chr(int(self.prediction.predicted_alphabets[0][3:],16)),self.prediction.font_result)))
        self.label_4.setText(_translate("MainWindow", "Confidence : {}:{}".format(self.prediction.alphabets_confidence,self.prediction.result_confidence)))
    
    def browseImg(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '','All Files (*);;PNG Files (*.png);;Jpg Files (*.jpg)')
        if filename[0]:
            image = filename[0]
            # img = cv2.imread(image)
            # cropImg = self.getImgCorner(img)
            cropImg = cv2.imread(image) # for testing
            self.imgs = [cropImg]
            self.showImg(self.imgs[self.index])
            self.prediction.predict(cropImg)
            self.update_text()
            self.imgs.append(self.prediction.rois_img)
            for roi in self.prediction.rois:
                self.imgs.append(roi)
            
        else:
            return
    
    def showImg(self,img):
        print(img.shape)
        print(type(img))
        # cv2.imshow("test",img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if len(img.shape) == 2: # If image is grayscale
            height, width = img.shape
            bytesPerLine = width
            # Convert np array to QImage
            qImage = QImage(np.array(img).data, width, height, bytesPerLine , QImage.Format_Grayscale8)
        else: # If image is color
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





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
