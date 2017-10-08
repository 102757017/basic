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
 'Content-Length': '0',
 'Cookie': 'safedog-flow-item=; acw_tc=AQAAAGgmjiZEagEANsUQG7ADO+hDMTt4; '
           'ASP.NET_SessionId=0drlfv54gcfu5m5fimroviin; '
           'login=117309,2017-10-08 14:41:10; '
           'dfw=54awjO1NA5wOthKCv8LDA/ycqv9/p6BiLdLiiVyL0QsPL13pI4bMh/anxSPIxR5Rtg7lU9Y/qJv70RNCULN64CtfREL+Vmp3dQkGeYe68D7ART+6HYIfhPJPNmRUZ1ctBswHBuU5eeEr6AmgPNeigFlJYy3rIwmqoQTi0rtWvzNii/kwFYxoN5NHmzPg3Mbx+f0VLjh23vB28OaenPl3i2N24gPFJeboZ1Zl6J6h4XQDF36jaZVZCxM4tcdgPqnsLKVEhjIjzMhWv3F2Q6OEGaVnT2LHg7ONNie1sKWitiiO8apQeHfh2/e3NnLlL3D+zFwpIOw15dberIYrzNuMUZTSP12AxCKSFOb3+OKwe4s4MWvkW3iBL2Av+iJk98iKeqSnOq83QWPv3NcJVBAnRHnvLTBTfrYm3+RlWbuYzV87vhgrqM8ovcd0iOCbY/PAE/horQvBrL05hHHkTva/RbAqTZ4GpX0c+C23xJg7cBHlR05Q7AOwCFKR6pY7cDUx955wZqIJWYwjkYzJjTGSXSLaIkd3CcPddJzrJXSNrw9Jp//odnmCYYo001inya/emyEwPZyC2snBfw4YQDiv9P5YPKHN8w5376wBsNRyuM5j/n9DdxHI/TuXnKfOqywIG2T2nJwCP1lwmZTIVCynt2Y7TaUS4TImK8wStHvWLXjH+3STZ4xZz1nYy0IafP4TtvVBrhe7rn7kz5Crv3mUBtESwuNzxo03xfhKNJyGTmLDvgubLMmLnKGtf4060767a451bc2b391b7568640b83dc0; '
           'si117309=1',
 'Host': 'www.yv55.com',
 'Origin': 'http://www.yv55.com',
 'Referer': 'http://www.yv55.com/PersonalCenter',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
               'like Gecko) Chrome/60.0.3112.113 Safari/537.36',
 'X-Requested-With': 'XMLHttpRequest'}



url2="http://www.yv55.com/uc/GetAllBet?0.4610653719152149"
url3="http://www.yv55.com/uc/SubmitBet?0.7372482543845444"
post_body="issueNum=201710070782&hongtl=100&DFW=0&huitl=0&myy=0"


def checktime():
    r=requests.post(url,headers=headers)
    try:
        result = r.json()
    except BaseException as e:
        print(r.text)
    a=result['list']
    b=result['nTime']
    return b

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
while 1:
    if b>39000:
        dt=(b-39000)/1000
    else:
        dt=(b+21000)/1000
    print("wait:",dt)
    time.sleep(dt)
    try:
        c=getbat()
        print('筹码差额',c/100000000)
        if c>-130000000 and c<-75000000:
            bat()
    except BaseException as e:
        print("产生了错误",e)
        pass
    finally:
        b=checktime()
        print(b)
