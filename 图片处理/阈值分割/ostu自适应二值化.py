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

ret2,binary = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("image", binary)


