# -*- coding: UTF-8 -*-
from selenium import webdriver
import pprint
import requests
import time



browser = webdriver.Chrome()
browser.get('https://www.lup2p.com/user/login?returnPostURL=https%3A%2F%2Fwww.lup2p.com%2Fsecmkt%2FproductDetail%2Fp2p%3FproductId%3D181294888850353%26from%3Dlup2p')

cookies=[{'domain': '.lup2p.com', 'httpOnly': False, 'name': '_token', 'path': '/', 'secure': False, 'value': '"MDZiMGI3Y2VlNTJmZmNjMzlkZjk2YzQxMTI4YzM1ZGMwZGE4MzAxYjo2MzMzNDg3OjE1NDkwOTA2NDcyMDc="'}, {'domain': '.lup2p.com', 'expiry': 1706770585.999831, 'httpOnly': False, 'name': '_g2', 'path': '/', 'secure': False, 'value': 'n_430302_58fdcd2d-abec-4c21-91c2-b56f3a049736'}, {'domain': '.lup2p.com', 'expiry': 1706770585.999737, 'httpOnly': True, 'name': '_g', 'path': '/', 'secure': False, 'value': 'n_430302_70fd771c-d399-42a7-9a34-d8b26a9f63d8'}, {'domain': '.www.lup2p.com', 'expiry': 1580626624, 'httpOnly': False, 'name': 'Hm_lvt_9842c7dcbbff3109ea37b7407dd0e95c', 'path': '/', 'secure': False, 'value': '1549090587'}, {'domain': '.lup2p.com', 'httpOnly': True, 'name': 'IMVC', 'path': '/', 'secure': False, 'value': '272b4e6a76264a9780fa6d1e39b05c5e'}, {'domain': '.lup2p.com', 'expiry': 1706770623.670423, 'httpOnly': False, 'name': '_tn', 'path': '/', 'secure': False, 'value': '"M0E5RTcxQTg4RDRCNTQxNEIwOUYzNjkzODUxRDBBODc="'}, {'domain': '.lup2p.com', 'httpOnly': True, 'name': '_lufaxSID', 'path': '/', 'secure': False, 'value': '"4a98789e-3b17-4703-9652-4cf5eeff4f46,ujsL62nvfIJ6emQbADBtl62GyIzmF+YoaaqYkim7RoWjKwp4qoPspZdOhmxEm6FPIEOVA2FguEjRjYzI6kZUJQ=="'}, {'domain': '.lup2p.com', 'expiry': 1551682586.878201, 'httpOnly': True, 'name': '_fp', 'path': '/', 'secure': False, 'value': '"HTREVzIwMTkwMTEwMTAzODM5OTUxNjg1_flUxiPJgSzQK/ev+JyNMVaGMRpjcFSGckL4SAt1zstrVBMGxnaSlKCw6wb+awwJ2I+I=:QhYz3psU0OXsKWeFAdu5zE4HgMRq5P2nha6shJ5MM3U="'}, {'domain': '.lup2p.com', 'expiry': 1706770623.67047, 'httpOnly': False, 'name': '_tnf', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.lup2p.com', 'expiry': 1706770623.670512, 'httpOnly': False, 'name': '_tm', 'path': '/', 'secure': False, 'value': '"M0E5RTcxQTg4RDRCNTQxNEIwOUYzNjkzODUxRDBBODc="'}, {'domain': '.lup2p.com', 'expiry': 1706770623.670549, 'httpOnly': False, 'name': '_tmf', 'path': '/', 'secure': False, 'value': '2'}, {'domain': '.lup2p.com', 'expiry': 1864450624, 'httpOnly': False, 'name': 'WT-FPC', 'path': '/', 'secure': False, 'value': 'id=4.0.4.13-2030326640.30718660:lv=1549090624758:ss=1549090586992:fs=1549090586992:pn=2:vn=1'}, {'domain': '.www.lup2p.com', 'httpOnly': False, 'name': 'Hm_lpvt_9842c7dcbbff3109ea37b7407dd0e95c', 'path': '/', 'secure': False, 'value': '1549090625'}]
for cookie in cookies:
    browser.add_cookie(cookie_dict=cookie)





user = browser.find_element_by_xpath("//*[@id='userNameLogin']")
'''xpath路径获取：使用chrome浏览器开发者选项，定位到元素，
在元素html代码上点右键，选择copy-copy xpath。复制代码内的双引号要改成单引号
'''
user.clear()#清除文本框内数据
user.send_keys("15827577155")#写数据

pwd = browser.find_element_by_xpath("//*[@id='pwd']")
'''xpath路径获取：使用chrome浏览器开发者选项，定位到元素，
在元素html代码上点右键，选择copy-copy xpath。复制代码内的双引号要改成单引号
'''
pwd.clear()#清除文本框内数据
pwd.send_keys("h37174141")#写数据

button = browser.find_element_by_xpath("//*[@id='loginBtn']")
button.click()
#点击按钮后必须加延时，否则页面还没加载完成就执行后面的语句了
time.sleep(2)
browser.get("https://my.lu.com/my/account")


cookies=''
a=browser.get_cookies()
for x in a:
    cookies=cookies+x['name'] + "=" + x['value'] + ";"
print(cookies)









headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate, br',
 'Accept-Language': 'zh-CN,zh;q=0.9',
 'Connection': 'keep-alive',
 'Cookie':cookies ,
 'Host': 'my.lu.com',
 'Referer': 'https://www.lup2p.com/secmkt/productDetail/p2p?productId=181294888850353&from=lup2p',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}








url = 'https://my.lu.com/my/account'
r=requests.get(url,headers=headers,verify=False)
a=r.text
print(a)
