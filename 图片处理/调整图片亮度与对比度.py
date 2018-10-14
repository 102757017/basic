# -*- coding: UTF-8 -*-
import cv2
import numpy as np
 
def contrast_demo(img1, c, b):  # 亮度就是每个像素所有通道都加上b
    rows, cols, chunnel = img1.shape
    blank = np.zeros([rows, cols, chunnel], img1.dtype)  # np.zeros(img1.shape, dtype=uint8)
    dst = cv2.addWeighted(img1, c, blank, 1-c, b)    
    return dst
 
img1 = cv2.imread("test.png", cv2.IMREAD_COLOR)
 
change=contrast_demo(img1, 1, -100)
cv2.imshow("con_bri_demo", change)

cv2.waitKey(0)
cv2.destroyAllWindows()

