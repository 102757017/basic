# -*- coding: UTF-8 -*-
import datetime
from datetime import timedelta
import time
import sched #定时任务模块
from urllib import request   #导入request库中的urllib函数
import urllib
import http.client
import os
import sys

sys.path.append(os.path.dirname(__file__))
from jd import login
from jd import pre
from jd import grab

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
    t=time2-time1
    
    return t


            
#时间格式转换函数，输出datetime.datetime，参数time的类型为字符串，格式为"09:59:00:000000"，
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
def timer(clock):
        now = datetime.datetime.now()
        a=timedelta(minutes=0)
        while now+a<clock:
                try:
                    a=GetDelayTime()
                except BaseException as e:
                    print('获取服务器延时失败:', e)
                now = datetime.datetime.now()
                #print(now)

def timer2(clock):
        now = datetime.datetime.now()
        while now<clock:
                now = datetime.datetime.now()
                #print(now)


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
        pretime=luck_time-timedelta(minutes=1)
        return pretime,luck_time



#同步服务器时间
GetJDServerTime()
#抢券时间
luck_time=("10:00:00:000000","14:00:00:000000","20:00:00:000000","00:00:00:000000")
i=neartime(luck_time)
print(i[0],i[1])
timer(i[0])
print("到达准备时间，开始执行代码")
browser=pre()
print("执行完毕")
timer(i[1])
print("到达抢卷时间，开始执行代码")
grab(browser)
print("执行完毕")
