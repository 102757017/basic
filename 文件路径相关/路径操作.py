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
a = __file__
print(a)
print('\n')

#  所有基于模块的使用到__file__属性的代码，在源码运行时表示的是当前脚本的绝对路径，但是用pyinstaller打包后就是当前模块的模块名（即文件名xxx.py）
#  因此需要用以下代码来获取exe的绝对路径
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
print(bundle_dir)


print('当前脚本所在的目录：')
a = os.path.dirname(a)
print(a)
print('\n')

print('上级目录：')
a = os.path.dirname(a)
print(a)
print('\n')

print('用os.path.join构造路径:')
a = os.path.join(a, 'xxx', "yyy")
print(a)
print('\n')

print('用os.path.sep构造路径:')
a = os.path.sep.join([a, 'aaa', "bbb"])
print(a)
print('\n')


print("当前脚本工作的目录路径:")
path1 = os.getcwd()
print(path1)
print('\n')

print("切换工作目录")
os.chdir(sys.path[0])
print("当前脚本工作的目录路径:")
path1 = os.getcwd()
print(path1)
print('\n')

if os.path.exists(sys.path[0]+os.path.sep+'temp'):
    #修改文件夹的名称
    os.rename(sys.path[0]+os.path.sep+'temp',sys.path[0]+os.path.sep+'temp2')
    shutil.rmtree(sys.path[0]+os.path.sep+'temp2')

print("在当前文件夹内创建temp目录:")
path = sys.path[0]+os.path.sep+'temp'
os.mkdir(path)
print('\n')


print("python的环境变量目录:")
path = sys.path
print(path)
print('\n')

print("python的安装目录:")
path = sys.prefix
print(path)
print('\n')


print("pythonw.exe的路径(当前Python解释器):")
path = sys.executable
print(path)
print('\n')


print("dir获取python安装目录下文件命令:")
list1 = os.listdir(sys.prefix)
print(list1)
print('\n')


print("在D盘创建log.txt的空文件:")
open("D:\log.txt", "w+").close()
print('\n')

print("复制log.txt:")
shutil.copy("D:\log.txt", "log.txt")
print('\n')

print("判断log.txt文件是否存在:")
result = os.path.isfile("D:\log.txt")
print(result)
print('\n')

print("删除D盘的log.txt:")
os.remove("D:\log.txt")
print('\n')

print("创建文件夹test:")
os.mkdir("test")
print('\n')

print("复制文件夹test为test2:")
shutil.copytree("test", "test2")
print('\n')


print("判断test文件夹是否存在:")
result = os.path.isdir("test")
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
print('\n')

print("遍历指定目录下所有的文件和文件夹，返回所有文件夹名词，不包括子目录内的")
files = os.listdir(sys.path[0])
for x in files:
    if os.path.isdir(sys.path[0]+os.path.sep+ x):
        print(x)
print('\n')

print("遍历指定目录下所有的文件和文件夹，返回所有文件名称，不包括子目录内的")
files = os.listdir(sys.path[0])
for x in files:
    if os.path.isfile(sys.path[0]+os.path.sep+ x):
        # 分离文件名与扩展名，仅显示txt后缀的文件
        if os.path.splitext(x)[1]=='.txt':
            print(x)
print('\n')

print("导入自定义模块:")
sys.path.append(r'H:\学习资料\编程学习\pathon\基础操作\basic\文件读写')
import 读写txt