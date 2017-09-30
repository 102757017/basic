# -*- coding: UTF-8 -*-
from urllib import request   #导入request库中的urllib函数
import urllib
import re          #导入正则表达式库
import time        #导入延时函数库
import os
import androidhelper  #导入安卓API库
import ssl

def search():      #定义一个函数，需要加“：”函数下面缩进的内容相当于{}
    url = "https://licai.suning.com/lcportal/portal/bill/productList.htm?ajax=true&type=ticket&loanPeriod=&incomeRate=&sortName=&sortType=&pageIndex=1&_=1505043744127"
    req = request.Request(url)      #此处一定要用大写的Request才能表示对象
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')    #注意如果依然不能抓取，这里可以设置抓取网站的host
    req.add_header('Referer','https://licai.suning.com/lcportal/portal/period/list.htm?srclc=PC_LCSY_daohang3&channelCode=PC_LCSY_daohang3')
    req.add_header('Host','licai.suning.com')
    req.add_header('Cookie','__wmv=1493044579.1; _snma=1%7C149304457748876966%7C1493044577488%7C1493044577488%7C1493044577488%7C1%7C1; __ssav=149304457748876966%7C1493044579131%7C1493044579131%7C1493044579131%7C1%7C1%7C1; _ga=GA1.2.1380423976.1493044594; JSESSIONID=4Au_zOkzAbz9LMnC6J9Zvizn.slave57:fserver2; _cusenoek=1AB6E5A2DCEE5095E5337HBB')
    req.add_header('Connection','Keep-Alive')
    req.add_header('Accept','*/*')
    req.add_header('Referer','https://licai.suning.com/lcportal/portal/bill/productList.htm?ajax=true&type=ticket&loanPeriod=&incomeRate=&sortName=&sortType=&pageIndex=1&_=1493473713817')
    req.add_header('Accept-Encoding','gzip')
    f=request.urlopen(req)
    html=f.read()
    html=html.decode('utf-8')       #读取的网页编码是utf-8编码，需要解码成unicode编码才能正常显示。
    result = re.findall(r'"limitDay":"([0-9]+)","minAmount"', html) #在字符串html中搜索天数
    return(result)                     #返回result是list类型

context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context
droid=androidhelper.Android()
t=search()
for x in t:
    print(x)


while 2>1:
    try:
        t=search()
        for x in t:
            print(x)
            if int(x)<40:
                #droid.vibrate(1000)  
                print('找到小于30天的产品')
                droid.mediaPlay(r'/storage/emulated/0/kgmusic/download/金南玲 - 逆流成河.mp3') 
        time.sleep(60)          #每60s循环一次
    except BaseException as e:
        print('产生了错误,跳过错误:', e)
        time