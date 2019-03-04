# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
import math
import time

os.chdir(os.path.dirname(__file__))

def sdfl(array,n):
    for i in range(n):
        value=int(255/(n-1))*i
        low=255/n*i
        high=255/n*(i+1)
        area=np.where((array>low)&(array<high))
        array[area]=value
    return array

#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('aaa.jpg', dtype=np.uint8), 1)




target = sdfl(img,2)
cv2.imshow('image',target)
cv2.imwrite('binary.png',target)


