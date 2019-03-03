# -*- coding: UTF-8 -*-
import numpy as np
from PIL import Image
import os
import cv2

os.chdir(os.path.dirname(__file__))
# 由于opencv不支持读取中文路径，用以下方法代替cv2.imread
frame = cv2.imdecode(np.fromfile('get-captcha.jpeg', dtype=np.uint8), 1)

 
# 把 BGR 转为 HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 

#opencv中，H（色度）范围[0,255],S(饱和度)范围[0,255]，V(亮度)范围[0,115]
lower_blue = np.array([0,0,0]) 
upper_blue = np.array([255,255,115]) 
 
# 获得区域的mask
mask = cv2.imdecode(np.fromfile('mask.jpg', dtype=np.uint8), 1)
# 图片先转成灰度的
mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
# 再把图片转换为二值图
ret, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

#参数1：待修补的图像
#参数2：需要修补的位置
#参数3：修补半径
#参数4：修补方法
dst=cv2.inpaint(frame, mask, 5, cv2.INPAINT_NS)

cv2.namedWindow('inpaint', cv2.WINDOW_NORMAL)
cv2.imshow('inpaint',dst)
