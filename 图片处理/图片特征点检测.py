# -*- coding: UTF-8 -*-
from PIL import Image
import sys
import cv2
import numpy as np
import os

os.chdir(os.path.dirname(__file__))


#cv2.IMREAD_COLOR表示以彩色模式读入图片
img = cv2.imread('test.png', cv2.IMREAD_COLOR)
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('test.png', dtype=np.uint8), 1)
#颜色转换函数，BGR->Gray 就可以设置为 cv2.COLOR_BGR2GRAY
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('origin',img)


#SIFT
sift= cv2.xfeatures2d.SIFT_create()
#keypoints返回关键点
keypoints = sift.detect(gray, None)

#kp是关键点的列表，des是形状数组
kp,des = sift.compute(gray,keypoints)

cv2.drawKeypoints(gray, keypoints, img)
cv2.imshow('testSift', img)


img=cv2.drawKeypoints(gray,keypoints,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#cv2.imwrite('sift_keypoints.jpg',img)
#由于cv2.imwrite不支持保存图片到中文路径，用以下方法代替cv2.imwrite
cv2.imencode('.jpg', img)[1].tofile('sift_keypoints.jpg')


#键盘绑定函数，共一个参数，表示等待毫秒数，将等待特定的几毫秒，
#看键盘是否有输入，返回值为ASCII值。如果其参数为0，则表示无限期的等待键盘输入。
cv2.waitKey(0)
cv2.destroyAllWindows()
