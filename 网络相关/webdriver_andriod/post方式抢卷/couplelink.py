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
        #result1 = re.findall('"val":([^:]{0,5}),"scope":([^:]{0,50}),.{10,100}?"limit":([^:]*),.{0,50}?"picture":"([^:]*),.{0,50}?"scene":([^:]*),"args":([^:]*),',r.text)
        val = re.findall('"val":([^:]{0,10}),',r.text)
        scope = re.findall('"scope":([^:]{0,50}),',r.text)
        limit = re.findall('"limit":([^:]*),',r.text)
        picture = re.findall('"picture":"([^:]*),',r.text)
        scene = re.findall('"scene":([^:]*),',r.text)
        args = re.findall('"args":([^:]*),',r.text)
        result2=re.findall('"encodeActivityId":(.+?),',r.text)
        

        if len(val)==len(scope) and len(val)==len(limit) and len(val)==len(picture) and len(val)==len(scene) and len(val)==len(args) and len(val)!=0:
                for x in range(len(val)):
                    pictrueurl="\"http:"+picture[x]#优惠券图片
                    body="body={\"activityId\":"+ result2[0] +",\"scene\":"+ scene[x] +",\"args\":"+ args[x] +",\"mitemAddrId\":\"\",\"geo\":{\"lng\":\"\",\"lat\":\"\"}}"        
                    link="https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&"+body+"&client=wh5&clientVersion=1.0.0"#领卷链接
                    link=urllib.parse.quote(link,safe='/:?=&')   
                    href.append([val[x],scope[x],limit[x],pictrueurl,link,Referer])

        if href:    
            pprint.pprint(href)            
        a=open(os.path.join(os.path.dirname(__file__),"couplelink.txt"),'w')
        a.write(Referer)
        a.write("\n")
        for y in href:
            a.write(str(y))
            a.write("\n")
        a.close()
                           
    except BaseException as e:
        print('获取网页源码出错:',Referer, e)
        pass
    
    return href



#Referer为领卷页面
#Referer="https://pro.m.jd.com/mall/active/2i1YcEh4r9LhxVeQai9BfuLqMaL7/index.html"
#b=makeurl(Referer)
