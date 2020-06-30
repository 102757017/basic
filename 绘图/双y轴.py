#!/usr/bin/python
#coding: utf-8
 
import numpy as np
import matplotlib.pyplot as plt
 
x = np.arange(1, 2, 0.1)
 
y1 = x * x
y2 = x+100
 
plt.plot(x, y1)
 
# 添加一条坐标轴，此后绘制的图都画在第二个y轴上
plt.twinx()
plt.plot(x, y2,color="r")
 
plt.show()
