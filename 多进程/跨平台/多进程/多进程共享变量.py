# -*- coding: UTF-8 -*-
from multiprocessing import Process,Manager
from ctypes import c_char_p
import time


def run_proc1(flag):
    flag[0] = 1
    time.sleep(0.1)
    

def run_proc2(flag):
    flag[0] = 2
    time.sleep(0.1)


if __name__=='__main__':
    #Manager()返回的manager对象控制了一个server进程，此进程包含的python对象可以被其他的进程通过proxies来访问。
    #从而达到多进程间数据通信且安全。
    #Manager支持的类型有list,dict,Namespace,Lock,RLock,Semaphore,BoundedSemaphore,Condition,Event,Queue,Value和Array。 
    flag = Manager().list()
    flag.append(3)

    p1 = Process(target=run_proc1, args=(flag,))
    p1.start()
    p1.join()
    print(flag[0])

    p2 = Process(target=run_proc2, args=(flag,))
    p2.start()
    p2.join()
    print(flag[0])

