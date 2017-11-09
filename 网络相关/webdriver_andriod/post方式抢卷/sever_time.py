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


def GetJDServerTime():
    """获取jd服务器时间
    NOTE: 原理是通过服务器头文件响应获取服务器时间
    """
    flag=1
    i=0
    conn = http.client.HTTPConnection( 'api.m.jd.com' )
    conn.request( 'GET', '/' )
    response = conn.getresponse()
    ts2 =  response.getheader('Date')
    while flag:
        #conn = http.client.HTTPConnection( 'miaosha.jd.com' )
        conn = http.client.HTTPConnection( 'api.m.jd.com' )
        conn.request( 'GET', '/' )
        response = conn.getresponse()
        ts =  response.getheader('Date')
        i=i+1
        if ts!=ts2:
            flag=0      
        #按照特定时间格式将字符串转换为时间类型
    ltime = time.strptime( ts[5:25], '%d %b %Y %H:%M:%S' )#非夏令时时间数组
    ttime=time.localtime(time.mktime(ltime)+8*60*60)#夏令时时间数组
    dtime = datetime.datetime.fromtimestamp(time.mktime(ltime)+8*60*60)#夏令时时间类型
    return dtime


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

print(GetJDServerTime())
print(datetime.datetime.now())
print(GetJDServerTime()>datetime.datetime.now())
