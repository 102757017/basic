# -*- coding: UTF-8 -*-
from sklearn.datasets import load_iris 
from sklearn.cluster import KMeans
import sys 
import os
import numpy as np

#给系统添加环境变量，修改的环境变量是临时改变的，当程序停止时修改的环境变量失效（系统变量不会改变）
os.environ["Path"] += os.pathsep + r"G:\Program Files\WinPython-64bit-3.6.1.0Qt5\graphviz\bin"

iris =load_iris()
print(iris["data"])
print(iris["target"])
print(iris["target_names"])
print(iris["data"].shape)
X = iris["data"]



#构造聚类器，分3类
estimator = KMeans(n_clusters=3)
#聚类
estimator.fit(iris["data"])
# 获取聚类标签
label_pred = estimator.labels_  
print(label_pred)

