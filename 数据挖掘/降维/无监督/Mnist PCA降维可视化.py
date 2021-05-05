# -*- coding: UTF-8 -*-
from sklearn.decomposition import PCA
import numpy as np
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

f=np.load('mnist.npz')
x_train = f['x_train']
y_train = f['y_train']

x_train=x_train.reshape(x_train.shape[0],-1)
print('x_train',x_train.shape)
print('y_train',y_train.shape)

#PCA是线性降维方法，PCA缺省参数为None，所有特征被保留，此处降为3维
t=datetime.datetime.now()
X_pca = PCA(3).fit_transform(x_train)
t2=datetime.datetime.now()-t
print("PCA降维耗时:",t2)
print("PCA降维后:",X_pca.shape)



trace0 = go.Scatter3d(x =X_pca[:, 0], y = X_pca[:, 1], z = X_pca[:, 2],mode = 'markers', marker = dict(size = 1,color = y_train, colorscale = 'Viridis'))
fig = make_subplots(rows=1,cols=1,subplot_titles=["PCA降维图"],specs=[[{"type": "scene"}]])
fig.append_trace(trace0, 1, 1) 
fig.show()