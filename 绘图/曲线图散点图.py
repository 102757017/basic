#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from time import sleep


#只提供了一个list，matplotlib就会假设这个序列是Y轴上的取值，并且会自动为你生成X轴上的值
plt.plot([1,2,3,4],label="sample1")

#同时提供了x,y的值
plt.plot([0.5, 2, 3, 4], [1, 4, 5, 10],label="sample2")


#绘制散点图
plt.plot([0,2,3,4], [1,6,9,16], 'ro',label="sample3")

#绘制标签栏
#loc参数设置标签的显示位置，'best'为自适应方式
#ncol设置列的数量，使显示扁平化，当要表示的标签特别多的时候会有用
leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)

plt.show()
