#!/usr/bin/python
# -*- coding: UTF-8 -*-



a = "这是一个测试，这是另一个测试"
b=set(a)
print('字符串转换为set',b)

c = ["这", "是", "一个", "测试"]
d=set(c)
print('list转换为set',d)

print("求交集",b&d)

print("求差集",b-d)

print("求并集",b|d)

print("求对称差集",b^d)
