#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import django



#运行mysite目录下的开发服务器
c1='cmd /k & '
c2='F: & '
c3=r'cd F:\学习资料\编程学习\pathon\django\mysite & '
c4="\"E:\Program Files\WinPython-64bit-3.6.1.0Qt5\python-3.6.1.amd64\python.exe\" manage.py runserver"
c=c1+c2+c3+c4
print(c)
os.system(c)

'''
现在用网页浏览器访问 http://127.0.0.1:8000/ 。
应该可以看到一个令人赏心悦目的淡蓝色Django欢迎页面。 它开始工作了。
'''
