#!/usr/bin/python
# -*- coding: UTF-8 -*-


d={'Michael':95,'Bob':75,'Tracy':85}

#默认情况下dict迭代的是key值
for x in d:
    print(x)
print('\n')

#也可以用如下形式
for x in d.keys():
    print(x)
print('\n')

#如果要迭代value
for x in d.values():
    print(x)
print('\n')

#如果要同时迭代key和value

for (x,y) in d.items():
    print(x,y)
print('\n')
