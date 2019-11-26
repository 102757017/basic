#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from matplotlib.animation import FuncAnimation


#matplotlib主要用来绘制静态图，绘制动图刷新率较低
# 生成画布
fig=plt.figure()

#生成子图
ax=fig.add_subplot(111)

xdata, ydata = [], []

# ,表示创建tuple类型
ln, = ax.plot([], [], 'r-', animated=False)

def init():
    #设置子图横坐标范围
    ax.set_xlim(0, 2*np.pi)
    #设置子图纵坐标范围
    ax.set_ylim(-1, 1)
    return ln,

#可以在update函数中判断当前数据包是不是新的，如果是则更新图像
def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

#生成器函数，不断检测数据包是否更新，并将结果返回给update函数
def gen_function():
    return np.linspace(0, 2*np.pi, 12800)

#参数fig是画布
#参数func是更新图形的函数
#frames 在函数运行时，其值会传递给函数update(n)的形参“n”
#intit_func是图形开始使用的函数
#interval是更新的间隔时间(ms)
#blit决定是更新整张图的点(Flase)还是只更新变化的点（True）
ani = FuncAnimation(fig, func=update, frames=gen_function(),init_func=init,interval=5, blit=True)


plt.show()
