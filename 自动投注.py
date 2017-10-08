# -*- coding: UTF-8 -*-
import datetime
from datetime import timedelta
import time
import requests


def delay(t):
    flag=1
    now=time.time()
    deta=0
    while deta<t:
        deta=time.time()-now
        #print(deta)


url = "http://www.yv55.com/uc/GetKJIssue?0.041975538396118006"
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Host': 'www.yv55.com',
         'Origin': 'http://www.yv55.com',
         'Referer': 'http://www.yv55.com/PersonalCenter',
         'X-Requested-With': 'XMLHttpRequest',
         'Content-Type': 'text/html',
         'Connection': 'Keep-Alive',
         'Cache-Control': 'max-age=0',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
         }
headers2={'Accept': 'application/json, text/javascript, */*; q=0.01',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'Connection': 'keep-alive',
 'Content-Length': '52',
 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
 'Cookie': 'safedog-flow-item=; acw_tc=AQAAAEiOGmGTNA4ANsUQG4zEXm/RH0KN; '
           'ASP.NET_SessionId=ey5fss5lxdeo1roptysc2kpu; '
           'login=117309,2017-10-08 20:15:18; si117309=1; '
           'dfw=54awjO1NA5wOthKCv8LDA/ycqv9/p6BiLdLiiVyL0QsPL13pI4bMh/anxSPIxR5Rtg7lU9Y/qJv70RNCULN64CtfREL+Vmp3dQkGeYe68D7ART+6HYIfhPJPNmRUZ1ctBswHBuU5eeEr6AmgPNeigFlJYy3rIwmqoQTi0rtWvzNii/kwFYxoN5NHmzPg3Mbx+f0VLjh23vB28OaenPl3i2N24gPFJeboZ1Zl6J6h4XQDF36jaZVZCxM4tcdgPqnsLKVEhjIjzMhWv3F2Q6OEGaVnT2LHg7ONNie1sKWitiiO8apQeHfh2/e3NnLlL3D+gzsEVxSg33G1yusP1MQyiLxcCxOJVpi9iQtoIY5HqUNETFNkzu6o46WplMqVkQPv1Y4aPV3LnY0TeIdz8BB1E/+TWUsU6GSPE9h/snVF4K2Kfiy/Scwd9PfC5m6QeDpGkKtydArrj6+HO0j+rh0dywQdaa6xSN927MkDzFbUPg2ZXf4mqUiKXjngiKaEDHXLRqUoYnedNPCfIlNME7ZInAn+2f/dr7tBCPtnnOQWPYZDeUJ7QW8JQIRS2TrOXTp5fz0M/D7oabiZvw4HYBLUMO6SaERq3DIot2Kfdw3uSVsUPolHKGvvRGTRBibLM4mAqTlBGt80xT/g9LL1P1L0C+xvEfmnw8E405Vt5virQw2jCbWt1tccnbYATX5WyxuDElsykTNHqsv1RI2KJKEZUTWwak/pTEF7xfhKNJyGTmLDvgubLMmLnKGtf5ff8abcf1926c3b90c39bd0b639f17ae',
 'Host': 'www.yv55.com',
 'Origin': 'http://www.yv55.com',
 'Referer': 'http://www.yv55.com/PersonalCenter',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
               'like Gecko) Chrome/60.0.3112.113 Safari/537.36',
 'X-Requested-With': 'XMLHttpRequest'}



url2="http://www.yv55.com/uc/GetAllBet?0.4610653719152149"
url3="http://www.yv55.com/uc/SubmitBet?0.7372482543845444"
post_body="issueNum=201710081215&hongtl=100&DFW=0&huitl=0&myy=0"


def checktime():
    r=requests.post(url,headers=headers)
    try:
        result = r.json()
    except BaseException as e:
        print(r.text)
    a=result['list']
    b=result['nTime']
    a4=a['IssueNum']
    return b,a4

def getbat():
    r=requests.post(url2,headers=headers)
    try:
        result = r.json()
    except BaseException as e:
        print(r.text)
    a=result['list']
    a1=a['DFW']
    a2=a['hongtl']
    data=a1-a2
    print('正向筹码',a1)
    print('反向筹码',a2)
    return data

def bat():
    print('下注')
    r=requests.post(url3,headers=headers2,data=post_body)
    try:
        result = r.json()
    except BaseException as e:
        print(r.text)
    d=result['msg']
    print(d)
        
b=checktime()
IssueNum=str(int(b[1])+1)
post_body="issueNum="+IssueNum+"&hongtl=100&DFW=0&huitl=0&myy=0"

while 1:
    if b[0]>39000:
        dt=(b[0]-39000)/1000
        IssueNum=str(int(b[1])+1)
        post_body="issueNum="+IssueNum+"&hongtl=100&DFW=0&huitl=0&myy=0"        
    else:
        dt=(b[0]+21000)/1000
        post_body="issueNum="+b[1]+"&hongtl=100&DFW=0&huitl=0&myy=0"
    print("wait:",dt)
    time.sleep(dt)
    try:
        c=getbat()
        print('筹码差额',c/100000000)
        if c>-130000000 and c<-75000000:
            bat()
        b=checktime()
    except BaseException as e:
        print("产生了错误",e)
        pass
    finally:
        print(b)
