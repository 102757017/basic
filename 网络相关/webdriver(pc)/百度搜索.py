# -*- coding: UTF-8 -*-

from selenium import webdriver

browser = webdriver.Chrome()

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
