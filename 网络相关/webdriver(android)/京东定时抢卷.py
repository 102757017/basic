# -*- coding: UTF-8 -*-
import datetime
from datetime import timedelta
import time
import sched #定时任务模块
from urllib import request   #导入request库中的urllib函数
import urllib
import http.client
import os


def GetJDServerTime():
    """获取jd服务器时间
    NOTE: 原理是通过服务器头文件响应获取服务器时间
    """
    
    conn = http.client.HTTPConnection( 'miaosha.jd.com' )
    conn.request( 'GET', '/' )
    response = conn.getresponse()
    ts =  response.getheader('Date')
    ltime = time.strptime( ts[5:25], '%d %b %Y %H:%M:%S' )
    ttime=time.localtime(time.mktime(ltime)+8*60*60)    
    dat="date %u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    tm="time %02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    os.system(dat)
    os.system(tm)
    time_now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print("修正完了，当前系统时间:"+time_now)
        #按照特定时间格式将字符串转换为时间类型
    
    return time_now


def GetDelayTime():
    """获取jd服务器时间
    NOTE: 原理是通过服务器头文件响应获取服务器时间
    """
    time1 = datetime.datetime.now()
    conn = http.client.HTTPConnection( 'miaosha.jd.com' )
    conn.request( 'GET', '/' )
    response = conn.getresponse()
    ts =  response.getheader('Date')
    time2 = datetime.datetime.now()
    
    return time2-time1


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



#同步服务器时间
#GetJDServerTime()
#抢券时间
luck_time=("10:00:00:000000","14:00:00:000000","17:00:00:000000","00:00:00:000000")
i=neartime(luck_time)
timer(luck_time[i])

           
