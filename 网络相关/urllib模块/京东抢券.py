# -*- coding: UTF-8 -*-
from urllib import request   #导入request库中的urllib函数
import urllib
import re          #导入正则表达式库
import time        #导入延时函数库
#import androidhelper  #导入安卓API库
import http.client
import datetime
import os
import gzip     #部分网页是采取gzip压缩的，直接读取会得到乱码，需要先解压
import socket   

timeout = 60
socket.setdefaulttimeout(timeout)         #设置urlopen的超时时间



def GetJDServerTime():
    """获取jd服务器时间
    NOTE: 原理是通过服务器头文件响应获取服务器时间
    """
    
    conn = http.client.HTTPConnection( 'miaosha.jd.com' )
    conn.request( 'GET', '/' )
    response = conn.getresponse()
    ts =  response.getheader('Date')
    ltime = time.strptime( ts[5:25], '%d %b %Y %H:%M:%S' )
    ttime=time.localtime(time.mktime(ltime)+8*60*60)    
    dat="date %u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    tm="time %02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    os.system(dat)
    os.system(tm)
    time_now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print("修正完了，当前系统时间:"+time_now)
        #按照特定时间格式将字符串转换为时间类型
    
    return time_now






#使用前要替换URL为抢券链接，并且替换cookie

def search(link,ck):      #定义一个函数，需要加“：”函数下面缩进的内容相当于{},x表示html文件保存路径
    url =link
    req = request.Request(url)      #此处一定要用大写的Request才能表示对象
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')    #注意如果依然不能抓取，这里可以设置抓取网站的host
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    req.add_header('Accept-Encoding','gzip, deflate')  #返回的数据是经过压缩的，直接按照 content.decode(“utf8”), 解码会出现乱码
    req.add_header('Host','coupon.jd.com')
    req.add_header('Cookie',ck)
    try:
        f=request.urlopen(req) 
        data=f.read()
        html=gzip.decompress(data).decode("utf-8")
        #html=data.decode("utf-8")  
    except OSError as e:
        html=data
    except urllib.error.URLError as e:         #防止URLError异常导致跳出循环
        print('urlerror')
        pass
    except urllib.error.HTTPError as e:        #防止HTTP返回异常导致跳出循环
        print('httperror')
        pass
    finally:
        pass
    return(html)                     #返回result是list类型


#i为抢券链接
i = []
i.append('https://coupon.jd.com/ilink/couponSendFront/send_index.action?key=541b33b4e0d84ac49b7b9f38f9c1b771&roleId=6973596&to=sale.jd.com/act/mgetnqvzxoyub4j.htm')
i.append('https://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=aee5e3cfe1d945b4bcbf9f1913f7e56c&roleId=6909661&to=sale.jd.com/act/cvafe6uqonw.html&')
i.append('https://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=21447f8a48984039b6515a31a05db571&roleId=6909660&to=sale.jd.com/act/cvafe6uqonw.html&')
j='user-key=d43f9be0-b65e-4395-8adf-e1fce86ef683; mt_xid=V2_52007VwMSV1RbW1waSR1sAzcEQVYPWVpGSEhMWxliURBTQQgCW0hVEFQNYAATB1hbUF4beRpdBWEfE1VBWFBLHEoSXwVsBhRiX2hRahtKH1wAYDMSVlw%3D; ipLoc-djd=1-72-2799-0; sid=76251ce7b01fc8685658d6a5fb328137; cn=35; TrackID=1ki3cbGEELOZQZ8gpDq2sgfVUwwsz3Mu6HB3Fo3XkzTOHjTkZK1-jSxbzzTjGP6VJjgvOBvnrQy2SVbuuoSc35Gs-LWIsGVCgrWHa0gO-Gu23MUWhCK9s08PjjWVarMRq; pinId=R5fO1lY05DJA9AXplivx1A; pin=102757017; unick=jd102757wnq; _tp=I00R%2B94QwvtSFxZRChbeQg%3D%3D; _pst=102757017; ceshi3.com=103; unpl=V2_YDNtbRYAEBIlWxNWLx0JBGJQEl8RAkIUfV8SVH8fVAM1AhEPclRCFXMUR1NnGVgUZAIZXkFcRhZFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJABNdQF9DFnQMQmRLGlw1ZwIiXUJSShZ8DkNUfylsAlczIllBUkYSfDhHZHopHlE7BBpVRl5EWHUIQ114EFoAZwciXHJU; __jdv=122270672|baidu-search|t_262767352_baidusearch|cpc|2013912055_0_efb6abd3e5d04b13bd009fe15797c02c|1497529378790; thor=F321987AC1395F963EBCCF7D05E8DB3A31529AC53C67DF83E563DFF48C2A50582481F31647D80B17E6E934D2F860391644CD88051C513EF684F31314AC0D9938F1512AD437E210B8928A6CEEBC3A5D30CF2916642E2A1EB671D7B35677A55C6DBCC322CD86500C05A2365BB2215DBB66E02E530B4DCC30078521ED570127D2EB03D392CBAD9306DDDEA647EA02AB3BB9; __jda=122270672.1148287415.1472140207.1497528429.1497529379.42; __jdc=122270672; __jdu=1148287415; 3AB9D23F7A4B3C9B=IHSNBGUVYXY53LNG5A6XUXQX6ZO3O3IXT37IIBNJPHFEA5BKTQ3Z2RFL3WOUYKVYUA6KXRIHL2NRTM6GPWNNP2YLA4'


a=GetJDServerTime()


dt = list(time.localtime())
hour = dt[3]
minute = dt[4]
z=0
while z==0:
    while hour==10 and minute==00: #上午10点00分的时候开始提示
        for x in i:
            a=search(x,j)
            result = re.findall(r'<h1 class="ctxt02"><s class="icon-redbag"></s>(.+?)\n', a)
            print(result[0])
          
            dt=list(time.localtime())
            hour = dt[3]
            minute = dt[4]
      
    


