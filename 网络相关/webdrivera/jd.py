# -*- coding: UTF-8 -*-
import os
import time
import pprint
from selenium import webdriver

def getcookie():
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
    
    browser = webdriver.Android(host='localhost', port=8080, desired_capabilities={'browserName': 'android', 'version': '', 'platform': 'ANDROID'})
    #browser = webdriver.Chrome()


    browser.get('https://plogin.m.jd.com/user/login.action?appid=100')

    user = browser.find_element_by_xpath("//*[@id='username']")
    '''xpath路径获取：使用chrome浏览器开发者选项，定位到元素，
    在元素html代码上点右键，选择copy-copy xpath。复制代码内的双引号要改成单引号
    '''
    user.clear()#清除文本框内数据
    user.send_keys("102757017")#写数据

    password = browser.find_element_by_xpath("//*[@id='password']")
    password.clear()#清除文本框内数据
    password.send_keys("h37174141")#写数据

    login = browser.find_element_by_xpath("//*[@id='loginBtn']")
    login.click()#点击按钮

    #a=browser.get_cookies() #获取当前页面的cookies
    #for x in a:
        #cookies=cookies+x['name'] + "=" + x['value'] + ";"
    #print(cookies)
    #browser.close() #关闭浏览器
    return browser
    



