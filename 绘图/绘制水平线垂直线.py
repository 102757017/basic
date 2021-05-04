#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt

# 生成画布
fig = plt.figure()

#生成子图
ax = fig.add_subplot(111)

ax.hlines(y=55, xmin=0, xmax=100,colors='green')
ax.hlines(y=20, xmin=0, xmax=100,colors='green')
#无限长的水平线
ax.axhline(y=30,ls=':',c='green')

ax.vlines(x=30, ymin=0, ymax=60,colors='red')

plt.show()
