# -*- coding: UTF-8 -*-
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print(name)

#windows下必须加if __name__=='__main__':才能正常运行，在ldle下不能运行，必须在cmd下运行

for i in range(5):
    if __name__=='__main__':
        p = Process(target=run_proc, args=(i,))
        p.start()


