import random
import main as M
import cv2
import numpy as np
import threading





class Image_Mode:


    def img_canny(self, img):



        edges = cv2.Canny(img, 50,150)



        return (edges, 'luminance')

    def img_thresh(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 128,255,cv2.THRESH_BINARY)

        return (thresh, 'luminance')


    def comic(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.blur(gray, (5,5))

        th2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17,6)

        img_th2 = cv2.bitwise_and(img, img, mask=th2)

        contrast = cv2.bitwise_and(img_th2, img_th2, mask=th2)

        final = cv2.bitwise_and(contrast, contrast, mask=th2)



        return (final, 'bgr')


    def comic_uncolored(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.blur(gray, (3, 3))

        th2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 6)

        return (th2,'luminance')


    def blue_light(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.blur(gray, (3, 3))

        th2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 6)

        plus = cv2.bitwise_not(img, img, mask=th2)

        com = cv2.bitwise_and(plus, plus, mask=th2)



        return (com, 'bgr')

class Cam_Mode:


    def frame_thresh(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 128,255,cv2.THRESH_BINARY)

        return (thresh, 'luminance')

    def comic_uncolored_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.blur(gray, (3, 3))

        th2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 6)

        return (th2,'luminance')

    def blue_light_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.blur(gray, (3, 3))

        th2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 6)

        plus = cv2.bitwise_not(frame, frame, mask=th2)

        com = cv2.bitwise_and(plus, plus, mask=th2)

        return (com, 'bgr')

    def canny(self, frame):


        edges = cv2.Canny(frame, 0 , 20)

        video = cv2.bitwise_or(frame,frame, mask=edges)



        return (video, 'bgr')

    def kernel(self, frame):

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            close = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel1)
            div = np.float32(gray) / (close)
            res = np.uint8(cv2.normalize(div, div, 0, 255, cv2.NORM_MINMAX))

            return (res, 'luminance')
        except:
            return (None, 'luminance')


    def kernal_light(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rey, tresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

        kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        close = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel1)
        div = np.float32(tresh) / (close)
        res = np.uint8(cv2.normalize(div, div, 0, 255, cv2.NORM_MINMAX))

        return (res, 'luminance')

    def replicate(self, frame):

        video = cv2.copyMakeBorder(frame, 350,350,350,350, cv2.BORDER_REPLICATE)

        return (video, 'bgr')

    def reflect(self, frame):

        video = cv2.copyMakeBorder(frame, 350,350,350,350, cv2.BORDER_REFLECT)

        return (video, 'bgr')

    def reflect101(self, frame):
        video = cv2.copyMakeBorder(frame, 350, 350, 350, 350, cv2.BORDER_REFLECT_101)

        return (video, 'bgr')

    def wrap(self, frame):

        video = cv2.copyMakeBorder(frame,350,350,350,350,cv2.BORDER_WRAP)

        return (video, 'bgr')
    def constant(self, frame):
        A = random.randint(0,255)
        B = random.randint(0,255)
        C = random.randint(0,255)
        video = cv2.copyMakeBorder(frame,350,350,350,350,cv2.BORDER_CONSTANT,value=(A,B,C))
        return (video, 'bgr')


