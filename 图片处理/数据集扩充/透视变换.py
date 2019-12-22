# coding: utf-8
#!/usr/bin/python
import numpy as np
import cv2
import matplotlib.pyplot as plt
import Augmentor
import os

os.chdir(os.path.dirname(__file__))
img = cv2.imdecode(np.fromfile("a.png", dtype=np.uint8), 1)
#Augmentor一次可以处理n个图片，此例只有一张图片，所以需要转换shape
img=img.reshape(1,img.shape[0],img.shape[1],img.shape[2])
label=np.array([0],dtype=np.uint8)
#建立管道
p = Augmentor.Pipeline()
#添加变形
p.skew_tilt(probability=1,magnitude=0.5)
#添加数据集
g=p.keras_generator_from_array(img,label,batch_size=10)

X, y = next(g)

plt.imshow(X[0], cmap="Greys")
plt.show()

