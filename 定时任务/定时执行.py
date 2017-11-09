# -*- coding: UTF-8 -*-
import datetime
import time
from time import sleep
from datetime import timedelta
import sched #定时任务模块
from urllib import request   #导入request库中的urllib函数
import urllib
import http.client
import os




def mission():
        print('开始执行代码')


#时间格式转换函数，参数time的类型为字符串，格式为"09:59:00:000000"
def timech(time):
        if time=="00:00:00:000000":
                now=datetime.datetime.now()+timedelta(days=1)
        else:
                now = datetime.datetime.now()
                
        s=time.split(":")
        b=[]
        for x in s:
                b.append(int(x))       
        time2=datetime.datetime(now.year,now.month,now.day,b[0],b[1],b[2],b[3])
        return time2

        
        

#定时器函数，到点执行代码，参数time的类型为datetime.datetime
def timer(time):
        now = datetime.datetime.now()
        delta=time-now
        delta=delta.seconds
        print('延时',delta,'秒')
        sleep(delta)         
        print("到达指定时间，开始执行代码")
        mission()
        print("执行完毕")


def neartime(luck_times):
        m=[]
        for time in luck_times:
                if timech(time)>datetime.datetime.now():
                        m.append(timech(time)-datetime.datetime.now())
                else:
                        b=timedelta(days=1)
                        m.append(b)
        i=m.index(min(m))
        luck_time=timech(luck_times[i])
        pretime=luck_time-timedelta(minutes=2)
        print('抢卷时间',type(luck_time),luck_time)
        print('准备时间',type(pretime),pretime)
        return pretime,luck_time



#抢券时间
luck_time=("10:00:00:000000","14:00:00:000000","22:00:00:000000","00:00:00:000000")

#获取luck_time中最接近抢券时间的一个
i=neartime(luck_time)

#执行定时任务
timer(i[0])

           
