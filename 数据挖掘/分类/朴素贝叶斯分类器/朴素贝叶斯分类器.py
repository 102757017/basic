# -*- coding: UTF-8 -*-
import os
import sys

os.chdir(sys.path[0])

#数据读取模块genfromtxt；返回来一个给定形状和类型的用0填充的数组zeros
from numpy import genfromtxt, zeros

#绘图模块plot
from pylab import plot, show

#GaussianNB分类器模块
from sklearn.naive_bayes import GaussianNB

#把样本分为训练集和测试集进行交叉验证
from sklearn import model_selection

#用混淆矩阵评价测试结果
from sklearn.metrics import confusion_matrix

#用分类器评价测试结果
from sklearn.metrics import classification_report

#多次将数据分为不同的训练集和测试集，最终分类器评估选取多次预测的平均值。
from sklearn.model_selection import cross_val_score

#算平均数
from numpy import mean

# 读取前4列
data = genfromtxt('iris.csv',delimiter=',',usecols=(0,1,2,3))

# 读取第5列
target = genfromtxt('iris.csv',delimiter=',',usecols=(4),dtype=str)

print(data)
print("返回矩阵对象data",type(data))
print("矩阵大小",data.shape)
print("\n")


print(target)
print("返回矩阵对象target",type(target))
print("矩阵大小",target.shape)
print("\n")

'''
plot为绘图函数，plot(x,y,color)内分别为横坐标,纵坐标，颜色。坐标参数可以是list
bo---blue   co---cyan  go---green    ko----black
mo---magenta ro---red  wo---white    yo----yellow
'''
plot(data[target=='setosa',0],data[target=='setosa',2],'bo')
plot(data[target=='versicolor',0],data[target=='versicolor',2],'ro')
plot(data[target=='virginica',0],data[target=='virginica',2],'go')
#show()

#zeros(n)构造n*1的矩阵,zeros((n,m))构造n*m的矩阵，矩阵全部用0填充
t = zeros(len(target))
t[target == 'setosa'] =1
t[target == 'versicolor'] =2
t[target == 'virginica'] =3
print(t)
print("将target矩阵中的字符串替换成“1、2、3”返回矩阵对象t",type(t))
print("矩阵大小",t.shape)
print("\n")

#创建一个分类器
classifier = GaussianNB()


train,test,t_train,t_test = model_selection.train_test_split(data, t,test_size=0.4, random_state=0)
print("训练集数据矩阵",train.shape)
print("测试集数据矩阵",test.shape)
print("训练集结果矩阵",t_train.shape)
print("测试集结果矩阵",t_test.shape)
print("\n")

#用训练集数据训练分类器
classifier.fit(train,t_train)


#用测试集数据评价分类器准确率
a=classifier.score(test,t_test)
print("综合评价测试集测试准确率",a)
print("\n")

print("用混淆矩阵评价：")
print(confusion_matrix(classifier.predict(test),t_test))
print("\n")

print('''用分类器评价测试结果：
Precision：正确预测的比例
Recall（或者叫真阳性率）：正确识别的比例
F1-Score：precision和recall的调和平均数''')
print(classification_report(classifier.predict(test), t_test, target_names=['setosa', 'versicolor', 'virginica']))
print("\n")

print("6次将数据分为不同的训练集和测试集，最终分类器评估选取多次预测的平均值：")
scores = cross_val_score(classifier, data, t, cv=6)
print("6次的正确率分别为：",scores)
print("平均正确率为：",mean(scores))
