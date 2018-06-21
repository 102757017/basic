# -*- coding: UTF-8 -*-
import os
import sys

os.chdir(sys.path[0])
#a="\""+ sys.prefix + "\Scripts\pyinstaller.exe\"" +" hello.py"
a="\""+ sys.prefix + "\python.exe\""  + "\""+ sys.prefix + "\Scripts\pyinstaller.exe\"" +" hello.py"

#生成command命令,指定安装源为阿里云
print("command命令是："+ a)
os.system(a) #执行command

'''
"G:\Program Files\WinPython-64bit-3.6.1.0Qt5\python-3.6.1.amd64\python.exe" "G:\Program Files\WinPython-64bit-3.6.1.0Qt5\python-3.6.1.amd64\Scripts\pyinstaller.exe" "H:\学习资料\编程学习\pathon\基础操作\basic\打包发布exe\hello.py"
'''
