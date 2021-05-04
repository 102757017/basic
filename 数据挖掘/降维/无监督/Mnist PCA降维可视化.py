# -*- coding: UTF-8 -*-
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import datetime


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


# 生成画布
fig = plt.figure()
#生成子图，将画布分割成1行1列，图像画在从左到右从上到下的第2块
ax1=fig.add_subplot(111,projection='3d')
#使用PCA降维绘制3D散点图
ax1.scatter3D(X_pca[:, 0], X_pca[:, 1],X_pca[:, 2],s=1,c=y_train)

plt.show()