# -*- coding: UTF-8 -*-
import os
import time
import pprint
import requests
import urllib
import re
import chardet
import pprint

from couplelink import makeurl


#获取页面上所有的url
def GetAllUrl():
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
         'Host': "m.jd.com",
         'Connection': 'Keep-Alive',
         'Accept-Language': 'zh-CN,zh;q=0.8',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept': '*/*'
         }
    result1=[]
    try:
        r=requests.get("https://m.jd.com/",headers=headers)
        result1 = re.findall('"(https?://[^ ]*?)"',r.text)
        result2=[]
        for index,url in enumerate(result1):
            if url[-3:]!='jpg' and url[-3:]!='png':
                result2.append(url)
            
        print("首页链接个数:",len(result2))
        return result2
    except BaseException as e:
        print('获取网页源码出错:', e)


