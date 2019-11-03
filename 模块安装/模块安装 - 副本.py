# -*- coding: UTF-8 -*-
import os
import sys


# 获取 系统环境 PATH 的变量
env = os.environ.get("PATH")
s1=sys.prefix
os.environ["PATH"] =env+";"+ s1



a="python -m pip install  pywinauto -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com"
#a="python -m pip install --upgrade pyinstaller -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com"
#a="\""+ sys.prefix + "\python.exe\"" +" -m pip uninstall pydot_ng"
#生成command命令,指定安装源为阿里云
print("command命令是："+ a)
os.system(a) #执行command

