# -*- coding: UTF-8 -*-
import re          #导入正则表达式库
import time        #导入延时函数库
#import androidhelper  #导入安卓API库
import chardet
import requests
import sqlite3
import os

#os.chdir(os.path.dirname(__file__))

conn = sqlite3.connect('test.db')
# 创建一个Cursor:
cursor = conn.cursor()


#在url内输入关键词和价格上、下限
url = "https://s.2.taobao.com/list/list.htm?_input_charset=utf-8&start=500&end=800&q=小米 全新&ist=0"
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate, br',
 'Accept-Language': 'zh-CN,zh;q=0.9',
 'Connection': 'keep-alive',
 'Cookie': 'swfstore=51641; thw=cn; t=3a377139f8278112b9ff39e8fba21356; '
           'cna=oU+tE4qxJzUCAXdiPW61qgv1; tg=0; '
           'UM_distinctid=16417fd1de42c-0641f52568185-47e1137-1fa400-16417fd1de67ec; '
           'x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; '
           'hng=CN%7Czh-CN%7CCNY%7C156; '
           'enc=WpCn2dPRM56J3rcpZIZq51ur34FkKTThanz%2B3ofLwyjZK1U8AgsAVNoL8KYabEq1p5v4kyB3wbNdxwo96kE7vA%3D%3D; '
           'miid=8497391561744461801; '
           '_m_h5_tk=ac2b3a4b365f68f4363a6828047b2514_1541701458289; '
           '_m_h5_tk_enc=1bad695f86a090786e56203d88c01bde; '
           'cookie2=32302c28d322b1a262d1f3d2c3e44353; '
           '_tb_token_=e73eb7e33e5a7; '
           'CNZZDATA30058275=cnzz_eid%3D76868439-1542111753-%26ntime%3D1542111753; '
           'CNZZDATA1252911424=1528423750-1542108450-%7C1542113851; v=0; '
           'unb=48570348; sg=781; _l_g_=Ug%3D%3D; skt=be2654707bdea95f; '
           'cookie1=BqVpxpn3YlQ7DAL3om58U2SHoBThkU8hbNQwfK0Ah%2FI%3D; '
           'csg=db997f30; '
           'uc3=vt3=F8dByR%2FNWnt4iKBzfDA%3D&id2=VyT2ER3%2FGeM%3D&nk2=C3w%2BCIAJiioWAQ%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; '
           'existShop=MTU0MjExNTgxNg%3D%3D; tracknick=h102757017; '
           'lgc=h102757017; _cc_=U%2BGCWk%2F7og%3D%3D; dnk=h102757017; '
           '_nk_=h102757017; cookie17=VyT2ER3%2FGeM%3D; '
           'uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&pas=0&cookie14=UoTYNO6HDqnxQg%3D%3D&tag=8&lng=zh_CN; '
           'mt=ci=3_1; whl=-1%260%260%261542115873936; '
           'isg=BPf3mYFGYCRH4-RqzWv8PD4XhuuBFMlykpa1nEmlwkYt-BQ6V4gYb_Wa3hgDEKOW',
 'Host': 's.2.taobao.com',
 'Referer': 'https://s.2.taobao.com/list/list.htm?spm=2007.1000337.6.2.4d42304ecRga8H&st_edtime=1&q=%BA%EC%C3%D7+s2+%C8%AB%D0%C2&ist=1',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
pushurl="http://sc.ftqq.com/SCU16688T720aa0191560d41d3d15b007b46ca2175a1ac1a6eb851.send"
pushheaders={'Accept': '*/*',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'Connection': 'keep-alive',
 'Content-Length': '34',
 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
 'Host': 'sc.ftqq.com',
 'Origin': 'http://sc.ftqq.com',
 'Referer': 'http://sc.ftqq.com/?c=code',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
               'like Gecko) Chrome/60.0.3112.113 Safari/537.36',
 'X-Requested-With': 'XMLHttpRequest'}



xb=[]      #创建一个空的列表保存产品清单
while True:
    try:
        r=requests.get(url,headers=headers)
        a=r.text
        result = re.findall(r'href="(.+?)">(.+?)</a></h4>[\s\S]+?</b><em>([0-9]+.[0-9]{2})</em>',a)
        for x in result:
            cursor.execute('select * from xianyu where url=?', ("https:"+x[0],))
            values = cursor.fetchall()
            if len(values)==0:
                xb.append(x)
                href="https:"+x[0]
                cursor.execute("insert into xianyu values (?,?,?,?)",(href,x[1],x[2],time.strftime("%m/%d/%Y %H:%M")))
                # 提交事务:
                conn.commit()
            
                print(x[1],x[2])
                d = {'text': x[1]+x[2], 'desp': href}
                r2 = requests.post(pushurl, headers=pushheaders,data=d)
                #droid.vibrate(3000)                #震动

        time.sleep(60)          #每60s循环一次
    except BaseException as e:
        print('产生了错误,跳过错误:', e)
        time.sleep(60)
        pass

# 关闭Cursor:
cursor.close()

# 关闭数据库
conn.close()


