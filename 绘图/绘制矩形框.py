#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt

# 生成画布
fig = plt.figure()

#生成子图
ax = fig.add_subplot(111)

#生成矩形
#facecolor='none'表示矩形内不填充
rect = plt.Rectangle((0.1,0.1),0.5,0.3,linewidth=1,edgecolor='r',facecolor='none')

#将矩形添加到子图中
ax.add_patch(rect)

plt.show()
