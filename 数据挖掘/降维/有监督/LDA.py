# -*- coding: UTF-8 -*-
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
import sklearn
from sklearn.datasets import load_iris

iris =load_iris()
print(iris["data"])
print(iris["target"])
print(iris["target_names"])
print(iris["data"].shape)


#n_components：指定LDA降维后的特征数
model_lda = LinearDiscriminantAnalysis(n_components=2)

X_lda = model_lda.fit_transform(iris["data"], iris["target"])
print("LDA降维后:",X_lda.shape)


plt.subplot(111)
plt.scatter(X_lda[:, 0], X_lda[:, 1], c=iris["target"],label="LDA")



plt.show()
