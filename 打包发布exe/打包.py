# -*- coding: UTF-8 -*-
import os
import sys
import subprocess


#在64位系统下打包的程序只能在64位系统上运行
#pyinstaller也是有版本的，所以对于一些库的新版本是不支持的。 requests的版本只支持到 2.10.0

os.chdir(os.path.dirname(__file__))

d1=os.path.join(sys.prefix,"python.exe")
d2=os.path.join(sys.prefix,"Scripts","pyinstaller.exe")

a="\""+ d1  + "\" "+ "\""+ d2  + "\" "+"hello.py"
#生成command命令
print("command命令是：",a)

pipe = subprocess.Popen(a, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True).stdout  
print(pipe.read())  


