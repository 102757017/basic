# -*- coding: UTF-8 -*-
import os
import sys

#升级setuptools与pip
os.system('''"D:\Program Files\WinPython-64bit-3.6.1.0Qt5\python-3.6.1.amd64\python.exe" -m pip install --upgrade setuptools pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com''')


a="\""+ sys.prefix + "\python.exe\"" +" -m pip list"
#生成command命令,指定安装源为阿里云
print("command命令是："+ a)
os.system(a) #执行command
