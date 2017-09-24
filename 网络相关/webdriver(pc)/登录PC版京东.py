# -*- coding: UTF-8 -*-

from selenium import webdriver

browser = webdriver.Chrome()

browser.get('https://passport.jd.com/new/login.aspx?')

ulogin=browser.find_element_by_xpath("//*[@id='content']/div[2]/div[1]/div/div[2]/a")
ulogin.click()

user = browser.find_element_by_id("loginname")#按id定位搜索文本框
user=browser.find_element_by_xpath("//*[@id='loginname']")#另一种方法是使用xpath定位
user.clear()#清除文本框内数据
user.send_keys("102757017")#写数据

password = browser.find_element_by_id("nloginpwd")#按id定位搜索文本框
password = browser.find_element_by_xpath("//*[@id='nloginpwd']")#另一种方法是使用xpath定位
password.clear()#清除文本框内数据
password.send_keys("h37174141")#写数据

login = browser.find_element_by_xpath("//*[@id='loginsubmit']")
login.click()#点击按钮

browser.get('https://a.jd.com/')
browser.get('https://a.jd.com/')
coupon=browser.find_element_by_xpath("//*[@id='quanlist']/div[7]/div[1]/div[4]/div[1]/a")
#定位页面第7张优惠券
coupon.click()

a=browser.get_cookies() #获取当前页面的cookies

a=browser.page_source #获取网页渲染后的源代码



#browser.close() #关闭浏览器
