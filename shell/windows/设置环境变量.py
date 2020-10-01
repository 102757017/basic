# -*- coding: UTF-8 -*-
import os
import pprint
import sys
import subprocess

#新增的系统变量使用下面的方法获取不到，关机重启即可
#修改的环境变量是临时改变的，当程序停止时修改的环境变量失效（系统变量不会改变）
# 获取 系统环境 PATH 的变量
env = os.environ.get("PATH")
s1=sys.prefix

# 定义环境变量
os.environ["PATH"] =env+";"+ s1
pprint.pprint(os.environ.get("PATH"))

a="python"
print("command命令是：",a)


status = subprocess.run(a,shell=True, capture_output=True,text=True )
print(status.stdout)
print(status.stderr)
