# -*- coding: UTF-8 -*-
import pprint



#从fiddler内复制header到此处
headers='''User-agent: smzdm_android_V8.7.7 rv:455 (ONEPLUS A3000;Android7.1.1;zh)smzdmapp
Host: api.smzdm.com
Connection: Keep-Alive
Accept-Encoding: gzip'''


#pprint.pprint(headers)
head={}
a=headers.split("\n")
for x in a:
    b=x.split(": ")
    b1=b[0]
    b2=b[1]
    head[b1]=b2
pprint.pprint(head)




postdata="%22id%22:%225472%22,%22couponListType%22:%224%22,%22clientType%22:%22web%22,%22clientVersion%22:%220.0.0%22"
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
