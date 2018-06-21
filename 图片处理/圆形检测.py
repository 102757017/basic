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

#返回np数组,数组元素为圆心坐标和半径
#dp 识别精度，1.0表示按原图精度
#minDist为两个圆的圆心最小距离
#param1为边缘检测时使用Canny算子的高阈值
circles=cv2.HoughCircles(binary,cv2.HOUGH_GRADIENT,dp=1.5,minDist=10,param1=7,param2=20,minRadius=10,maxRadius=25)
print(type(circles),circles)

if circles is not None:
    for p in circles[0]:
        x,y,radius=p
        center=(x,y)
        '''第一个参数是指明在哪幅图像上绘制圆形；
        第二个参数是绘制圆心的坐标。
        第三个参数指定半径
        第四个参数表示颜色
        第五个参数表示轮廓线的宽度，如果是-1，则为填充模式'''
        cv2.circle(img,center,radius,(200,0,0),2) 



cv2.imshow("largest shape", img)

cv2.waitKey(0)  
