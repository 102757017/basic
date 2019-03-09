# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
import scipy.ndimage as ndimg
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(__file__))

 
#img = cv2.imread('contour.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('p1.png', dtype=np.uint8), 1)

#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#再把图片转换为二值图
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

#填充孔洞，返回的bool值的矩阵
fill_holes=ndimg.binary_fill_holes(binary)
fill_holes=np.where(fill_holes==True,255,0)

#去除小的区域
remove_little,contours,hierarch=cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    #设定阈值
    if area < 20:
        cv2.drawContours(remove_little,[contours[i]],0,0,-1)



fig=plt.figure()

ax1=fig.add_subplot(131)
ax1.imshow(img)
ax1.set_title("origin")

ax2=fig.add_subplot(132)
ax2.imshow(fill_holes)
ax2.set_title("fill_holes")

ax3=fig.add_subplot(133)
ax3.imshow(remove_little)
ax3.set_title("remove_little")

plt.show()

