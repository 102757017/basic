#!/usr/bin/python
# -*- coding: UTF-8 -*-
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

z = np.linspace(0,13,100)
x = 5*np.sin(z)
y = 5*np.cos(z)

#子图1
trace0 = go.Scatter3d(x = x, y = y, z = z,mode = 'markers', marker = dict(size = 12,color = z, colorscale = 'Viridis'))
#子图2
trace1 = go.Scatter3d(x = x, y = y, z = z,mode = 'markers', marker = dict(size = 5,color = 1, colorscale = 'Viridis'))

'''
specs用来指定子图的类型
“ xy”：散点图，柱状图等的2D子图类型。如果未指定类型，则这是默认设置。
“scene”：用于3D散点图，圆锥体等的子图。
“polar”：极坐标散点图，极坐标上的柱状图等。
“ternary”：三元图子图。
“ mapbox”：地理地图子图。
'''
fig = make_subplots(rows=1,cols=2,subplot_titles=["trace0的标题", "trace1的标题"],specs=[[{"type": "scene"}, {"type": "scene"}]])
fig.append_trace(trace0, 1, 1) 
fig.append_trace(trace1, 1, 2) 


fig.show()