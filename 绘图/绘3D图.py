#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np


z = np.linspace(0,13,100)
x = 5*np.sin(z)
y = 5*np.cos(z)

# 生成画布
fig = plt.figure()

#生成子图，将画布分割成1行2列，图像画在从左到右从上到下的第1块
ax1=fig.add_subplot(121,projection='3d')
#绘制3D散点图
ax1.scatter3D(x,y,z,'red')

#生成子图，将画布分割成1行2列，图像画在从左到右从上到下的第2块
ax1=fig.add_subplot(122,projection='3d')
#绘制3D曲线图
ax1.plot3D(x,y,z,'red')

plt.show()
