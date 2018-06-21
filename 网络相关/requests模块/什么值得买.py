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

signurl="https://api.smzdm.com/v1/user/checkin"
signheader={'Accept-Encoding': 'gzip',
 'Connection': 'Keep-Alive',
 'Content-Length': '267',
 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
 'Cookie': 'sess=NjgxMjF8MTUxNzA0ODA2OHw2NzgwNjY1MjQyfDM5ZGRlZTA1ZThlMjUzODU5MTViMDdhNTU5ZWE5Yjhk;ab_test=d;pid=99000736971433;partner_id=4;device_id=e15548e1ed76a1d291d31c2def68a2b6;imei=427c28421b32f91c4c12901326573e33;partner_name=360market;mac=02:00:00:00:00:00;smzdm_id=6780665242;login=1;device_push=1;network=wifi;device_smzdm_version=8.5.3;device_smzdm_version_code=434;device_s=jHkyBXLyqgKpjvLB3PIjpJnNZIdTQLnc;device_type=OnePlusONEPLUS '
           'A3000;device_system_version=7.1.1;device_smzdm=android;rs_id1=;rs_id2=;rs_id3=;rs_id4=;rs_id5=;smzdm_device=android;smzdm_user_source=jHkyBXLyqgKpjvLB3PIjpJnNZIdTQLnc;smzdm_version=8.5.3;',
 'Host': 'api.smzdm.com',
 'If-Modified-Since': 'Sat, 23 Dec 2017 03:53:05 GMT+00:00',
 'User-agent': 'smzdm_android_V8.5.3 rv:434 (ONEPLUS '
               'A3000;Android7.1.1;zh)smzdmapp'}
signdata=signdata={'captcha': '',
 'f': 'android',
 's': 'jHkyBXLyqgKpjvLB3PIjpJnNZIdTQLnc',
 'sign': '7F019E76340F4C5F5EDA58454A6FD280',
 'sk': 'G1uyvK0tLJpp5c/zMTivE8Zber6CU6IZgy4jk0VdVoE=',
 'time': '1514127998832',
 'token': 'NjgxMjF8MTUxNzA0ODA2OHw2NzgwNjY1MjQyfDM5ZGRlZTA1ZThlMjUzODU5MTViMDdhNTU5ZWE5Yjhk',
 'v': '8.5.3',
 'weixin': '1'}

r = requests.post(signurl,headers=signheader,data=signdata)
pprint.pprint(r.json())

lotteryurl="https://api.smzdm.com/v1/user/lottery/draw"
lotteryheader={'Accept-Encoding': 'gzip',
 'Connection': 'Keep-Alive',
 'Content-Length': '0',
 'Content-Type': 'application/x-www-form-urlencoded',
 'Cookie': 'sess=NjgxMjF8MTUxNzA0ODA2OHw2NzgwNjY1MjQyfDM5ZGRlZTA1ZThlMjUzODU5MTViMDdhNTU5ZWE5Yjhk;ab_test=d;pid=99000736971433;partner_id=4;device_id=e15548e1ed76a1d291d31c2def68a2b6;imei=427c28421b32f91c4c12901326573e33;partner_name=360market;mac=02:00:00:00:00:00;smzdm_id=6780665242;login=1;device_push=1;network=wifi;device_smzdm_version=8.5.3;device_smzdm_version_code=434;device_s=jHkyBXLyqgKpjvLB3PIjpJnNZIdTQLnc;device_type=OnePlusONEPLUS '
           'A3000;device_system_version=7.1.1;device_smzdm=android;rs_id1=;rs_id2=;rs_id3=;rs_id4=;rs_id5=;smzdm_device=android;smzdm_user_source=jHkyBXLyqgKpjvLB3PIjpJnNZIdTQLnc;smzdm_version=8.5.3;',
 'Host': 'api.smzdm.com',
 'User-agent': 'smzdm_android_V8.5.3 rv:434 (ONEPLUS '
               'A3000;Android7.1.1;zh)smzdmapp'}
r = requests.post(lotteryurl,headers=lotteryheader)
pprint.pprint(r.json())





url = "https://m.smzdm.com/"
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate, br',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'Cache-Control': 'max-age=0',
 'Connection': 'keep-alive',
 'Host': 'm.smzdm.com',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
               'like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


r=requests.get(url,headers=headers)
timesort = re.findall('timesort="([0-9]{12})"',r.text)
t=timesort[-1]
#title = re.findall(r"""'pagetitle':(.*?)\}\)" href="(https?://[^ ]*?)"[\s\S]{1000,1500}"zm-icon-comments-o"></i>([0-9]{0,4}) {10,30}</span>[\s\S]{50,200}"zm-icon-zhi-char"></i>([0-9]{0,3}%?) {10,30}</span>""",a)

#pprint.pprint(timesort)

goods=[]
for i in range(15):
    url="https://m.smzdm.com/ajax_home_list_show?timesort="+t
    #print(url)
    r=requests.get(url,headers=headers)
    data=r.json()['data']
    goods=goods+data
    t=data[-1]["time_sort"]
#print(type(goods),len(goods))

a=open(os.path.join(os.path.dirname(__file__),"WorthyGoods.html"),'w',encoding='utf-8')
a.write('''<html>
<head><title>Ordering notice</title></head>
<body>
''')
#<br>表示html渲染后换行
a.write("更新时间:"+str(datetime.datetime.now())+"<br>\n")

for x in goods:
    if 'article_worthy' in x:
        worthy=str(x["article_worthy"])
        worthy=worthy.replace("%","")
        worthy=int(worthy)/100
        comments=int(x["article_comment"])
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
