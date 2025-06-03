# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np


os.chdir(os.path.dirname(__file__))

 
img = cv2.imread('contour.png')
#要显示中文必须安装opencv-python-rolling（opencv的开发版）
cv2.putText(img, "中文", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

cv2.imshow('ADD Text', img)
# 等待按键事件无限时间，然后关闭所有窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
