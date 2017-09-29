#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import shutil

print("当前操作系统的路径分隔符为:")
print(os.path.sep)
print('\n')

print('\n')
print('当前脚本的绝对路径：')
a=__file__
print(a)
print('\n')

print('当前脚本所在的目录：')
a=os.path.dirname(a)
print(a)
print('\n')

print('上级目录：')
a=os.path.dirname(a)
print(a)
print('\n')

print('用os.path.join构造路径:')
a=os.path.join(a,'xxx',"yyy")
print(a)
print('\n')

print('用os.path.sep构造路径:')
a=os.path.sep.join([a,'aaa',"bbb"])
print(a)
print('\n')


print("当前脚本工作的目录路径:")
path1=os.getcwd()
print(path1)
print('\n')

print("切换工作目录")
os.chdir(sys.path[0])
print("当前脚本工作的目录路径:")
path1=os.getcwd()
print(path1)
print('\n')

if os.path.exists(sys.path[0]+os.path.sep+'temp'):
    shutil.rmtree(sys.path[0]+os.path.sep+'temp')

print("在当前文件夹内创建temp目录:")
path=sys.path[0]+os.path.sep+'temp'
os.mkdir(path)
print('\n')


print("python的环境变量目录:")
path=sys.path
print(path)
print('\n')

print("python的安装目录:")
path=sys.prefix
print(path)
print('\n')


print("pythonw.exe的路径(当前Python解释器):")
path=sys.executable
print(path)
print('\n')


print("dir获取python安装目录下文件命令:")
list1=os.listdir(sys.prefix)
print(list1)
print('\n')


print("在D盘创建log.txt的空文件:")
open("D:\log.txt","w+").close()
print('\n')

print("复制log.txt:")
shutil.copy("D:\log.txt","log.txt")
print('\n')

print("判断log.txt文件是否存在:")
result=os.path.isfile("D:\log.txt")
print(result)
print('\n')

print("删除D盘的log.txt:")
os.remove("D:\log.txt")
print('\n')

print("创建文件夹test:")
os.mkdir("test")
print('\n')

print("复制文件夹test为test2:")
shutil.copytree("test","test2")
print('\n')


print("判断test文件夹是否存在:")
result=os.path.isdir("test")
print(result)
print('\n')


print("删除test和test2文件夹:")
shutil.rmtree("test")
shutil.rmtree("test2")
print('\n')


print("遍历指定目录下所有的文件和文件夹，包括子目录内的")
list_dirs = os.walk(sys.path[0]) 
for root, dirs, files in list_dirs: 
    for d in dirs: 
        print(os.path.join(root, d))
    for f in files: 
        print(os.path.join(root, f))


print("导入自定义模块:")
sys.path.append('F:\学习资料\编程学习\pathon\文件读写')
import 读写txt
