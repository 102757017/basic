# -*- coding: UTF-8 -*-
from urllib import request   #导入request库中的urllib函数
import urllib
import time        #导入延时函数库
import http.client
import datetime
import os





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


GetJDServerTime()


      
    


