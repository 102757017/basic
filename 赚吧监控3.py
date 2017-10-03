# -*- coding: UTF-8 -*-
import re          #导入正则表达式库
import time        #导入延时函数库
#import androidhelper  #导入安卓API库
import chardet
import requests
import sqlite3
import os

os.chdir(os.path.dirname(__file__))

conn = sqlite3.connect('test.db')
# 创建一个Cursor:
cursor = conn.cursor()


url = "http://www.zuanke8.com/forum.php?mod=forumdisplay&fid=15&filter=author&orderby=dateline"
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Host': 'www.zuanke8.com',
         'Content-Type': 'text/html',
         'Connection': 'Keep-Alive',
         'Cache-Control': 'max-age=0',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
         }



xb=[]      #创建一个空的列表保存线报清单
#droid=androidhelper.Android()
xb=[]      #创建一个空的列表保存线报清单
while 2>1:
    try:
        r=requests.get(url,headers=headers)
        a=r.text
        result = re.findall(r'<a href="(.+?)"  class="s xst" target="_blank">(.+?)[\n\r]{2} - \[阅读权限 <span class="xw1">([0-9]+)',a)
        for x in result:
            cursor.execute('select * from table1 where 线报=?', (x[1],))
            values = cursor.fetchall()
            if len(values)==0:
                xb.append(x)
                href=x[0].replace('amp;','')
                cursor.execute("insert into table1 values (?,?,?,?)",(href,x[1],x[2],time.strftime("%m/%d/%Y %H:%M")))
                # 提交事务:
                conn.commit()
            
                print(x[1],x[2])
                #droid.vibrate(3000)                #震动

        time.sleep(3)          #每60s循环一次
    except BaseException as e:
        #print('产生了错误,跳过错误:', e)
        time.sleep(3)
        pass

# 关闭Cursor:
cursor.close()

# 关闭数据库
conn.close()


