#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pprint


#可迭代对象，包括list，dict，truple,string均可用以下方法排序
def byname(x):
    return x[0]

def byscore(x):
    return x[1]

L=[['Bob',75],['Adam',92],['Bart',66],['Lisa',88]]

#按名字排序
a=sorted(L, key=byname)
print('按名字排序',a)

#按分数排序
a=sorted(L, key=byscore)
print('按分数排序',a)



#按分数反向排序
a=sorted(L, key=byscore,reverse=True)
print('按分数反向排序',a)

d={'Michael':95,'Bob':75,'Tracy':85}




#按名字排序
a=sorted(d, key=byname)
print('按名字排序',a)

#按分数排序
a=sorted(d, key=byscore)
print('按分数排序',a)

#按分数反向排序
a=sorted(d, key=byscore,reverse=True)
print('按分数反向排序',a)

