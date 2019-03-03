# -*- coding: UTF-8 -*-
import numpy as np
from PIL import Image
import os
import cv2

os.chdir(os.path.dirname(__file__))
# 由于opencv不支持读取中文路径，用以下方法代替cv2.imread
frame = cv2.imdecode(np.fromfile('get-captcha.jpeg', dtype=np.uint8), 1)

 
# 把 BGR 转为 HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 

#opencv中，H（色度）范围[0,255],S(饱和度)范围[0,255]，V(亮度)范围[0,115]
lower_blue = np.array([0,0,0]) 
upper_blue = np.array([255,255,115]) 
 
# 获得区域的mask,返回二值图，寻找到的区域赋值255,其它区域赋值0
mask = cv2.inRange(hsv, lower_blue, upper_blue)
 
# 和原始图片进行and操作，获得指定区域的原始图
res = cv2.bitwise_and(frame,frame, mask= mask)
 
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.imshow('frame',frame)
cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
cv2.imshow('mask',mask)
cv2.namedWindow('res', cv2.WINDOW_NORMAL)
cv2.imshow('res',res)
