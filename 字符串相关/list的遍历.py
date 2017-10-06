#!/usr/bin/python
# -*- coding: UTF-8 -*-


#如果对一个列表，既要遍历索引又要遍历元素时，可以这样写,enumerate()可以同时获得索引和值
list1 = ["这", "是", "一个", "测试"]
for index, item in enumerate(list1):
    print(index, item)
