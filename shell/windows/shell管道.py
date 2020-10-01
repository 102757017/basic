# -*- coding: UTF-8 -*-
import os
import sys
import subprocess



#非阻塞模式
os.popen("notepad")
print("执行完毕")


#会阻塞程序继续运行
#执行单个命令不能使用["notepad"]，需要使用"notepad"
status = subprocess.run(["notepad"],shell=True, capture_output=True,text=True )
print(status.stdout)
print(status.stderr)
print("执行完毕")
