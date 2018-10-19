# -*- coding: UTF-8 -*-
from multiprocessing import Pool,Queue
import os, time, random


def long_time_task(name):
    print('运行子进程 %s，子进程PID：%s' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('子进程 %s 运行了 %0.2f 秒' % (name, (end - start)))

    
#windows下必须加if __name__=='__main__':才能正常运行，在ldle下不能运行，必须在cmd下运行
if __name__=='__main__':
    print('父进程PID:',os.getpid())
    p = Pool(4)
    for i in range(5):
        #i为long_time_task的参数
        p.apply_async(long_time_task, [i])
    print('等待所有子进程执行完毕...')
    
    #关闭进程池，不再接受新的进程
    p.close()
    #对Pool对象调用join()方法会等待所有子进程执行完毕，join方法必须在close或terminate之后使用。
    p.join()
    print('所有进程结束')




