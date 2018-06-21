# -*- coding: UTF-8 -*-

from selenium import webdriver
import os

#需要先将驱动文件chromedriver.exe复制到chrome的安装目录下，…\Google\Chrome\Application\
executable_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"   #指定chromediver的位置
os.environ["webdriver.chrome.driver"] = executable_path
browser = webdriver.Chrome(executable_path)

browser.get('http://www.baidu.com')
a=browser.get_cookies() #获取当前页面的cookies
print(a)

#browser.close() #关闭浏览器
