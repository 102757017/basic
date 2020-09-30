# -*- coding: UTF-8 -*-
from PIL import Image
import sys
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(__file__))


#cv2.IMREAD_COLOR表示以彩色模式读入图片
img1 = cv2.imread('捕获1.PNG', cv2.IMREAD_COLOR)
img1 = cv2.imdecode(np.fromfile('捕获1.PNG', dtype=np.uint8), 1)
img2 = cv2.imread('捕获2.PNG', cv2.IMREAD_COLOR)
img2 = cv2.imdecode(np.fromfile('捕获2.PNG', dtype=np.uint8), 1)
#颜色转换函数，BGR->Gray 就可以设置为 cv2.COLOR_BGR2GRAY
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


#SIFT
sift= cv2.SIFT_create()
#keypoints返回关键点
keypoints1 = sift.detect(gray1, None)
keypoints2 = sift.detect(gray2, None)


#kp是关键点的列表，des是形状数组
kp1,des1 = sift.compute(gray1,keypoints1)
kp2,des2 = sift.compute(gray2,keypoints2)
print("关键点kp1类型为",type(kp1))
print("形状数组des1类型为",type(des1))
print("关键点kp1数量为",len(kp1))
print('\n')
print("关键点kp2类型为",type(kp2))
print("形状数组des2类型为",type(des2))
print("关键点kp2数量为",len(kp2))
print('\n')

bf = cv2.BFMatcher()
#返回k个最佳匹配  
matches = bf.knnMatch(des1, des2, k=2)
print("matches类型为",type(matches))
print("matches数量为",len(matches))
print('\n')

print("基于第一张图的特征点构造匹配矩阵，初始化矩阵为0")
matchesMask = [[0,0] for i in range(len(matches))]
print("matchesMask类型为",type(matchesMask))
print("matchesMask数量为",len(matchesMask))
#print("matchesMask矩阵如下:",matchesMask)
print('\n')


#如果对一个列表，既要遍历索引又要遍历元素时可以使用enumerate()
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]
ppn=matchesMask.count([1,0])
rato=ppn/len(matchesMask)
print("匹配的特征点数量为",ppn,"，img1特征点的匹配比率为",rato)
#print("匹配后的matchesMask矩阵如下:",matchesMask)
print('\n')

draw_params = dict(matchColor = (0,255,0), singlePointColor = (255,0,0), matchesMask = matchesMask, flags = 0)
img3= cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)


plt.imshow(img3,)
plt.show()




#键盘绑定函数，共一个参数，表示等待毫秒数，将等待特定的几毫秒，
#看键盘是否有输入，返回值为ASCII值。如果其参数为0，则表示无限期的等待键盘输入。
cv2.waitKey(0)
cv2.destroyAllWindows()
