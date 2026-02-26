# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np


os.chdir(os.path.dirname(__file__))

 
img = cv2.imread('contour.PNG')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('contour.PNG', dtype=np.uint8), 1)

#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊
gray=cv2.GaussianBlur(gray, (3, 3), 0)  


#gray=cv2.Canny(gray,100,300)

param1=150
# 添加调试代码，观察边缘检测效果
edges = cv2.Canny(gray, param1, param1/2)  # Canny通常用高阈值:低阈值=2:1
cv2.imshow("Edges", edges)
cv2.waitKey(0)

#返回np数组,数组元素为圆心坐标和半径
#dp 识别精度，1.0表示按原图精度
#minDist为两个圆的圆心最小距离
#param1为边缘检测时使用Canny算子的高阈值
#param2：累加器阈值，就是圆的得分
circles=cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,dp=1.5,minDist=10,param1=7,param2=20,minRadius=10,maxRadius=25)

print(type(circles),circles)

if circles is not None:
    # 将坐标转换为整数，因为cv2.circle需要整数坐标
    circles = np.round(circles[0]).astype(int)
    for p in circles:
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
