# -*- coding: UTF-8 -*-
import os

print('父进程step1')#父进程
'''fork()是一个很特殊的方法,一次调用,它会返回2个值,
一个值为0,表示在子进程返回;另外一个值为非0,表示在父进程中返回子进程ID
'''
pid = os.fork()
print('同时执行父进程step2，子进程step1，共执行两次')
if pid == 0 :#子进程
    print('子进程step2')
    os._exit(0) #结束子进程

else:#父进程
    print('父进程step3')
print("父进程step4")
