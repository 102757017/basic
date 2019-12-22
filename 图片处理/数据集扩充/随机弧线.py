# coding: utf-8
#!/usr/bin/python
import os
import random
from skimage import draw,data,io
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(__file__))
img=io.imread("a.png")

#绘制曲线
#y0, x0 : int
#y1, x1 : int
#y2, x2 : int
#weight : double
rr, cc = draw.bezier_curve(random.randint(0, 56),5, random.randint(0, 56), 25, random.randint(0, 56), 50, 2)

#设置曲线颜色
curve_color=random.randint(0, 100)

draw.set_color(img,[rr,cc],[curve_color,curve_color,curve_color])
draw.set_color(img,[rr+1,cc],[curve_color,curve_color,curve_color])
draw.set_color(img,[rr-1,cc],[curve_color,curve_color,curve_color])

img=img.astype(np.uint8)

io.imshow(img)
plt.show()
