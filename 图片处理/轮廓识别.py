# -*- coding: UTF-8 -*-
import cv2
import os

os.chdir(os.path.dirname(__file__))

 
img = cv2.imread('test.png')

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
第二个，返回我们要找的，轮廓的点集
第三个，各层轮廓的索引'''
binary,contours,hierarchy= cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  


'''第一个参数是指明在哪幅图像上绘制轮廓；
第二个参数是轮廓本身，在Python中是一个list。
第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓。
第四个参数表示颜色
第五个参数表示轮廓线的宽度，如果是-1，则为填充模式'''
cv2.drawContours(img,contours,-1,(0,0,255),2)  

  
cv2.imshow("img", img)  
cv2.waitKey(0)  
