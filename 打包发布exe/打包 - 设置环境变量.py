# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
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

os.system(a)
#pipe = subprocess.Popen(a, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True).stdout
#print(pipe.read())


