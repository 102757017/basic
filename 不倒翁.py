# -*- coding: UTF-8 -*-
import re          #导入正则表达式库
import time        #导入延时函数库
#import androidhelper  #导入安卓API库
import chardet
import requests
import sqlite3
import json
import pprint
import os

os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect('bat.db')
cursor = conn.cursor()

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


url2="http://www.yv55.com/uc/GetAllBet?0.4610653719152149"



flag=1
while 1:
    r=requests.post(url,headers=headers)
    try:
        result = r.json()
    except BaseException as e:
        print(r.text)
    #pprint.pprint(result)
    a=result['list']
    a1=a['CreateTime']
    a2=a['EditTime']
    a3=a['EndTime']
    a4=a['IssueNum']
    a5=a['KJhm']
    a6=a['LotteryNum']
    a7=a['LotteryTime']
    a8=a['StartTime']
    a9=a['id']
    b=result['nTime']
    if b<18000 and flag==1:
        r2=requests.post(url2,headers=headers)
        result2 = r2.json()
        c=result2['list']
        c1=c['DFW']
        c2=c['hongtl']
        flag=0
        cursor.execute("insert into table2 values (?,?,?,?,?,?,?,?,?,?,?,?)",(a1,a2,a3,a4,a5,a6,a7,a8,a9,b,c1,c2))
        conn.commit()
        print(a4)
    time.sleep(2)
    if b>50000:
        flag=1
    

# 关闭Cursor:
cursor.close()

# 关闭数据库
conn.close()
