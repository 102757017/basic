# -*- coding: UTF-8 -*-
from sklearn.datasets import load_iris 
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import sys 
import os
import graphviz
import numpy as np
from scipy import stats

#异常点检测：训练数据中包含离群点，我们需要适配训练数据中的中心部分（密集的部分），忽视异常点
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
iso_data=iris["data"][51:61]

#混合数据
X_train = np.r_[X_train,iso_data]

#max_samples：样本总数
#random_state：随机数生成器
#contamination：异常样本的比例
clf=IsolationForest(max_samples=60, random_state=np.random.RandomState(42), contamination=10/60)

#训练模型
clf.fit(X_train)
#返回值：+1 表示正常样本， -1表示异常样本。
print(clf.predict(iris["data"][40:70]))


