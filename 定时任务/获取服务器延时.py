# -*- coding: UTF-8 -*-
from urllib import request   #导入request库中的urllib函数
import urllib
import re          #导入正则表达式库
import time        #导入延时函数库
import http.client
import datetime
import os





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

a=GetDelayTime()
print(a)

      
    


