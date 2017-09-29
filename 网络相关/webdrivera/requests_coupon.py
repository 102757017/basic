# -*- coding: UTF-8 -*-
import re          #导入正则表达式库
import time        #导入延时函数库
#import androidhelper  #导入安卓API库
import chardet
import requests
import sqlite3


def post(url,ck):
    url = url
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
             'Host': 'coupon.m.jd.com',
             'Content-Type': 'text/html',
             'Connection': 'Keep-Alive',
             'Cache-Control': 'max-age=0',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'Cookie':ck
             }
    try:
        r=requests.get(url,headers=headers)
        a=r.text
        print(a)
    except BaseException as e:
        print('产生了错误,跳过错误:', e)
        pass
    return


      
a = "https://coupon.m.jd.com/center/getCouponCenter.action"
b=""

post(a,b)


