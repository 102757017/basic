# -*- coding: UTF-8 -*-
from sklearn.datasets import load_iris 
from sklearn.ensemble import RandomForestClassifier
import sys 
import os
import graphviz
import numpy as np

#给系统添加环境变量，修改的环境变量是临时改变的，当程序停止时修改的环境变量失效（系统变量不会改变）
os.environ["Path"] += os.pathsep + r"G:\Program Files\WinPython-64bit-3.6.1.0Qt5\graphviz\bin"

iris =load_iris()
print(iris["data"])
print(iris["target"])
print(iris["target_names"])
print(iris["data"].shape)


#n_estimators：指定森林中树的颗数，越多越好，只是不要超过内存
#max_features：指定了在分裂时，随机选取的特征数目，sqrt即为全部特征的平均根
#min_samples_leaf：指定每颗决策树完全生成，即叶子只包含单一的样本
#n_jobs：指定并行使用的进程数
rf=RandomForestClassifier(n_estimators=50,max_features="sqrt",min_samples_leaf=1,n_jobs=4)
#训练模型
rf.fit(iris["data"],iris["target"])

#自己随便写的一个样本数据
x_new=[5,3,1,0.1]
#将数据转换为一行的矩阵
x_new = np.array(x_new).reshape(1, -1)
#预测
print("x_new的预测结果：",rf.predict(x_new))
