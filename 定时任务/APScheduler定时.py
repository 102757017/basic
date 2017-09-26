#-*-coding:utf-8-*-  
from apscheduler.scheduler import Scheduler  
  
def job_function(a):  
    print(a)
  
if __name__ == '__main__':  
    hello = 'hello world'  
    sched = Scheduler(daemonic=False) 
    # 注意这里，要设置 daemonic=False,因为上面的脚本要是没有sched.daemonic=False的话，它会创建一个守护线程。这个过程中，会创建scheduler的实例。但是由于脚本很小，运行速度很快，主线程mainthread会马上结束，而此时定时任务的线程还没来得及执行，就跟随主线程结束而结束了。
    sched.add_cron_job(job_function, day_of_week='mon-fri', hour='*', minute='0-59', second='*/5', args=[hello]) # args=[] 用来给job函数传递参数  
    sched.start()  