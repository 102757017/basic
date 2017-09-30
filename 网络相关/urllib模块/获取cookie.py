#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib

import http.cookiejar

# 初始化一个CookieJar来处理Cookie

cookie=http.cookiejar.CookieJar()

#实例化一个全局opener

handler=urllib.request.HTTPCookieProcessor(cookie)

opener=urllib.request.build_opener(handler)

# 获取cookie
r=opener.open('http://www.baidu.com/')

print(type(cookie))
for item in cookie:
    print ('Name = '+item.name)
    print ('Value = '+item.value)





