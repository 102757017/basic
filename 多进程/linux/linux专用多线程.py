# -*- coding: UTF-8 -*-
import os

for x in range(5):
    pid = os.fork()
    if pid == 0 :#创建子进程
        print(x)
        a=x+1#变量a在多个子进程内不共用
        print(x,a)
        os._exit(0) #结束子进程
    
        
