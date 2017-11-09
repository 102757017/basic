# -*- coding: UTF-8 -*-
import datetime
from datetime import timedelta
from time import sleep
import time
import sched #定时任务模块
from urllib import request   #导入request库中的urllib函数
import urllib
import http.client
import os
import sys

sys.path.append(os.path.dirname(__file__))


def GetDelayTime():
    """获取jd服务器时间
    NOTE: 原理是通过服务器头文件响应获取服务器时间
    """
    time1 = datetime.datetime.now()
    conn = http.client.HTTPConnection( 'api.m.jd.com' )
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
        clock=timech(clock)
        now = datetime.datetime.now()
        delta=clock-now
        delta=delta.seconds
        print('延时',delta,'秒')
        sleep(delta)         


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
        return pretime,luck_time




#抢券时间
luck_time=("10:00:00:000000","14:00:00:000000","20:00:00:000000","00:00:00:000000")
#Referer为领卷页面
Referer="https://pro.m.jd.com/mall/active/2swvgWopcM4Xy6hyxuE8toBnSkzV/index.html"
#url为领卷链接
url="http://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%222swvgWopcM4Xy6hyxuE8toBnSkzV%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D1b86ce9ab931422ea7379e2574bbc33c%2CroleId%3D8245464%2Cto%3Dpro.m.jd.com%2Fmall%2Factive%2F2vmBPknBMoauhsFm2Lc7nD5ARg45%2Findex.html%22%2C%22mitemAddrId%22%3A%22%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%7D&client=wh5&clientVersion=1.0.0&sid=99bd1b2f69031dafbaf5cacc4b5a4ad7&uuid=1504359002749618854944&area=&_=1506784781082&callback=jsonp3"


#同步服务器时间
GetJDServerTime()
i=neartime(luck_time)
print(i[0],i[1])
timer2(i[0])
print("到达准备时间，开始获取cookie")
cookie=getcookie(Referer)
print("获取完毕")

timer(i[1])
print("到达抢卷时间，开始执行代码")
grab(cookie,Referer,url)
grab(cookie,Referer,url)
grab(cookie,Referer,url)
print("执行完毕")
