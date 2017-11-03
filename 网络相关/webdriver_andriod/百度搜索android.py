# -*- coding: UTF-8 -*-
import os
import time
from selenium import webdriver

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











browser.get('http://www.baidu.com')

user = browser.find_element_by_xpath("//*[@id='kw']")
'''xpath路径获取：使用chrome浏览器开发者选项，定位到元素，
在元素html代码上点右键，选择copy-copy xpath。复制代码内的双引号要改成单引号
'''
print(user)
user.clear()#清除文本框内数据
user.send_keys("102757017")#写数据

user2 = browser.find_element_by_xpath("//*[@id='su']")
user2.click()
#browser.close() #关闭浏览器