# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np


os.chdir(os.path.dirname(__file__))

 
img = cv2.imread('part1.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('part1.png', dtype=np.uint8), 1)

#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊
#gray=cv2.GaussianBlur(gray, (3, 3), 0)  


#gray=cv2.Canny(gray,100,300)

def nothing(x):
    pass


cv2.namedWindow('image')

# 创建滚动条
#参数一、trackbarname：滑动控件的名称；
#参数二、winname：滑动控件用于依附的图像窗口的名称；
#参数三、value：初始化阈值；
#参数四、count：滑动控件的刻度范围；
#参数五、TrackbarCallback是回调函数，其定义如下：
cv2.createTrackbar('k','image',5,100,nothing)



while(1):
    # 获取滚动条的位置
    c1 = cv2.getTrackbarPos('k','image')

    #把图片转换为二值图
    #自适应阈值，倒数第二个参数是窗口大小，窗口大小必须为奇数，当窗口大小=图像大小时，等同于全局阈值

    binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,2*c1+3,3) 
    cv2.imshow("image", binary)


    
    k = cv2.waitKey(1) & 0xFF
    #ESC键
    if k == 27:
        cv2.imwrite("binary.png",binary)
        break

cv2.destroyAllWindows()

