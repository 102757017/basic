# -*- coding: UTF-8 -*-
from multiprocessing import Pool,Queue
import os, time, random

i=Queue()
i.put(0)
def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    print("count"+i.get(True))
    i.put(i.get(True)+1)
    
#windows下必须加if __name__=='__main__':才能正常运行，在ldle下不能运行，必须在cmd下运行
if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')


