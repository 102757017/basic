# -*- coding: UTF-8 -*-
import os
import time
import pprint
from selenium import webdriver
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
    try:
        r=requests.get(Referer,headers=headers)
    except BaseException as e:
        print('获取网页源码出错:', e)
    result1 = re.findall('"limit":([^:]*),.+?"scene":([^:]*),"args":([^:]*),',r.text)
    result2=re.findall('"encodeActivityId":(.+?),',r.text)
    href=[]
    for x in result1:
        body="body={\"activityId\":"+ result2[0] +",\"scene\":"+ x[1] +",\"args\":"+ x[2] +",\"mitemAddrId\":\"\",\"geo\":{\"lng\":\"\",\"lat\":\"\"}}"        
        link="https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&"+body+"&client=wh5&clientVersion=1.0.0"
        link=urllib.parse.quote(link,safe='/:?=&')
        title=x[0]
        href.append([title,link])

    '''    
    body={"activityId":"2swvgWopcM4Xy6hyxuE8toBnSkzV",
          "scene":"1",
          "args":"key=c817ac797dec4060a3b748d51092ad34,roleId=8245445,to=pro.m.jd.com/mall/active/2vmBPknBMoauhsFm2Lc7nD5ARg45/index.html",
          "mitemAddrId":"",
          "geo":{"lng":"","lat":""}}
    '''
    pprint.pprint(href)
    a=open(os.path.join(os.path.dirname(__file__),"couplelink.txt"),'w')
    a.write(Referer)
    a.write("\n")
    for y in href:
        a.write(str(y))
        a.write("\n")
    a.close()
    return(href)



#Referer为领卷页面
Referer="https://pro.m.jd.com/mall/active/4BdWMpAcyW3rdo3Zf4VfSJj8uDH/index.html"
makeurl(Referer)
