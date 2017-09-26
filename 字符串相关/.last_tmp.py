#!/usr/bin/python
# -*- coding: UTF-8 -*-
import chardet


b='test str'
b=b.encode('ascii')
#含有中文的str无法用ASCII编码，因为中文编码的范围超过了ASCII编码的范围
print("将'test str'转换为ascii：")
a=open("/sdcard/qpython/scripts3/网络相关/webdriver(android)/百度搜索android.py","rb")
b=a.read()
print(b)

print(chardet.detect(b))
print("\n")


print("将ascii码的'test str'再转换为unicode码：")
b=b.decode('ascii')
print(b)
print("\n")


b='中文'
b=b.encode('utf-8')
print("将'中文'转换为utf-8：")
print(b)
print(chardet.detect(b))
print("\n")

print("将utf-8码的'中文'再转换为unicode码：")
b=b.decode('utf-8')
print(b)
print("\n")


b='中文'
print("将'中文'转换为GBK编码：")
b=b.encode('gbk')
print(b)
print(chardet.detect(b))
print("\n")

print("将GBK编码的'中文'再转换为unicode码：")
b=b.decode('gbk')
print(b)
print("\n")