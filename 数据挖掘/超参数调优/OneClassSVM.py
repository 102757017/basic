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
#正常标签改写为1，异常标签改写为-1
label=np.ones_like(iris["target"])
label[50:]=-1



'''
采样贝叶斯优化的超参数调优模块
使用hyperopt的方法的步骤：
1.指定需要最小化的目标函数fmin
2.指定要搜索的空间
3.指定用于存储搜索的所有点评估的数据库
4.指定要使用的搜索算法
'''
from hyperopt import fmin, tpe, hp

from sklearn.model_selection import cross_val_score
# 定义目标函数
def f(params):
    clf = svm.OneClassSVM(**params)
    #训练模型
    clf.fit(X_train)
    pred=clf.predict(iris["data"])
    acc=np.sum(pred==label)/label.size
    return -acc

#2.指定要搜索的空间
#hp.uniform(label,low,high)参数label在low和high之间均匀分布
#hp.choice(label,options)，options是list或者tuple，参数label可选，为options中的一个元素
#hp.normal(label, mu, sigma)参数label正态分布，其中mu和sigma分别是均值和标准差
space= {
    'nu': hp.uniform('nu', 0,1),
    'kernel':hp.choice('kernel',["rbf","linear","poly","sigmoid"]),
    'gamma':hp.uniform('gamma', 0,1)
}
#fmin指定需要最小化的函数
#tpe表示tree of Parzen estimators，是一种算法
#max_evals 执行的最大评估次数，越大越容易找到最优解
best=fmin(f,space,algo=tpe.suggest,max_evals=100)
print(best)
