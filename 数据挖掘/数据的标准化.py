# -*- coding: UTF-8 -*-

def datastandard():
  from sklearn import preprocessing
  import numpy as np
  x = np.array([
    [ 1., -1.,  2.],
    [ 2.,  0.,  0.],
    [ 0.,  1., -1.]])
  print('原始数据为：\n',x,'\n\n')

  
  '''
  总体方差：计算数据为总体，总体数量为n,计算公式为σ^2=[((x1-x)^2 +(x2-x)^2 +......(xn-x)^2)/n]，excel中的公式为STDEV()
  样本方差：计算数据为总体中的样本，用样品数据来估算总体的方差，样本数据为n，
            因为总体方差总会大于样本方差，因此最后除以（n-1），计算公式为σ^2=[((x1-x)^2 +(x2-x)^2 +......(xn-x)^2)/（n-1)]，excel中的公式为VAR.P()
  标准差：标准差为方差的平方根，即σ
  '''
  print('使用scale()函数 按"列"将数据标准化,(默认均值0 方差 1)，标准化计算公式：(X - avg)/ σ')
  x_scaled = preprocessing.scale(x,axis=0)
  print('标准化后矩阵为:\n',x_scaled)
  print('处理后数据的均值:', x_scaled.mean(axis=0))
  print('处理后数据的总体方差:', x_scaled.std(axis=0))
  print("\n")


  print('使用scale()函数 按"行"将数据标准化')
  x_scaled = preprocessing.scale(x,axis=1)
  print('标准化后矩阵为:\n',x_scaled)
  print('处理后数据的均值:', x_scaled.mean(axis=1))
  print('处理后数据的总体方差:', x_scaled.std(axis=1))
  print("\n")



  print('\nmethod2:StandardScaler类,可以保存转换前的参数')
  scaler = preprocessing.StandardScaler().fit(x)
  #print('标准化前 均值方差为:',scaler.mean_,scaler.scale_)
  print('处理前数据的均值:', scaler.mean_)
  print('处理前数据的总体方差:', scaler.var_)
  print('处理前数据的标准差:', scaler.scale_)
  
  y=scaler.transform(x)
  print('标准化后矩阵为:\n',y)
  print("\n")


  #将标准化后的数据转换成原来的数据
  d=scaler.inverse_transform(y)
  print("还原后的数据为：\n",d,"\n")





  print('2.数据归一化,映射到区间[min,max]：')
  '''使用这种方法的目的包括：
  1、对于方差非常小的属性可以增强其稳定性。
  2、维持稀疏矩阵中为0的条目。
  '''  
  min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1)).fit(x)
  y=min_max_scaler.transform(x)
  print(y)
  
  print("还原后的数据为：\n",min_max_scaler.inverse_transform(y))


if __name__ == '__main__':
  datastandard()
