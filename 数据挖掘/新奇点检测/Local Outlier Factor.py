# -*- coding: UTF-8 -*-
from sklearn.datasets import load_iris 
from sklearn.neighbors import LocalOutlierFactor
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
#解决中文乱码问题
from matplotlib.font_manager import FontProperties 
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10)


#新奇点检测: 训练数据未被离群点污染，我们对新观测值是否为离群点感兴趣。在这个语境下，离群点被认为是新奇点。

iris =load_iris()
print(iris["data"])
print(iris["target"])
print(iris["target_names"])
print(iris["data"].shape)

#正常点数据
X_train=iris["data"][:50]
Y_train=iris["target"][:50]


#异常点数据
iso_data=iris["data"][51:61]
iso_lable=iris["target"][51:61]

#混合数据
mix_data = np.r_[X_train,iso_data]
mix_lable=np.r_[Y_train,iso_lable]

'''
novelty:进行新奇点检测将其novelty参数设为True,这样的话，fit_predict方法就不可用了，在新的未见过的数据上，你只能使用 predict, decision_function 和 score_samples
neighbors.LocalOutlierFactor 类在离群点检测和新奇点检测中的行为被总结在下面的表中。
方法	             离群点检测	                       新奇点检测
fit_predict	         可用	                          不可用
predict	             不可用	                          只能用于新数据
decision_function	 不可用	                          只能用于新数据
score_samples	     用 negative_outlier_factor_	  只能用于新数据

decision_function = score_samples - offset_offset_
score_samples：与X的局部离群因子相反。越大越好，即较大的值对应于正常数据。
offset_:偏移量用于从原始分数中获取二进制标签。negative_outlier_factor小于的观察值offset_ 被检测为异常。默认的偏移设置为-1.5（inliers score around -1），除非提供的污染参数不同于“自动”。在那种情况下，以这样的方式定义偏移量，即我们可以在训练中获得预期的异常值数量。
'''

clf=LocalOutlierFactor(novelty=True)

#训练模型
clf.fit(X_train[0:40])

#训练数据集的异常得分
print(clf.negative_outlier_factor_)

#预测数据是否是异常值，正常值返回1，异常值返回-1
print(clf.predict(mix_data))

#预测数据的异常度：LOF的值越接近1，越可能是正常样本，LOF的值越大于1，则越可能是异常样本
y_score=-clf.decision_function(mix_data)
print(y_score)


# 生成画布
fig = plt.figure()

#生成子图
ax1 = fig.add_subplot(121)
ax1.set_title("标签-异常值显示图",fontproperties=font_set)
ax1.scatter(mix_lable, -clf.decision_function(mix_data),c=mix_lable)
ax1.set_xlabel('标签',fontproperties=font_set)
ax1.set_ylabel('异常度',fontproperties=font_set)


ax2 = fig.add_subplot(122)
fpr,tpr,threshold=metrics.roc_curve(mix_lable,y_score)
auc = metrics.auc(fpr, tpr)
print("auc:",auc)
ax2.set_title("ROC曲线图",fontproperties=font_set)
ax2.plot(fpr, tpr)
ax2.set_xlabel('假正率',fontproperties=font_set)
ax2.set_ylabel('真负率',fontproperties=font_set)

plt.show()