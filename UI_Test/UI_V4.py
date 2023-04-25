from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import sys

import numpy as np
import cv2

# If no image is chosen when browse
# If choose new image

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setGeometry(500,540,500,500)                   # (x, y, w, h)
        self.setWindowTitle('Font Detection')
        self.initUI()

    def initUI(self):
        self.labelTitle = QtWidgets.QLabel(self)
        self.labelTitle.setText('Choose an image to detect your fonts')
        self.labelTitle.move(100,100)

        self.labelImage = QtWidgets.QLabel(self)
        self.labelImage.move(300,100)

        self.buttonA = QtWidgets.QPushButton(self)
        self.buttonA.setText('Browse')
        self.buttonA.move(100,200)
        self.buttonA.clicked.connect(self.browseImg)

        self.buttonB = QtWidgets.QPushButton(self)
        self.buttonB.setText('Check')
        self.buttonB.move(100,300)
        self.buttonB.clicked.connect(self.checkImg)

    def browseImg(self):
        # Browse folder for image
        filename = QFileDialog.getOpenFileName(self, 'Open File', ' ','All Files (*);;PNG Files (*.png);;Jpg Files (*.jpg)')
        print(filename)
        image = filename[0]
        # img = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)

        cropImage = self.getImgCorner(image)  # Go to crop image
        height, width, ch = cropImage.shape
        bytesPerLine = 3 * width
        # Convert np array to QImage
        qImage = QImage(cropImage.data, width, height, bytesPerLine, QImage.Format_BGR888)

        # Open the image
        self.pixmap = QPixmap.fromImage(qImage)
        self.labelImage.setPixmap(self.pixmap) # Show image
        self.labelImage.adjustSize()
        # print(x)    # Print image loc in console

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
            cv2.imshow("Image", img)
            if clicked:
                cv2.circle(img, (x_pos[i], y_pos[i]), 5, (0, 0, 255), -1)
                clicked = False
                i+=1
            if cv2.waitKey(10) == 13:
                cv2.destroyAllWindows()
                break

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
        copium = cv2.getPerspectiveTransform(pts1,pts2)
        cropImage = cv2.warpPerspective(img, copium, (rows,cols), borderValue=(255,255,255))
        return cropImage

    def checkImg(self):
        print('placeholder')

    def update(self):               # Placehold in case of updating label, etc.
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = mainWindow()
    win.show()
    sys.exit(app.exec_())

window()