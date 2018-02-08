# -*- coding: UTF-8 -*-
import time, threading

def child(n):
    print("我是子线程",n)

t1 = threading.Thread(target=child, args=("a",))
t2 = threading.Thread(target=child, args=("b",))
t1.start()
t2.start()
t1.join()
t2.join()


#多线程同时修改某个变量时，为了防止冲突，一定要给该变量加锁，否则会导致变量计算错误。
def change():
    global i
    lock.acquire()# 先要获取锁:
    i=i+2
    lock.release()# 改完了一定要释放锁:

i=0
lock = threading.Lock()
t1 = threading.Thread(target=change, args=())
t2 = threading.Thread(target=change, args=())
t1.start()
t2.start()
t1.join()
t2.join()
print(i)
