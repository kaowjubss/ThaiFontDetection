from keras.models import load_model
import cv2
import numpy as np
import sys, os


class ImagePrediction():
    def __init__(self):
        self.alphabet_model = load_model(os.path.dirname(os.path.abspath(sys.argv[0])) + '/main_model.h5')

    def predict(self,image):
        self.image = image
        self.rois, self.roi_position,self.rois_img= self.get_regions_of_interest(self.image)
        self.rois_pnd, self.roi_position_pnd,self.rois_img_pnd = self.get_regions_of_interest_pnd(self.image)
        self.predict_imgs = self.preprocessing(self.rois)
        self.predict_imgs_pnd = self.preprocessing_pnd(self.rois_pnd)
        # self.predicted_alphabets,self.alphabets_confidence,self.alphabets_img = self.predict_alphabet(self.rois_img_pnd,self.roi_position,self.predict_imgs_pnd,self.alphabet_model)
        self.predicted_alphabets,self.alphabets_confidence,self.alphabets_img = self.predict_alphabet(self.rois_img,self.roi_position,self.predict_imgs,self.alphabet_model)
        self.predicted_fonts,self.fonts_confidence = self.predict_font(self.predict_imgs,self.predicted_alphabets)
        self.font_result,self.result_confidence = self.get_font_result(self.predicted_fonts)
    
    @staticmethod
    def get_font_result(predicted_fonts):
        counter = 0
        result = predicted_fonts[0]
        for i in predicted_fonts:
            curr_frequency = predicted_fonts.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                result = i
        result_confidence = predicted_fonts.count(result)/len(predicted_fonts)
    
        return result,result_confidence

    @staticmethod
    def get_regions_of_interest_pnd(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # blur
        # blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # threshold
        thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # find contours
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        im2 = img.copy()
        rois=[]
        rois_position = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # draw a rectangle to visualize the bounding rect
            cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # crop character
            roi = img[y:y + h, x:x + w]
            # show cropped image
            # display at middle of screen
            # move window to (20,20)

            rois.append(roi)
            rois_position.append((x,y,w,h))

        return rois,rois_position,im2

    @staticmethod
    def cropfit_pnd(img):
        # find the bounding box of the image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #find the first row, first col, last row, last col of white pixels
        x, y, w, h = cv2.boundingRect(tr)
        #crop the image
        img = img[y:y+h, x:x+w]
        return img
    @staticmethod
    def croped2square_pnd(roi,increase_ratio=1.2):
        h, w,c = roi.shape
        r=int(max(h,w)*increase_ratio)
        square = np.zeros((r,r,c), dtype=np.uint8)
        # background.fill(255)  # or img[:] = 255
        # place the image in the center of the background
        offset_x = int((square.shape[1] - w) / 2)
        offset_y = int((square.shape[0] - h) / 2)
        square[offset_y:offset_y+h, offset_x:offset_x+w] = roi
        square = cv2.resize(square, (100,100))
        return square
    
    def preprocessing_pnd(self,rois):
        predict_imgs=[]
        for roi in rois:
            img=self.croped2square_pnd(self.cropfit_pnd(roi))

            img=img.reshape(1,100,100,3)
            predict_imgs.append(img)
        return predict_imgs   
            

    @staticmethod
    def croped2square(roi,increase_ratio=1.2):
        h, w = roi.shape
        r=int(max(h,w)*increase_ratio)
        square = np.zeros((r,r), dtype=np.uint8)
        # background.fill(255)  # or img[:] = 255
        # place the image in the center of the background
        offset_x = int((square.shape[1] - w) / 2)
        offset_y = int((square.shape[0] - h) / 2)
        square[offset_y:offset_y+h, offset_x:offset_x+w] = roi
        square = cv2.resize(square, (100,100))
        return square

    @staticmethod
    def cropfit(img):
        # find the bounding box of the image
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #find the first row, first col, last row, last col of white pixels
        x, y, w, h = cv2.boundingRect(img)
        #crop the image
        img = img[y:y+h, x:x+w]
        return img

    def preprocessing(self,rois):
        predict_imgs=[]
        for roi in rois:
            img=self.croped2square(self.cropfit(roi))
            img=img.reshape(1,100,100,1)
            predict_imgs.append(img)
        return predict_imgs   

    @staticmethod
    def get_regions_of_interest(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # blur
        # blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # threshold
        thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # find contours
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        im2 = img.copy()
        rois=[]
        rois_position = []
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
            rois_position.append((x,y,w,h))

        return rois, rois_position ,im2
    
    @staticmethod
    def predict_alphabet(image,rois_position,predict_imgs, model):
        predicted_classes=[]
        predictions=[]
        num2alpha = ['uni0E01', 'uni0E02', 'uni0E03', 'uni0E04', 
                        'uni0E05', 'uni0E06', 'uni0E07', 'uni0E08', 
                        'uni0E09', 'uni0E0A', 'uni0E0B', 'uni0E0C', 
                        'uni0E0D', 'uni0E0E', 'uni0E0F', 'uni0E10', 
                        'uni0E11', 'uni0E12', 'uni0E13', 'uni0E14', 
                        'uni0E15', 'uni0E16', 'uni0E17', 'uni0E18', 
                        'uni0E19', 'uni0E1A', 'uni0E1B', 'uni0E1C', 
                        'uni0E1D', 'uni0E1E', 'uni0E1F', 'uni0E20', 
                        'uni0E21', 'uni0E22', 'uni0E23', 'uni0E24', 
                        'uni0E25', 'uni0E26', 'uni0E27', 'uni0E28', 
                        'uni0E29', 'uni0E2A', 'uni0E2B', 'uni0E2C', 
                        'uni0E2D', 'uni0E2E', 'uni0E2F', 'uni0E30', 
                        'uni0E31', 'uni0E32', 'uni0E33', 'uni0E34', 
                        'uni0E35', 'uni0E36', 'uni0E37', 'uni0E38', 
                        'uni0E39', 'uni0E3A', 'uni0E3F', 'uni0E40', 
                        'uni0E41', 'uni0E42', 'uni0E43', 'uni0E44', 
                        'uni0E45', 'uni0E46', 'uni0E47', 'uni0E48', 
                        'uni0E49', 'uni0E4A', 'uni0E4B', 'uni0E4C', 
                        'uni0E4D', 'uni0E4E']
        for c,predict_img in enumerate(predict_imgs):
            # predict
            prediction=model.predict(predict_img)
            img= cv2.putText(image, num2alpha[c], (rois_position[c][0], rois_position[c][1]),cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 0, 255))
            predicted_classes.append(num2alpha[np.argmax(prediction, axis=-1)[0]])
            predictions.append(np.amax(prediction))
        return predicted_classes, predictions ,img
    @staticmethod
    def predict_font(predict_imgs, predicted_alphabets):
        num2font=['AngsanaNew', 'Chonburi', 'iannnnn-DUCK', 'MN KHAIPHALO',
                'pluempluem', 'pphometowntest', 'THBaijam', 'THCharmofAU',
                'THFahkwang', 'THKodchasal', 'THKoHo', 'THKrub', 'THMaliGrade6',
                'THSarabunNew']
        predicted_fonts=[]
        predictions=[]
        for c,predict_img in enumerate(predict_imgs):
            model= load_model(r'D:\University_Work\y2\sem2\AI\code\Project\model\{}.h5'.format(predicted_alphabets[c])) 
                                #(os.path.dirname(os.path.abspath(sys.argv[0])) + '???')
            prediction=model.predict(predict_img)
            predicted_fonts.append(num2font[np.argmax(prediction, axis=-1)[0]])
            predictions.append(prediction)
        return predicted_fonts, predictions
        
        

