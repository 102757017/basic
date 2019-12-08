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


d={'code': {'code': 0, 'message': 'SUCCESS'}, 'data': {'dynStock': {'holdQuantity': 0, 'sellableQuantity': 8, 'sku': {';1627207:28320;': {'holdQuantity': 0, 'oversold': False, 'sellableQuantity': 8, 'stock': 8}}, 'stock': 8, 'stockType': 'normal'}}}
#多重dict的遍历,print所有根节点的值
def list_all_dict(dict_a):
    #使用isinstance检测数据类型
    if isinstance(dict_a,dict):
        for (x,y) in dict_a.items():
            if isinstance(y,dict):
                pass
            else:
                #print根节点的key.value
                print(x,y)
                
            #自我调用实现无限遍历
            list_all_dict(y)

list_all_dict(d)
