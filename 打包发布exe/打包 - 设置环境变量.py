# -*- coding: UTF-8 -*-
import os
import sys
from subprocess import run
import pprint


#在64位系统下打包的程序只能在64位系统上运行
#pyinstaller也是有版本的，所以对于一些库的新版本是不支持的。 requests的版本只支持到 2.10.0
os.chdir(os.path.dirname(__file__))

env = os.environ.get("PATH")
s1=sys.prefix
s2=os.path.join(sys.prefix,"Scripts")

# 定义环境变量
os.environ["PATH"] =env+";"+ s1+";"+s2
pprint.pprint(os.environ.get("PATH"))


a="pyinstaller hello.py"
#生成command命令
print("command命令是：",a)

status = run(a,shell=True ,capture_output=True,text=True )
print(status.stdout)
print(status.stderr)


