# -*- coding: UTF-8 -*-
import cv2
import numpy as np

def nothing(x):
    pass

# 创建一个黑色背景的窗口
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# 创建改变颜色的滚动条
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# 创建控制函数的开关
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # 获取四个滚动条的位置
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]#把滚动条里的颜色值赋给图片

cv2.destroyAllWindows()
