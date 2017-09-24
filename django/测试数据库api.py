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
#此处的mysite为项目名称
path2=sys.path[0]+os.path.sep+"mysite"
os.chdir(path2)
print("切换后脚本工作的目录路径:")
path1=os.getcwd()
print(path1)


#载入django设定后启动shell
c1='sh & '
#c2="python manage.py shell"
c2=sys.executable+" "+"manage.py shell"

c=c1+c2
os.system(c)


