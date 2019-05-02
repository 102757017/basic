# -*- coding: UTF-8 -*-
import os
from skimage import io,data,color,img_as_ubyte
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

os.chdir(os.path.dirname(__file__))
img=io.imread('test.png')
io.imshow(img)
plt.show()

print(type(img))
print(img.dtype)

#PIL(RGB)
#Skimage(RGB)
#OpenCV(BGR)

#转换为cv2的格式
img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

#转换回PIL格式
img = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

#PIL转换为array
img2 = np.asarray(img)

#转换回skimage格式
img=np.asarray(img,dtype=np.uint8)


#图片先转成灰度的
#在skimage中，一张彩色图片转换为灰度图后，数据会被归一化，它的类型就由unit8变成了float
gray=color.rgb2gray(img)


#将归一化的矩阵还原到0~255
gray=gray*255
grayr=gray.astype(np.uint8)

