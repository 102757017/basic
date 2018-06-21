# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np


os.chdir(os.path.dirname(__file__))

 
img = cv2.imread('part1.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('part1.png', dtype=np.uint8), 1)

#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊，目的是去除噪点
gray=cv2.GaussianBlur(gray, (3, 3), 0)  
cv2.imshow("gray1", gray)


#canny算法只接受二值图
a=50
gray=cv2.Canny(gray,a,a*3,3)


cv2.imshow("gray2", gray)


