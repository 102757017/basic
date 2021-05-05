#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from mayavi import mlab

#pyecharts
#必须从conda-forge通道安装mayavi，默认通道安装的版本无法运行
#采用matplotlib绘制大型数据集的3D点云图时，旋转很卡，因此推荐采用mayavi绘制3D图

z = np.linspace(0,13,100)
x = 5*np.sin(z)
y = 5*np.cos(z)
s=np.zeros(len(z))


#scale_factor:控制球的大小
#用s控制点的颜色，而不改变球的大小，添加参数scale_mode
pl = mlab.points3d(x,y,z,s,scale_factor=.15,scale_mode="none")
mlab.axes(xlabel='x', ylabel='y', zlabel='z')
mlab.outline(pl)

p2 = mlab.points3d(x,y,-3-z,s,scale_factor=.15,scale_mode="none")
mlab.outline(p2)

mlab.show()