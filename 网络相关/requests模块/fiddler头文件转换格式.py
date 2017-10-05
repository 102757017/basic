# -*- coding: UTF-8 -*-
import pprint


#从fiddler内复制header到此处
headers='''Host: www.baidu.com
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: BAIDUID=BBE82D421F44BBEC0383435F9C0766AA:FG=1; BIDUPSID=BBE82D421F44BBEC0383435F9C0766AA; PSTM=1502987050; __cfduid=de14f09f10a3abb11a4577e65f1e829a41503327809; sugstore=1; MCITY=-218%3A156%3A; ispeed_lsm=0; H_PS_645EC=88398W0iAvnZpxz8xE2Z%2FACv9XxfMhFnRGqXDIjn%2BOo2U6ljKXDHXPxUyro; BD_CK_SAM=1; PSINO=3; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=0; H_PS_PSSID=1441_21085_17001_20719; BD_UPN=12314353'''

#pprint.pprint(headers)
head={}
a=headers.split("\n")
for x in a:
    b=x.split(": ")
    b1=b[0]
    b2=b[1]
    head[b1]=b2
pprint.pprint(head)

