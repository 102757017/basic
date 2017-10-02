# -*- coding: UTF-8 -*-

#数据读取模块genfromtxt；返回来一个给定形状和类型的用0填充的数组zeros
from numpy import genfromtxt, zeros
#绘图模块plot
from pylab import plot, show


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
print([target=='setosa'])
plot(data[target=='setosa',0],data[target=='setosa',2],'bo')
plot(data[target=='versicolor',0],data[target=='versicolor',2],'ro')
plot(data[target=='virginica',0],data[target=='virginica',2],'go')

#show()
