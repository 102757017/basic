# -*- coding: UTF-8 -*-
import pprint



#从fiddler内复制header到此处
headers='''Host: 192.168.2.1
Connection: keep-alive
Content-Length: 61
Accept: */*
Origin: http://192.168.2.1
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Content-Type: application/json
Referer: http://192.168.2.1/?t=1510587253
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8'''



#pprint.pprint(headers)
head={}
a=headers.split("\n")
for x in a:
    b=x.split(": ")
    b1=b[0]
    b2=b[1]
    head[b1]=b2
pprint.pprint(head)
