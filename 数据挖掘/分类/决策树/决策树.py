# -*- coding: UTF-8 -*-
import graphviz
from sklearn.datasets import load_iris 
from sklearn import tree 
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


#生成树
clf = tree.DecisionTreeClassifier()
#决策树拟合
clf = clf.fit(iris["data"], iris["target"])

#自己随便写的一个样本数据
x_new=[5,3,1,0.1]
#将数据转换为一行的矩阵
x_new = np.array(x_new).reshape(1, -1)
#预测
print("x_new的预测结果：",clf.predict(x_new))

#将模型存入dot数据
dot_data = tree.export_graphviz(clf, out_file=None)

#转换dot数据
graph = graphviz.Source(dot_data)
#决策树可视化，在同级目录下生成tree.pdf文件
graph.render("tree")
