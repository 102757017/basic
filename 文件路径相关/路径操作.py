#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import shutil
from pathlib import Path


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
if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
    os.environ["WICO_ROOT"] = sys._MEIPASS
else:
    os.environ["WICO_ROOT"] = str(Path(__file__).parent)
KV_DIR = f"{os.environ['WICO_ROOT']}"
print(KV_DIR)


print('当前脚本所在的目录：')
a = Path(__file__).parent
print(a)
print('\n')

print('上级目录：')
a = Path(a).parent
print(a)
print('\n')

print('构造路径:')
a=a/"xxx"/"yyy"

print(a)
print('\n')


print("当前脚本工作的目录路径:")
path1 = Path.cwd()
print(path1)
print('\n')

print("切换工作目录")
os.chdir(sys.path[0])
print("当前脚本工作的目录路径:")
path1 = Path.cwd()
print(path1)
print('\n')

root=Path(sys.path[0])

if Path.exists(root/'temp'):
    #修改文件夹的名称
    Path.rename(root/'temp',root/'temp2')
    shutil.rmtree(sys.path[0]+os.path.sep+'temp2')

print("在当前文件夹内创建temp目录:")
path = root/'temp'
Path.mkdir(path)
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


print("在本目录创建log.txt的空文件:")
open(root/"log.txt", "w+").close()
print('\n')

print("复制log.txt:")
shutil.copy(root/"log.txt", "log2.txt")
print('\n')

print("判断log.txt文件是否存在:")
result = Path.is_file(root/"log.txt")
print(result)
print('\n')

print("删除本目录的log.txt:")
os.unlink(root/"log.txt")
print('\n')

print("创建文件夹test:")
Path.mkdir(root/"test")
print('\n')

print("复制文件夹test为test2:")
shutil.copytree("test", "test2")
print('\n')


print("判断test文件夹是否存在:")
result = Path.is_dir(root/"test")
print(result)
print('\n')


print("删除test和test2文件夹:")
shutil.rmtree(root/"test")
shutil.rmtree(root/"test2")
print('\n')


print("遍历指定目录下所有的文件和文件夹，包括子目录内的")
list_dirs = root.rglob('*')
for files in list_dirs:
    print(files)
print('\n')



print("遍历指定目录下所有的文件和文件夹，返回所有文件夹名词，不包括子目录内的")
list_dirs = root.glob('*')
for files in list_dirs:
    print(files)
print('\n')


print("遍历所有txt文件，使用正则进行匹配")
list_dirs = root.rglob('*.txt')
for files in list_dirs:
    print(files)
print('\n')


print("导入自定义模块:")
root = Path.cwd()
sys.path.append(str(root.parent/"文件读写"))
import 读写txt
