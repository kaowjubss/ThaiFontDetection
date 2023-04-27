from ImagePrediction import ImagePrediction
import cv2
import numpy as np


prediction = ImagePrediction()
img = cv2.imread('C:/Users/kow16/Documents/GitHub/ThaiFontDetection/alphabet_test1.png')
prediction.predict(img)
#show image
cv2.imshow('image',prediction.alphabets_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(prediction.font_result)
print(prediction.result_confidence)