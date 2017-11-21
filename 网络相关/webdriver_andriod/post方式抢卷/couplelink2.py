# -*- coding: UTF-8 -*-
import os
import time
import pprint
import requests
import urllib
import re
import chardet


#获取页面上所有的领卷链接
def makeurl(Referer):
    host=Referer.split("/")[2]
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
         'Host': host,
         'Connection': 'Keep-Alive',
         'Accept-Language': 'zh-CN,zh;q=0.8',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept': '*/*',
         'Referer': Referer
         }
    href=[]
    try:
        print("正在获取网页")
        r=requests.get(Referer,headers=headers)
        print("获取完毕，开始正则解析")
        result1 = re.findall('href="(//coupon.m.jd.com/coupons/show.action\?key&[^: ]{0,200}?)"[\s\S]{0,1000}?data-src="(.{0,200}?)">',r.text)
        for x in result1:
                    pictrueurl="\"http:"+x[1]#优惠券图片   
                    link="\"http:"+x[0]#领卷链接
                    href.append(['val','scope','limit',pictrueurl,link])

        if href:    
            pprint.pprint(href)            
                           
    except BaseException as e:
        print('获取网页源码出错:',Referer, e)
        pass
    
    return href



#Referer为领卷页面
#Referer="https://pro.m.jd.com/mall/active/2i1YcEh4r9LhxVeQai9BfuLqMaL7/index.html"
#b=makeurl(Referer)
