# -*- coding: UTF-8 -*-
import numpy as np
from PIL import Image

#im=Image.open("aa.jpg")
#a=np.array(im)
#print(type(a),a.shape,a.dtype)

#创建一维矩阵
a=np.random.random(5)#创建随机数构成的矩阵，元素是5个
print("创建随机数构成的矩阵，元素是5个",a,'\n')
print(a.shape)


a=np.array([1,2,3,4,5,6])
print("创建制定元素的矩阵\n",a,'\n')

a=np.arange(1,6)#按照步长创建矩阵，默认步长为1
print("按照步长创建矩阵，默认步长为1\n",a,'\n')

a=np.arange(1,12,2)#指定步长为2的等差数列
print("指定步长为2的等差数列\n",a,'\n')

a=np.linspace(1,6,10)#指定元素个数为10个的等差数列
print("指定元素个数为10个的等差数列\n",a,'\n')

a=np.zeros((5, 2), dtype=float)
print("创建5*2的矩阵，用0填充\n",a,'\n')

a=np.ones((5, 2), dtype=float)
print("创建5*2的矩阵，用1填充\n",a,'\n')

a=np.empty((5, 2)) #empty()仅仅分配矩阵所使用的内存，不对矩阵元素进行初始化操作，因此它的运行速度是最快的
print("创建5*2的空矩阵\n",a,'\n')

'''二维矩阵是将一维矩阵叠放而成,即二维的高维每多一维,就是多一个一维矩阵.
同理的,三维矩阵是由多个二维矩阵叠放而成,三维的高维每多一维就是一个二维矩阵.
以此类推,四维矩阵就是将多个三维矩阵叠放而成的'''
a=np.zeros((5,3,2))
print("5个3*2矩阵构成一个3维矩阵\n",a,'\n')

#使用切片方式获取的矩阵与原矩阵共享内存，修改一个另一个会同时变更
print("[0,:,:]表示第一个3维矩阵，相当于正方体的第一个切面\n",a[0,:,:],'\n')
print("[1:3,:,:]表示第2个到第4个的3维矩阵\n",a[1:3,:,:],'\n')

a.copy()#返回矩阵的一个复制,和原矩阵不共享内存

print('矩阵形状',a.shape) #矩阵形状
print('\n')
print('矩阵维度',a.ndim) #矩阵维度
print('\n')
print('矩阵元素个数',a.size) #矩阵元素个数
print('\n')
print('矩阵元素类型',a.dtype) #元素数据类型
print('\n')

#改变矩阵形状，(m,n,p) m*n*p等于原矩阵元素总个数
#reshape()为浅层复制，创建的矩阵和原矩阵不共享内存，改变一个矩阵，另一个不会同时改变
b=a.reshape(6,5)
print(b)
print('\n')

#将数据转换为一行，“-1”为通配符，有函数自动计算数值
b=a.reshape(1,-1)
print(b)
print('\n')

#将数据转换为二列，“-1”为通配符，有函数自动计算数值
b=a.reshape(-1,2)
print(b)
print('\n')

#resize()为深层复制，创建的矩阵和原矩阵共享内存，改变一个矩阵，另一个会同时改变
a.resize(6, 5)
print(a)
print('\n')

print('矩阵元素相加\n',a+a,'\n')
print('矩阵元素相减\n',a-a,'\n')
print('矩阵元素相乘\n',a*a,'\n')
print('矩阵元素相除，返回精确的商\n',a/a,'\n')
print('矩阵元素相除，返回值取整\n',a//a,'\n')
print('x>3生成布尔矩阵\n',a>3,'\n')
print('x==0.5生成布尔矩阵\n',a==0.5,'\n')
print('矩阵转置\n',a.T,'\n')
print("矩阵沿第一个维度相加\n",np.sum(a, axis=-1, keepdims=True),'\n')
print("矩阵元素的最大值\n",np.max(a),'\n')
print("矩阵元素取较大值\n",np.maximum(a,2),'\n')


a=np.array([1,2,3,4,5,3])
print('获取x<3的数据的坐标，如果是n维矩阵，则返回n个矩阵')
print(np.where(a<3),'\n')
print('获取x<3的数据')
print(a[np.where(a<3)],'\n')
print('用布尔矩阵获取x<3的数据')
print(a[a<3],'\n')
print('返回与a相同shape的全1矩阵')
print(np.ones_like(a),'\n')


a=a.reshape(1,-1)
b=np.concatenate((a,a,a), axis=0)
print('axis=0连接矩阵\n',b,'\n')#水平连接矩阵

b=np.concatenate((a,a,a), axis=1)
print('axis=1连接矩阵\n',b,'\n')#垂直连接矩阵

b=np.r_[a,a,a]
print('按列连接两个矩阵，就是把两矩阵上下相加，要求列数相等\n',b,'\n')#按列连接两个矩阵，就是把两矩阵上下相加，要求列数相等

b=np.c_[a,a,a]
print('按行连接两个矩阵，就是把两矩阵左右相加，要求行数相等\n',b,'\n')#按行连接两个矩阵，就是把两矩阵左右相加，要求行数相等
