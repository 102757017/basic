# -*- coding: UTF-8 -*-
import time
import pprint
from selenium import webdriver

def getcookie():

    browser = webdriver.Chrome()

    browser.get('https://plogin.m.jd.com/user/login.action?appid=100')

    #time.sleep(10)
    user = browser.find_element_by_xpath("//*[@id='username']")
    '''xpath路径获取：使用chrome浏览器开发者选项，定位到元素，
    在元素html代码上点右键，选择copy-copy xpath。复制代码内的双引号要改成单引号
    '''
    user.clear()#清除文本框内数据
    user.send_keys("10275")#写数据

    password = browser.find_element_by_xpath("//*[@id='password']")
    password.clear()#清除文本框内数据
    password.send_keys("h3717")#写数据

    login = browser.find_element_by_xpath("//*[@id='loginBtn']")
    login.click()#点击按钮

    time.sleep(5)
    coupon = browser.find_element_by_xpath("//*[@id='appcenter']/div/div/nav/a[8]/span/img")
    coupon.click()#点击按钮
    cookies=''
    a=browser.get_cookies() #获取当前页面的cookies
    for x in a:
        cookies=cookies+x['name'] + "=" + x['value'] + ";"

    print(cookies)


    #pprint.pprint(a)

    a=browser.page_source #获取网页渲染后的源代码
    return cookies
    #browser.close() #关闭浏览器

