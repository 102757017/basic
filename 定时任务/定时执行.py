# -*- coding: UTF-8 -*-
import datetime
import time
import sched #定时任务模块



def mission():
        print('开始执行代码')


#时间格式转换函数，参数time的类型为字符串，格式为"09:59:00:000000"
def timech(time):
        s=time.split(":")
        b=[]
        for x in s:
                b.append(int(x))
        now = datetime.datetime.now()
        time2=datetime.datetime(now.year,now.month,now.day,b[0],b[1],b[2],b[3])
        return time2

        
        

#定时器函数，到点执行代码，参数time的类型为字符串，格式为"09:59:00:000000"
def timer(time):
        clock=timech(time)
        now = datetime.datetime.now()
        while now<clock:
                now = datetime.datetime.now()           
        print("到达指定时间，开始执行代码")
        mission()
        print("执行完毕")

timer("22:03:00:000001")
