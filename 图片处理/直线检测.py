# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np


os.chdir(os.path.dirname(__file__))

 
#img = cv2.imread('contour.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('contour.png', dtype=np.uint8), 1)

#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊
#gray=cv2.GaussianBlur(gray, (3, 3), 0)  

#提取轮廓
gray=cv2.Canny(gray,100,300)


#再把图片转换为二值图
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

# 参数1：要检测的二值图（一般是阈值分割或边缘检测后的图）
# 参数2：距离r的精度，值越大，考虑越多的线，最大值为图像的对角线
# 参数3：角度θ的精度，值越小，考虑越多的线
# 参数4：累加数阈值，值越小，考虑越多的线，检测到大于几个点共线则判断为一条直线
# minLineLength：最短长度阈值，比这个长度短的线会被排除
# maxLineGap：最大直线间隙
lines=cv2.HoughLinesP(binary, 1, np.pi / 180, 40 , minLineLength=2, maxLineGap=10)
print(type(lines),lines)


if lines is not None:
    #将检测的线画出来（注意是极坐标噢）
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1, lineType=cv2.LINE_AA)
        '''第一个参数是指明在哪幅图像上绘制圆形；
        第二个参数是直线起点坐标。
        第三个参数指直线终点坐标。
        第四个参数表示颜色
        第五个参数表示轮廓线的宽度'''





cv2.imshow("largest shape", img)

cv2.waitKey(0)  
