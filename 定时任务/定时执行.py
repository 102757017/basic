# -*- coding: UTF-8 -*-
import datetime
import time
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

        
        

#定时器函数，到点执行代码，参数time的类型为字符串，格式为"09:59:00:000000"
def timer(time):
        clock=timech(time)
        now = datetime.datetime.now()
        while now<clock:
                now = datetime.datetime.now()           
        print("到达指定时间，开始执行代码")
        mission()
        print("执行完毕")


def neartime(luck_time):
        m=[]
        for time in luck_time:
                if timech(time)>datetime.datetime.now():
                        m.append(timech(time)-datetime.datetime.now())
                else:
                        b=timedelta(days=1)
                        m.append(b)
        return m.index(min(m))



#抢券时间
luck_time=("10:00:00:000000","14:00:00:000000","17:00:00:000000","00:00:00:000000")

#获取luck_time中最接近抢券时间的一个
i=neartime(luck_time)

#执行定时任务
timer(luck_time[i])

           
