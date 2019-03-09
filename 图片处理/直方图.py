# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(__file__))

 
img = cv2.imread('captcha.jpg')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('get-captcha.jpeg', dtype=np.uint8), 1)



#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray",gray)

#参数1：输入图像，传入时应该用中括号[]括起来
#参数2：传入图像的通道，如果是灰度图像值为[0]，彩色图像值为0,1,2中选择一个，对应着BGR各个通道。这个值也得用[]传入
#参数3：掩膜图像。如果统计整幅图，那么为none
#参数4：使用多少个bin(柱子)，一般为256
#参数5：像素值的范围，一般为[0,255]表示0~255
hist=cv2.calcHist([gray],[0],None,[255],[0,255])
plt.plot(hist)
plt.show()
