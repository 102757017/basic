# -*- coding: UTF-8 -*-
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np



def sobel(gray,size):
    #ksize是指核的大小,只能取奇数，影响边缘的粗细
    x = cv2.Sobel(gray,cv2.CV_16S,1,0,ksize=size)
    y = cv2.Sobel(gray,cv2.CV_16S,0,1,ksize=size)
    
    # 转回uint8
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)

    dst = cv2.addWeighted(absX,0.5,absY,0.5,0)
    return dst


os.chdir(os.path.dirname(__file__))

img = cv2.imdecode(np.fromfile('5.png', dtype=np.uint8), 1)
#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
dst=sobel(gray,3)
cv2.imshow("Result", dst)

