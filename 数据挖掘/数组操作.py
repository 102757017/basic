# -*- coding: UTF-8 -*-
import numpy as np
from PIL import Image

#im=Image.open("aa.jpg")
#a=np.array(im)
#print(type(a),a.shape,a.dtype)

#创建一维数组
a=np.random.random(5)#创建随机数构成的数组，元素是5个
print("创建随机数构成的数组，元素是5个",a,'\n')

a=np.array([1,2,3,4,5,6])
print("创建制定元素的数组",a,'\n')

a=np.arange(1,6)#按照步长创建数组，默认步长为1
print("按照步长创建数组，默认步长为1",a,'\n')

a=np.arange(1,12,2)#指定步长为2的等差数列
print("指定步长为2的等差数列",a,'\n')

a=np.linspace(1,6,10)#指定元素个数为10个的等差数列
print("指定元素个数为10个的等差数列",a,'\n')

a=np.zeros((5, 2), dtype=float)
print("创建5*2的数组，用0填充",a,'\n')

a=np.ones((5, 2), dtype=float)
print("创建5*2的数组，用1填充",a,'\n')

a=np.empty((5, 2)) #empty()仅仅分配数组所使用的内存，不对数组元素进行初始化操作，因此它的运行速度是最快的
print("创建5*2的空数组",a,'\n')

'''二维数组是将一维数组叠放而成,即二维的高维每多一维,就是多一个一维数组.
同理的,三维数组是由多个二维数组叠放而成,三维的高维每多一维就是一个二维数组.
以此类推,四维数组就是将多个三维数组叠放而成的'''
a=np.zeros((5,3,2))
print("5个3*2数组构成一个3维数组",a,'\n')

#使用切片方式获取的数组与原数组共享内存，修改一个另一个会同时变更
print("[0,:,:]表示第一个3维数组，相当于正方体的第一个切面",a[0,:,:],'\n')
print("[1:3,:,:]表示第2个到第4个的3维数组",a[1:3,:,:],'\n')

a.copy()#返回数组的一个复制,和原数组不共享内存

print('数组形状',a.shape) #数组形状
print('\n')
print('数组维度',a.ndim) #数组维度
print('\n')
print('数组元素个数',a.size) #数组元素个数
print('\n')
print('数组元素类型',a.dtype) #元素数据类型
print('\n')

#改变数组形状，(m,n,p) m*n*p等于原数组元素总个数
#reshape()为浅层复制，创建的数组和原数组不共享内存，改变一个数组，另一个不会同时改变
b=a.reshape(6,5)
print(b)
print('\n')

#resize()为深层复制，创建的数组和原数组共享内存，改变一个数组，另一个会同时改变
a.resize(6,5)
print(a)
print('\n')

print('数组元素相加\n',a+a,'\n')
print('数组元素相减\n',a-a,'\n')
print('数组元素相乘\n',a*a,'\n')
print('数组元素相除，返回精确的商\n',a/a,'\n')
print('数组元素相除，返回值取整\n',a//a,'\n')
print('x>3生成布尔数组\n',a>3,'\n')
print('x==0.5生成布尔数组\n',a==0.5,'\n')
print('数组转置\n',a.T,'\n')

b=np.concatenate((a,a,a), axis=0)
print('水平连接数组',b,'\n')#水平连接数组

b=np.concatenate((a,a,a), axis=1)
print('垂直连接数组',b,'\n')#垂直连接数组
