# -*- coding: UTF-8 -*-
from sklearn.datasets import load_iris 
import matplotlib.pyplot as plt
from sklearn import svm
import sys 
import os
import numpy as np

#奇异点检测：训练数据中没有离群点，我们是对检测新发现的样本点感兴趣

#给系统添加环境变量，修改的环境变量是临时改变的，当程序停止时修改的环境变量失效（系统变量不会改变）
os.environ["Path"] += os.pathsep + r"G:\Program Files\WinPython-64bit-3.6.1.0Qt5\graphviz\bin"

iris =load_iris()
print(iris["data"])
print(iris["target"])
print(iris["target_names"])
print(iris["data"].shape)

#正常点数据
X_train=iris["data"][:50]

#异常点数据
iso_data=iris["data"][51:110]

#nu:错分样本所占比例的上限，0~1之间
#kernel:根据经验判断数据可能是那种分布。‘linear’：线性；‘rbf’：高斯分布等等
#gamma:如果gamma设的太大，高斯分布长得又高又瘦， 会造成只会作用于支持向量样本附近，对于未知样本分类效果很差，容易过拟合；而如果设的过小，则会造成平滑效应太大，无法在训练集上得到特别高的准确率，容易欠拟合。
#verbose:是否显示训练进程
clf = svm.OneClassSVM(nu=0.02, kernel="rbf", gamma=0.097,verbose=1)

#训练模型
clf.fit(X_train)

#返回值：+1 表示正常样本， -1表示异常样本。
print(clf.predict(iris["data"]))
#异常度
print(clf.decision_function(iso_data))
