# -*- coding: UTF-8 -*-
import os
import sys
import subprocess


#在64位系统下打包的程序只能在64位系统上运行


sys.path.append(os.path.dirname(__file__))
a="\""+ sys.prefix + "\python.exe\" "  + "\""+ sys.prefix + "\Scripts\pyinstaller.exe\" " +os.path.dirname(__file__)+"\hello.py"+" --distpath="+os.path.dirname(__file__)

#生成command命令,指定安装源为阿里云
print("command命令是："+ a)

pipe = subprocess.Popen(a, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True).stdout  
print(pipe.read())  


