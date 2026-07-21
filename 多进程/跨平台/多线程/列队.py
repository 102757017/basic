# -*- coding: UTF-8 -*-
import threading
import queue
import time

# 创建先进先出队列，最大容量为10
q = queue.Queue(maxsize=10)
#q = queue.LifoQueue()     #先进后出
#q = queue.PriorityQueue() #按优先级处理

'''
队列内部维护一个计数器（未完成任务数）：
1. 每次调用 put()：计数器 +1
2. 每次调用 task_done()：计数器 -1
3. 当计数器为 0 时，q.join() 解除阻塞
'''

def producer():
    """生产者：向队列中放入数据"""
    for i in range(5):
        time.sleep(0.1)
        q.put(i)  # 如果队列满了，会阻塞
        print(f"生产: {i}")
    q.put(None)  # 发送结束信号

def consumer():
    """消费者：从队列中取出数据"""
    while True:
        if not q.empty():  # 检查是否为空
            item = q.get(timeout=0.1)    # 如果队列为空，会阻塞
            if item is None:             # 收到结束信号
                q.task_done()
                break
            print(f"消费: {item}")
            q.task_done()  # 标记任务完成
    else:
        print("队列为空，不阻塞")

''' 
try:
    item = q.get_nowait()  #立即返回，不阻塞，没有则抛异常
except queue.Empty:        # 捕获这个异常
    print("队列为空！")

q.queue.clear() - 清空队列
''' 

# 创建并启动线程
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
t1.join() # 阻塞当前线程，直到被调用的线程执行完毕才继续执行
t2.join()
