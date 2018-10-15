#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np

# 生成画布
fig=plt.figure()

#生成子图，将画布分割成1行1列，图像画在从左到右从上到下的第1块
ax1=fig.add_subplot(311)
#设置子图横坐标范围
ax1.set_xlim(0, 5)
#设置子图纵坐标范围
ax1.set_ylim(0, 5)
ax1.plot([1,2,3,4])
ax1.set_title("sample1")

#生成子图
ax2=fig.add_subplot(312)
ax2.plot([0.5, 2, 3, 4], [1, 4, 5, 10])
ax2.set_title("sample2")

#生成子图
ax3=fig.add_subplot(313)
ax3.plot([0,2,3,4], [1,6,9,16], 'ro')
ax3.set_title("sample3")


plt.show()
