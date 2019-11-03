#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np

#解决中文乱码问题
from matplotlib.font_manager import FontProperties 
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10)

# 生成画布
fig=plt.figure()

#生成子图，将画布分割成1行1列，图像画在从左到右从上到下的第1块
ax1=fig.add_subplot(111)
#设置子图横坐标范围
ax1.set_xlim(0, 20)
#设置子图纵坐标范围
ax1.set_ylim(0, 9)

ax1.plot([1, 0, 1, 1, 2, 4, 3, 2, 3, 4, 4, 5, 6, 5, 4, 3, 3, 1, 1, 1])
ax1.set_title("sample1")

#添加注释
#xy 为被注释的坐标点
#xytext 为注释文字的坐标位置
#arrowprops 箭头参数,参数类型为字典dict。shrink：总长度的一部分，从两端“收缩”facecolor：箭头颜色
plt.annotate('max', xy=(5, 4), xytext=(4, 5),arrowprops=dict(facecolor='black', shrink=0.05))

plt.show()
