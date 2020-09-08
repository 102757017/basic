# coding: utf-8
#!/usr/bin/python
import numpy as np
import cv2
import matplotlib.pyplot as plt
import Augmentor
import os
import sys

os.chdir(sys.path[0])
img = cv2.imdecode(np.fromfile("a.png", dtype=np.uint8), 1)
#Augmentor一次可以处理n个图片，此例只有一张图片，所以需要转换shape
img=img.reshape(1,img.shape[0],img.shape[1],img.shape[2])
label=np.array([0],dtype=np.uint8)
#建立管道
p = Augmentor.Pipeline()
#添加变形
p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=4)
#添加数据集
g=p.keras_generator_from_array(img,label,batch_size=10)

X, y = next(g)

print(type(X[0]))
print(X[0].shape)
print(X[0].dtype)

#将归一化的矩阵还原到0~255
X[0]=X[0]*255
plt.imshow(X[0], cmap="Greys")
plt.show()

