# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
import math

os.chdir(os.path.dirname(__file__))

 
#img = cv2.imread('test.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('part2.PNG', dtype=np.uint8), 1)

#拆分色彩通道
b, g, r = cv2.split(img)

#用高斯模糊来去掉噪声,但是同时也会使得边缘信息减弱，有可能使得在后面的步骤中漏掉一些需要的边缘,因此如何精确的选择高斯半径就相当重要。
# 较小的滤波器产生的模糊效果也较少，这样就可以检测较小、变化明显的细线。较大的滤波器产生的模糊效果也较多,这样带来的结果就是对于检测较大、平滑的边缘更加有用，
# 给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊
#gray=cv2.GaussianBlur(gray, (3, 3), 0)

#图像锐化，加强边缘
b = cv2.equalizeHist(b)
g = cv2.equalizeHist(g)
r = cv2.equalizeHist(r)

def nothing(x):
    pass


cv2.namedWindow('image')

# 创建滚动条
#参数一、trackbarname：滑动控件的名称；
#参数二、winname：滑动控件用于依附的图像窗口的名称；
#参数三、value：初始化阈值；
#参数四、count：滑动控件的刻度范围；
#参数五、TrackbarCallback是回调函数，其定义如下：
cv2.createTrackbar('k_min','image',70,200,nothing)
cv2.createTrackbar('ratio','image',2 ,6,nothing)



while(1):
    # 获取滚动条的位置
    c1 = cv2.getTrackbarPos('k_min','image')
    c2 = cv2.getTrackbarPos('ratio','image')

    # 提取轮廓
    target_b = cv2.Canny(b, c1, c1*c2)
    target_g = cv2.Canny(g, c1, c1*c2)
    target_r = cv2.Canny(r, c1, c1*c2)
    
    target=cv2.add(target_b,target_g)
    target=cv2.add(target,target_r)
    cv2.imshow('image',target)


    k = cv2.waitKey(1) & 0xFF
    #ESC键
    if k == 27:
        cv2.imwrite("edge.png",target)
        break


cv2.destroyAllWindows()

