# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np


#创建全黑图像
img=np.zeros((90, 55), dtype=np.uint8)
#反色
binary = cv2.bitwise_not(img)
cv2.imshow("img", img)
#cv2.imwrite("img.jpg", img)
