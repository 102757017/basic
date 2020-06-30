#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import pprint

# 生成画布
fig=plt.figure()

#生成子图，将画布分割成1行1列，图像画在从左到右从上到下的第1块
ax1=fig.add_subplot(111)
#设置子图横坐标范围
ax1.set_xlim(0, 5)
#设置子图纵坐标范围
ax1.set_ylim(0, 5)
ax1.plot([1,2,3,4])
ax1.set_title("sample1")

#写入到本地的文件
plt.savefig('to_img.jpg')


#写入到内存中
file=BytesIO()
plt.savefig(file,format="png")
img=file.getvalue()


#读取到的是numpy矩阵的格式
img=plt.imread('to_img.jpg')

#将numpy矩阵保存为图片
plt.imsave('to_img.jpg',img)

#img为numpy矩阵格式
plt.imshow(img)
plt.show()
