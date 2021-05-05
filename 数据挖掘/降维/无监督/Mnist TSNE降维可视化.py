# -*- coding: UTF-8 -*-
from sklearn.manifold import TSNE
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

#tsns在大数据集上耗时太长，若不使用cuda加速，需要计算几个小时才能出结果。
#TSNE与keras中的池化层作用类似，是非线性降维，PCA是线性降维
#TSNE期望的输入数据是np.array，默认会将数据降成两维，指定n_components=3时可将数据降为三纬
#T-SNE，PCA是无监督学习方法，输入的数据不需要标记，根据样本间的相似性对样本集进行自动分类
#tsne 保留下的属性信息，更具代表性，也即最能体现样本间的差异；TSNE 运行极慢，PCA 则相对较快；因此更为一般的处理，尤其在展示（可视化）高维数据时，常常先用 PCA 进行降维，再使用 tsne：
#init:设置初始化方式，可选random或者pca，这里用pca，比起random init会更稳定一些
#perplexity:困惑度，较大的数据集通常需要较大的困惑度。考虑选择一个介于5到50之间的值。不同的值会导致明显不同的结果。
t=datetime.datetime.now()
X_tsne = TSNE(learning_rate=100,init='pca',perplexity=30,n_components=3).fit_transform(x_train)
t1=datetime.datetime.now()-t
print("T-SNE降维耗时:",t1)
print("T-SNE降维后:",X_tsne.shape)


trace0 = go.Scatter3d(x =X_tsne[:, 0], y = X_tsne[:, 1], z = X_tsne[:, 2],mode = 'markers', marker = dict(size = 1,color = y_train, colorscale = 'Viridis'))
fig = make_subplots(rows=1,cols=1,subplot_titles=["T-SNE降维图"],specs=[[{"type": "scene"}]])
fig.append_trace(trace0, 1, 1) 
fig.show()