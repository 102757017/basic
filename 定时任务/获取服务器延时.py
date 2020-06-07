# -*- coding: UTF-8 -*-
from urllib import request  # 导入request库中的urllib函数
import urllib
import re  # 导入正则表达式库
import time  # 导入延时函数库
import http.client
import datetime
import os
import requests


def GetDelayTime():
    """获取jd服务器时间
    NOTE: 原理是通过服务器头文件响应获取服务器时间
    """
    time1 = datetime.datetime.now()
    #conn = http.client.HTTPConnection( 'miaosha.jd.com' )
    conn = http.client.HTTPConnection('api.m.jd.com')
    conn.request('GET', '/')
    response = conn.getresponse()
    ts = response.getheader('Date')
    time2 = datetime.datetime.now()

    return time2-time1


def GetDelayTime2():
    url = "http://api.m.jd.com/"
    headers = {"Host": "api.m.jd.com",
               "Cache-Control": "max-age=0",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
               "Connection": "keep-alive"}
    local_time = time.time()
    r = requests.session()
    rs = r.get(url,
               headers=headers,
               # cookies=CookieJar,
               verify=False,
               allow_redirects=False,
               timeout=(3, 7),
               # proxies=proxies
               )
    server_time=float(rs.headers["X-API-Request-Id"][-13:])/1000
    delay=server_time-local_time
    print(delay)
    return delay



GetDelayTime2()