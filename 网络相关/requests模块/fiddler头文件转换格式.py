# -*- coding: UTF-8 -*-
import pprint



#从fiddler内复制header到此处
headers='''Host: rpc.zhongtuobang.com
Connection: keep-alive
Content-Length: 339
Accept: application/json
Origin: https://wx.zhongtuobang.com
User-Agent: Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A3000 Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 MicroMessenger/6.5.23.1180 NetType/WIFI Language/zh_CN
Content-Type: application/json;charset=UTF-8
Referer: https://wx.zhongtuobang.com/payment/ddk
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en-US;q=0.8
X-Requested-With: com.tencent.mm'''


#pprint.pprint(headers)
head={}
a=headers.split("\n")
for x in a:
    b=x.split(": ")
    b1=b[0]
    b2=b[1]
    head[b1]=b2
pprint.pprint(head)




postdata="bssid=2c%3Ab2%3A1a%3A5c%3Acb%3Af1&sign=ee6c5eec440009d7f56ddb5ab37db567d7b448a0&carrier=wifi&domain=appdownload.alicdn.com%20wwc.alicdn.com%20huodong.m.taobao.com&appName=taobao_android&lng=0.0&platformVersion=7.1.1&mnc=wifi&sid=48570348&cv=1&appVersion=7.1.0&signType=sec&t=1515041651878&preIp=106.11.11.95%3B106.11.12.92%3B106.11.253.66%3B106.11.42.24%3B106.11.42.29%3B106.11.42.30%3B106.11.42.33%3B106.11.42.48%3B106.11.42.52%3B106.11.93.13%3B106.11.95.13%3B116.211.133.219%3B116.211.152.241%3B116.211.153.189%3B116.211.153.193%3B116.211.183.109%3B116.211.183.226%3B116.211.183.238%3B116.211.183.89%3B116.211.183.96%3B116.211.249.90%3B116.211.249.96%3B140.205.163.87%3B140.205.163.89%3B140.205.35.58%3B221.233.60.240&netType=WIFI&lat=0.0&channel=600000"
print("\n\n\n\n\n\n\npost参数")
p={}
c=postdata.split("&")
#pprint.pprint(c)
for x in c:
    d=x.split("=")
    d1=d[0]
    try:
        d2=d[1]
        d2=d2.replace("%2B","+")
        d2=d2.replace("%20"," ")
        d2=d2.replace("%2F","/")
        d2=d2.replace("%3F","?")
        d2=d2.replace("%25","%")
        d2=d2.replace("%26","&")
        d2=d2.replace("%3D","=")
        d2=d2.replace("%23","#")
        d2=d2.replace("%3B",";")
    except:
        d2=""
    p[d1]=d2

pprint.pprint(p)
