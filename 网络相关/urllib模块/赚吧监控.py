# -*- coding: UTF-8 -*-
from urllib import request   #导入request库中的urllib函数
import urllib
import re          #导入正则表达式库
import time        #导入延时函数库
#import androidhelper  #导入安卓API库

import gzip     #部分网页是采取gzip压缩的，直接读取会得到乱码，需要先解压
import socket   

timeout = 60
socket.setdefaulttimeout(timeout)         #设置urlopen的超时时间







def search(x):      #定义一个函数，需要加“：”函数下面缩进的内容相当于{},x表示html文件保存路径
    url = "http://www.zuanke8.com/forum.php?mod=forumdisplay&fid=15&filter=author&orderby=dateline"
    req = request.Request(url)      #此处一定要用大写的Request才能表示对象
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')    #注意如果依然不能抓取，这里可以设置抓取网站的host
    req.add_header('Host','www.zuanke8.com')
    req.add_header('Connection','Keep-Alive')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Referer','https://licai.suning.com/lcportal/portal/bill/productList.htm?ajax=true&type=ticket&loanPeriod=&incomeRate=&sortName=&sortType=&pageIndex=1&_=1493473713817')
    req.add_header('Accept-Encoding','gzip, deflate')  #返回的数据是经过压缩的，直接按照 content.decode(“utf8”), 解码会出现乱码
    req.add_header('Cache-Control','max-age=0')
    try:
        f=request.urlopen(req) 
        data=f.read()
    
        temp= open(x,'wb')      #以可写模式打开x路径下的文件
        temp.write(data)
        temp.close()
    
        h=gzip.open(x, 'rb')     #gzip解压只能解压文件和内存，不能解压str
        html=h.read()
        h.close()

        temp= open(x,'wb')
        temp.write(html)
        temp.close()    
    except urllib.error.URLError as e:         #防止URLError异常导致跳出循环
        print(e.reason)
    except urllib.error.HTTPError as e:        #防止HTTP返回异常导致跳出循环
        print(e.read())        
    return(html)                     #返回result是list类型



  
def jk(x):
    t=search(x)
    #temp= open(x,'r',1,'gbk')  #手机文件打开模式，手机文件的默认编码是gbk，无法直接打开，需要用gbk解码
    temp= open(x,'r')

    
    a=temp.read()
    
    temp.close()
    result = re.findall(r'<a href="(.+?)"  class="s xst" target="_blank">(.+?)</a>\n - \[阅读权限 <span class="xw1">([0-9]+)', a)
    for x in result:
        if x not in xb:
            xb.append(x)
            print(x[1],x[2])
            #droid.vibrate(3000)                #震动

#droid=androidhelper.Android()
xb=[]      #创建一个空的列表保存线报清单
while 2>1:
    jk(r'D:\我的文档\桌面\aaa.txt')
    time.sleep(3)          #每60s循环一次
   
