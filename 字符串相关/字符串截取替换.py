#!/usr/bin/python
# -*- coding: UTF-8 -*-
import chardet

print("字符串内包含双引号和单引号：")
print("\'")
print("\"")
print("\n")


print("字符串内包含\\")
print(r"\\\\")
print("\n")

print("字符串内换行或引号时，也可以用三引号把字符串包含起来")
print('''我是a'
我是b"''')
print("\n")

a="abcdef"
print("字符串abcdef的长度为：")
print(len(a))


print("从第二位开始提取a[1:3]，向后提取2个字符（3-1=2）：")
print(a[1:3])
print("\n")

print("从第二位开始提取a[1:]，提取后方全部的字符")
print(a[1:])
print("\n")


print("提取最后一位：")
print(a[-1])
print("\n")

print("截取倒数第3位与倒数第2位之间的字符")
print(a[-3:-1])
print("\n")

print("截取倒数第3位到结尾的字符")
print(a[-3:])
print("\n")

print("将字符串中的b替换为空")
a='abcdef'
b=a.replace('b','')
print(b)
print("\n")


