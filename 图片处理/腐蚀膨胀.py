# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np


os.chdir(os.path.dirname(__file__))

 
img = cv2.imread('text.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('text.png', dtype=np.uint8), 1)

#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray",gray)


#再把图片转换为二值图
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  
cv2.imshow("threshold",binary)


#图片反色
thresh_img = cv2.bitwise_not(binary)
cv2.imshow("inverse",thresh_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

scale = 15
#img.shape返回的是图像的行数，列数，色彩通道数.
h_size = int(thresh_img.shape[1]/scale)



'''
构造形态学因子，形态学因子类似于笔刷，有不同的形状，并且有一个锚点
此处构造了一个10*1的矩阵，形态学因子是矩形，锚点未定义时取中心值
常用的形态学因子有如下几种：
椭圆（MORPH_ELLIPSE）
十字形结构（MORPH_CROSS）

'''
h_structure = cv2.getStructuringElement(cv2.MORPH_RECT,(10,1))
#腐蚀图像，相当于将笔刷沿轮廓内边缘绕行，返回笔刷锚点构成的封闭区
img1 = thresh_img.copy()
h_erode_img = cv2.erode(img1,h_structure,1)
cv2.imshow("erode",h_erode_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#膨胀图像，相当于将笔刷沿轮廓外边缘绕行，返回笔刷锚点构成的封闭区
img2 = thresh_img.copy()
h_dilate_img = cv2.dilate(img2,h_structure,1)
cv2.imshow("h_erode",h_dilate_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
