# -*- coding: UTF-8 -*-
from selenium import webdriver
import os

# 设置chromium可执行文件和chromedriver.exe驱动路径
options = webdriver.ChromeOptions()
options.binary_location = r'D:\Program Files\local-chromium\575458\chrome-win32\chrome.exe'
driver_path = r'H:\学习资料\编程学习\pathon\基础操作\basic\网络相关\webdriver\chromedriver_win32\chromedriver.exe'
browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

# 请求目标网址
browser.get('https://python.org')

a=browser.get_cookies() #获取当前页面的cookies
print(a)

# 退出
driver.quit()
