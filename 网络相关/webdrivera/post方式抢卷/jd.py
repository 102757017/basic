# -*- coding: UTF-8 -*-
import os
import time
import pprint
from selenium import webdriver
import requests
import re

def getcookie(Referer):
    c1='sh & '
    c2=r"am start -n org.openqa.selenium.android.app/org.openqa.selenium.android.app.MainActivity"
    c=c1+c2
    os.system(c)
    time.sleep(1)
    desired_caps = {}
    desired_caps['platform'] = 'Android'
    desired_caps['platformVersion'] = '4.4.4'
    desired_caps['deviceName'] = 'MI 3'
    desired_caps['browserName'] = 'chrome'
    desired_caps['noReset'] = 'true'

    #browser  = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.ANDROID)
    
    #browser = webdriver.Android(host='localhost', port=8080, desired_capabilities={'browserName': 'android', 'version': '', 'platform': 'ANDROID'})
    browser = webdriver.Chrome()


    browser.get('https://plogin.m.jd.com/user/login.action?appid=100')

    user = browser.find_element_by_xpath("//*[@id='username']")
    '''xpath路径获取：使用chrome浏览器开发者选项，定位到元素，
    在元素html代码上点右键，选择copy-copy xpath。复制代码内的双引号要改成单引号
    '''
    user.clear()#清除文本框内数据
    user.send_keys("15387102874")#写数据

    password = browser.find_element_by_xpath("//*[@id='password']")
    password.clear()#清除文本框内数据
    password.send_keys("asdfghjklzxc")#写数据

    login = browser.find_element_by_xpath("//*[@id='loginBtn']")
    login.click()#点击按钮
    
    browser.get(Referer)
    a=browser.get_cookies() #获取当前页面的cookies
    
    cookies=""
    for x in a:
        cookies=cookies+x['name'] + "=" + x['value'] + ";"
    print(cookies)
    #browser.close() #关闭浏览器
    return cookies


def grab(cookie,Referer,url):
    host=url.split("/")[2]
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
         'Host': host,
         'Connection': 'Keep-Alive',
         'Accept-Language': 'zh-CN,zh;q=0.8',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept': '*/*',
         'Referer': Referer,
         'Cookie':cookie
         }
    try:
        r=requests.get(url,headers=headers)
    except BaseException as e:
        print('抢卷出错:', e)
    
    #d = {'key1': 'value1', 'key2': 'value2'}
    #r=requests.post(url,headers=headers,data=d)
    print(r.text)
    return(r.text)

def makeurl(Referer):
    host=Referer.split("/")[2]
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
         'Host': host,
         'Connection': 'Keep-Alive',
         'Accept-Language': 'zh-CN,zh;q=0.8',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept': '*/*',
         'Referer': Referer
         }
    try:
        r=requests.get(Referer,headers=headers)
    except BaseException as e:
        print('获取网页源码出错:', e)
    result1 = re.findall('"limit":(.+?),.+?"scene":(.+?),"args":(.+?),"',r.text)
    result2=re.findall('"encodeActivityId":(.+?),',r.text)
    href=[]
    for x in result1:
        body="body={\"activityId\":"+ result2[0] +",\"scene\":"+ x[1] +",\"args\":"+ x[2] +",\"mitemAddrId\":\"\",\"geo\":{\"lng\":\"\",\"lat\":\"\"}}"        
        link="https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&"+body+"&client=wh5&clientVersion=1.0.0"
        title=x[0]
        href.append([title,link])

    '''    
    body={"activityId":"2swvgWopcM4Xy6hyxuE8toBnSkzV",
          "scene":"1",
          "args":"key=c817ac797dec4060a3b748d51092ad34,roleId=8245445,to=pro.m.jd.com/mall/active/2vmBPknBMoauhsFm2Lc7nD5ARg45/index.html",
          "mitemAddrId":"",
          "geo":{"lng":"","lat":""}}
    '''
    pprint.pprint(href)
    return(href)



#Referer为领卷页面
Referer="https://pro.m.jd.com/mall/active/2swvgWopcM4Xy6hyxuE8toBnSkzV/index.html"
#url为领卷链接
url="http://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%222swvgWopcM4Xy6hyxuE8toBnSkzV%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D1b86ce9ab931422ea7379e2574bbc33c%2CroleId%3D8245464%2Cto%3Dpro.m.jd.com%2Fmall%2Factive%2F2vmBPknBMoauhsFm2Lc7nD5ARg45%2Findex.html%22%2C%22mitemAddrId%22%3A%22%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%7D&client=wh5&clientVersion=1.0.0&sid=99bd1b2f69031dafbaf5cacc4b5a4ad7&uuid=1504359002749618854944&area=&_=1506784781082&callback=jsonp3"
makeurl(Referer)
#cookie=getcookie(Referer)
#grab(cookie,Referer,url)
