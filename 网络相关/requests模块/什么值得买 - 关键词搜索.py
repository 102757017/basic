# -*- coding: UTF-8 -*-
import re          #导入正则表达式库
import time        #导入延时函数库
import datetime
#import androidhelper  #导入安卓API库
import chardet
import requests
import sqlite3
import os
import pprint
import urllib.parse


headers={'Accept-Encoding': 'gzip',
 'Connection': 'Keep-Alive',
 'Host': 'api.smzdm.com',
 'User-agent': 'smzdm_android_V8.7.7 rv:455 (ONEPLUS '
               'A3000;Android7.1.1;zh)smzdmapp'}

key="蓝牙耳机"
key=urllib.parse.unquote(key)

goods=[]
for i in range(100):
    t=20*i
    url="http://api.smzdm.com/v1/list?keyword="+key+"&type=good_price&order=score&day=&limit=20&offset="+str(t)
    #print(url)
    r=requests.get(url,headers=headers)
    data=r.json()['data']['rows']
    goods=goods+data


a=open(os.path.join(os.path.dirname(__file__),"WorthyGoods.html"),'w',encoding='utf-8')
a.write('''<html>
<head><title>Ordering notice</title></head>
<body>
''')
#<br>表示html渲染后换行
a.write("更新时间:"+str(datetime.datetime.now())+"<br>\n")

for x in goods:
    comments=int(x["article_comment"])
    worthy=float(x['worthy_per_cent'])
    if worthy>0.85 and comments>10:
        #print(x["article_pic"])
        print(x["article_title"])
        print(x["article_price"])
        print(x["article_url"],"\n")
            
        a.write("<a href=\""+x["article_url"]+"\">"+"  </a>")
        a.write(x["article_title"])
        a.write(x["article_price"])
        a.write("<br>\n")            
        a.write("<a href=\""+x["article_url"]+"\"><img src=\""+x["article_pic"]+"\"></a>")
        a.write("<br>\n")         
a.write('''</body>
</html>
''')
a.close()
