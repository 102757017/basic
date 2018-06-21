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

#给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊
#gray=cv2.GaussianBlur(gray, (3, 3), 0)  


#gray=cv2.Canny(gray,100,300)

#把图片转换为二值图
#采用全局性阈值，第二个参数为分界值，灰度大于该值时将该像素灰度赋值为第三个参数。
ret, binary = cv2.threshold(gray,113,255,cv2.THRESH_BINARY)  
cv2.imshow("1", binary)


#黑白二值反转
ret, binary = cv2.threshold(gray,120,255,cv2.THRESH_BINARY_INV)  
cv2.imshow("2", binary)


#自适应阈值
binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,7,3)  
cv2.imshow("3", binary)
