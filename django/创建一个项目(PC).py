#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import django


print("当前脚本工作的目录路径:")
path1=os.getcwd()
print(path1)
print('\n')

print("切换工作目录")
os.chdir(sys.path[0])
print("切换后脚本工作的目录路径:")
path1=os.getcwd()
print(path1)
print('\n')


c1='cmd & '
#c2=r'cd /sdcard/qpython/scripts3/基础操作/django/&'
#项目路径
#c3="ptthon django-admin startproject mysite"
c3=sys.executable+" "+"\""+sys.prefix+os.path.sep+"Scripts"+os.path.sep+"django-admin.py"+"\""+' startproject mysite'
c=c1+c3
print(c)

'''

&& 用来分隔不同的命令,&&"，
一个&也行，前者只有前面的命令执行成功才执行后面命令，后者不管前面是否成功都执行下去。
'''

#开始一个项目,在指定路径创建一个目录mysite
os.system(c)
