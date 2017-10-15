# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np


os.chdir(os.path.dirname(__file__))

 
img = cv2.imread('contour.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('contour.png', dtype=np.uint8), 1)

#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊
#gray=cv2.GaussianBlur(gray, (3, 3), 0)  


#gray=cv2.Canny(gray,100,300)

#再把图片转换为二值图
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  


'''cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图），
所以读取的图像要先转成灰度的，再转成二值图
这个函数实际上返回了三个值
第一个，它返回了你所处理的图像
第二个，返回我们要找的轮廓集list，list元素为轮廓点集坐标构成的矩阵
第三个，各层轮廓的索引'''
binary,contours,hierarchy= cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
print(type(contours),len(contours))#共几个轮廓
print(type(contours[0]),len(contours[0]))#第一个轮廓的点集个数
print(contours[0])#第一个轮廓的坐标集
print(cv2.contourArea(contours[0]))#第一个轮廓的面积

'''第一个参数是指明在哪幅图像上绘制轮廓；
第二个参数是轮廓本身，在Python中是一个list。
第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓。
第四个参数表示颜色
第五个参数表示轮廓线的宽度，如果是-1，则为填充模式'''
cv2.drawContours(img,contours,-1,(0,0,255),2)  

cv2.imshow("img", img)

#cv2.contourArea计算轮廓面积,返回轮廓内像素点的个数，此处将轮廓集按面积排序
c = sorted(contours, key=cv2.contourArea, reverse=True)[0]
#cv2.minAreaRect主要求得包含点集最小面积的矩形，这个矩形是可以有偏转角度的，可以与图像的边界不平行。
rect = cv2.minAreaRect(c)
print(type(rect),rect)
box = np.int0(cv2.boxPoints(rect))
cv2.drawContours(img, [box], -1, (0, 255, 0), 3)
cv2.imshow("largest shape", img)

cv2.waitKey(0)  
