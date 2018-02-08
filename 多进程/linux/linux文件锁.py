# -*- coding: UTF-8 -*-
import fcntl
import time  
  
fp = open('hello.txt','w')  
#排他锁,文件加锁后其它进程就不能再次对该文件加锁，该进行会被阻塞，但不会退出
fcntl.flock(fp, fcntl.LOCK_EX)  
print('文件锁开始执行')
time.sleep(10)
#解锁
fcntl.flock(fp, fcntl.LOCK_UN)
print('文件锁已解除')
fp.close()  
