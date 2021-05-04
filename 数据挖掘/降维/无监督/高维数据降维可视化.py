# -*- coding: UTF-8 -*-
from sklearn.manifold import TSNE
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sklearn

iris =load_iris()
print(iris["data"])
print(iris["target"])
print(iris["target_names"])
print(iris["data"].shape)

#TSNE与keras中的池化层作用类似，是非线性降维，PCA是线性降维
#TSNE期望的输入数据是np.array，默认会将数据降成两维，指定n_components=3时可将数据降为三纬
#T-SNE，PCA是无监督学习方法，输入的数据不需要标记，根据样本间的相似性对样本集进行自动分类
#tsne 保留下的属性信息，更具代表性，也即最能体现样本间的差异；TSNE 运行极慢，PCA 则相对较快；因此更为一般的处理，尤其在展示（可视化）高维数据时，常常先用 PCA 进行降维，再使用 tsne：

#init:设置初始化方式，可选random或者pca，这里用pca，比起random init会更稳定一些
#perplexity:困惑度，较大的数据集通常需要较大的困惑度。考虑选择一个介于5到50之间的值。不同的值会导致明显不同的结果。
X_tsne = TSNE(learning_rate=100，init='pca',perplexity=30).fit_transform(iris.data)

#PCA是线性降维方法，PCA缺省参数为None，所有特征被保留，此处降为2维
X_pca = PCA(2).fit_transform(iris.data)

print("T-SNE降维后:",X_tsne.shape)
print("PCA降维后:",X_pca.shape)


#使用T-SNE降维绘子图
plt.subplot(121)
plt.title("T-SNE")
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=iris.target)

#使用PCA降维绘子图
plt.subplot(122)
plt.title("PCA")
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=iris.target,label="PCA")


plt.show()
