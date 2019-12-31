# -*- coding: UTF-8 -*-
import requests
import json
import pprint

url = 'http://httpbin.org/post'
# 截取封包内的Content-Length参数需要去除，Content-Length如果存在并且有效的话，则必须和消息内容的传输长度完全一致。（经过测试，如果过短则会截断，过长则会导致超时，requests会自动设置该参数
#Accept-Encoding: gzip, deflate, br;  注意requests不能解压br格式，会显示乱码，需去掉br或改用第三方模块
headers = {}
CookieJar = {}
proxies = {
    "http": "127.0.0.1:8888",
    "https": "127.0.0.1:8888"
}

data = "investCheckRequestParam=%s" % json.dumps(
    {"productId": "181333172208832", "investSource": "0", "investAmount": "18026.04", "bizChannel": "secmkt", "tradingType": "35"})
# verify https时是否进行证书验证
# allow_redirects 是否运行重定向
# proxies 代理服务器
# timeout connect 和 read 的超时时间,timeout判断的并不是整个请求的总时间，而是从与服务器连接成功后，客户端开始接受服务器的数据为计算起点的，卡在dns解析上的时间是不计算的
r = requests.post(url,
                  data=data,
                  headers=headers,
                  cookies=CookieJar,
                  verify=False,
                  allow_redirects=False,
                  timeout=(3, 7),
                  # proxies=proxies
                  )
print(r.text)

# 使用r.json()获取到的是dict格式，使用r.text获取到的是string格式
d = r.json()
pprint.pprint(d)
