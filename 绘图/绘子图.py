#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np


#画子图，将画布分割成1行1列，图像画在从左到右从上到下的第1块
plt.subplot(311)
plt.plot([1,2,3,4],label="sample1")

plt.subplot(312)
plt.plot([0.5, 2, 3, 4], [1, 4, 5, 10],label="sample2")

plt.subplot(313)
plt.plot([0,2,3,4], [1,6,9,16], 'ro',label="sample3")

plt.show()
