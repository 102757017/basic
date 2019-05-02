# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
import math
import time

os.chdir(os.path.dirname(__file__))

def sdfl(array,n):
    obj=np.zeros_like(array, dtype=np.uint8)
    for i in range(n):
        value=int(255/(n-1))*i
        low=255/n*i
        high=255/n*(i+1)
        area=np.where((array>low)&(array<high))
        obj[area]=value
    return obj

if __name__=="__main__":
    os.chdir(os.path.dirname(__file__))
    #由于opencv不支持读取中文路径，用以下方法代替cv2.imread
    img = cv2.imdecode(np.fromfile('get-captcha.png', dtype=np.uint8), 1)
    target = sdfl(img,2)
    cv2.imshow('image',target)
    cv2.imwrite('re_color.png',target)

