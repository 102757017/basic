# -*- coding: UTF-8 -*-
from PIL import Image
import sys
import cv2
import numpy as np
import os
from find_obj import filter_matches,explore_match
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(__file__))


#cv2.IMREAD_COLOR表示以彩色模式读入图片
img1 = cv2.imread('test.png', cv2.IMREAD_COLOR)
img2 = cv2.imread('sift_keypoints.jpg', cv2.IMREAD_COLOR)
#颜色转换函数，BGR->Gray 就可以设置为 cv2.COLOR_BGR2GRAY
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


#SIFT
sift= cv2.xfeatures2d.SIFT_create()
#keypoints返回关键点
keypoints1 = sift.detect(gray1, None)
keypoints2 = sift.detect(gray2, None)

#kp是关键点的列表，des是形状数组
kp1,des1 = sift.compute(gray1,keypoints1)

kp2,des2 = sift.compute(gray2,keypoints2)

bf = cv2.BFMatcher()
#返回k个最佳匹配  
matches = bf.knnMatch(des1, des2, k=2)
#p1, p2, kp_pairs = filter_matches(kp1, kp2, matches)
#explore_match('find_obj', img1, img2, kp_pairs)

matchesMask = [[0,0] for i in range(len(matches))]
draw_params = dict(matchColor = (0,255,0), singlePointColor = (255,0,0), matchesMask = matchesMask, flags = 0)
img3= cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)


plt.imshow(img3,)
plt.show()




#键盘绑定函数，共一个参数，表示等待毫秒数，将等待特定的几毫秒，
#看键盘是否有输入，返回值为ASCII值。如果其参数为0，则表示无限期的等待键盘输入。
cv2.waitKey(0)
cv2.destroyAllWindows()
