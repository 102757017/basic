# -*- coding: UTF-8 -*-
import pprint


#从fiddler内复制header到此处
headers='''Host: www.yv55.com
Connection: keep-alive
Content-Length: 0
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.yv55.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Referer: http://www.yv55.com/PersonalCenter
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8'''

head={}
a=headers.split("\n")
for x in a:
    b=x.split(":")
    b1=b[0]
    b2=b[1][1:]
    head[b1]=b2
pprint.pprint(head)

