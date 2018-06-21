# -*- coding: UTF-8 -*-

from selenium import webdriver

#启动浏览器的时候不想看的浏览器运行，那就加载浏览器的静默模式，让它在后台偷偷运行。用headless
option = webdriver.ChromeOptions()
option.add_argument('headless')

try:
    #browser  = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.ANDROID)        
    browser = webdriver.Android(host='localhost', port=8080, desired_capabilities={'browserName': 'android', 'version': '', 'platform': 'ANDROID'})
except BaseException as e:
    #加载预设项
    browser = webdriver.Chrome(chrome_options=option)

browser.get('http://www.baidu.com')
a=browser.get_cookies() #获取当前页面的cookies
print(a)

#browser.close() #关闭浏览器
