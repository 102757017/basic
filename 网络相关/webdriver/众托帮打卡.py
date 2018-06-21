# -*- coding: UTF-8 -*-
import os
import time
import pprint
from selenium import webdriver
import requests
import re
import chardet

def getcookie(un,pw):
    c1='sh & '
    c2=r"am start -n org.openqa.selenium.android.app/org.openqa.selenium.android.app.MainActivity"
    c3=r"am force-stop org.openqa.selenium.android.app"
    c=c1+c3
    os.system(c)
    time.sleep(2)
    c=c1+c2
    os.system(c)
    time.sleep(1)
    desired_caps = {}
    desired_caps['platform'] = 'Android'
    desired_caps['platformVersion'] = '4.4.4'
    desired_caps['deviceName'] = 'MI 3'
    desired_caps['browserName'] = 'chrome'
    desired_caps['noReset'] = 'true'

    try:
        #browser  = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.ANDROID)        
        browser = webdriver.Android(host='localhost', port=8080, desired_capabilities={'browserName': 'android', 'version': '', 'platform': 'ANDROID'})
    except BaseException as e:
        browser = webdriver.Chrome()
        
    browser.get('https://wx.zhongtuobang.com/login/mobileLogin?uri=%2Fuser%2Fmine')

    user = browser.find_element_by_xpath("//*[@id='username']")
    '''xpath路径获取：使用chrome浏览器开发者选项，定位到元素，
    在元素html代码上点右键，选择copy-copy xpath。复制代码内的双引号要改成单引号
    '''
    user.clear()#清除文本框内数据
    user.send_keys(un)#写数据

    password = browser.find_element_by_xpath("//*[@id='password']")
    password.clear()#清除文本框内数据
    password.send_keys(pw)#写数据

    login = browser.find_element_by_xpath("//*[@id='login-userpass-btn']")
    login.click()#点击按钮
    time.sleep(3)
    
    browser.get("https://wx.zhongtuobang.com/payment/ddk")
    
    dk = browser.find_element_by_xpath("//*[@id='continueDays']/img")
    dk.click()
    time.sleep(3)

    multiple = browser.find_element_by_xpath("//*[@id='multiple']/img")
    multiple.click()
    time.sleep(3)
    
    a=browser.get_cookies() #获取当前页面的cookies
    
    cookies=""
    for x in a:
        cookies=cookies+x['name'] + "=" + x['value'] + ";"
    print(cookies)
    browser.quit() #关闭浏览器    
    return cookies




if __name__=='__main__':
    cookie=getcookie("15102758397","37174141")
