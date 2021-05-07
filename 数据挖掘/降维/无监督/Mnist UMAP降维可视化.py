# -*- coding: UTF-8 -*-
import umap
import numpy as np
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#UMAP比TSNE速度快很多，与大多数t-SNE实现相比，UMAP在保留数据全局结构的某些方面通常表现更好。这意味着它通常可以为您的数据提供更好的“概览”视图，并且可以保留本地邻居关系。

f=np.load('mnist.npz')
x_train = f['x_train']
y_train = f['y_train']

x_train=x_train.reshape(x_train.shape[0],-1)
print('x_train',x_train.shape)
print('y_train',y_train.shape)


t=datetime.datetime.now()
'''
n_neighbors：这确定在流形结构的局部近似中使用的相邻点的数量。较大的值将导致保留更多的全局结构，而不会丢失详细的局部结构。通常，此参数通常应在5到50的范围内，明智的默认选择是10到15。
min_dist：这控制允许将压缩点压缩在一起的紧密程度。较大的值可确保嵌入点的分布更均匀，而较小的值可使算法针对局部结构更准确地进行优化。明智的值是在0.001到0.5的范围内，其中0.1是一个合理的默认值。
metric：确定用于测量输入空间中距离的度量标准的选择。各种各样的度量标准已经编码，并且只要numba已将其定义为JITd，就可以传递用户定义的函数。
'''
X_umap =umap.UMAP(n_components=5,min_dist=0.01,metric='correlation').fit_transform(x_train)
t1=datetime.datetime.now()-t
print("UMPA降维耗时:",t1)
print("UMAP降维后:",X_umap.shape)


trace0 = go.Scatter3d(x =X_umap[:, 0], y = X_umap[:, 1], z = X_umap[:, 2],mode = 'markers', marker = dict(size = 1,color = y_train, colorscale = 'Viridis'))
fig = make_subplots(rows=1,cols=1,subplot_titles=["UMAP降维图"],specs=[[{"type": "scene"}]])
fig.append_trace(trace0, 1, 1) 
fig.show()