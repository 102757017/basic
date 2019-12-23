# -*- coding: UTF-8 -*-
import requests

url = 'http://httpbin.org/post'


'''
post参数内如果包含了%,传递时会进行转义。
以下为fiddler内截取的post参数，直接复制到到字典d内，%会被转义为%25，post结果会出错
action_mode=apply&username=admin&Pwd=YWRtaW4%3D&_pageStyle=pc
%3D需要转意为“=”,因此Pwd="YWRtaW4="
'''
# 截取封包内的Content-Length参数需要去除，Content-Length如果存在并且有效的话，则必须和消息内容的传输长度完全一致。（经过测试，如果过短则会截断，过长则会导致超时，requests会自动设置该参数
headers = {}
CookieJar = {}
proxies = {
    "http": "127.0.0.1:8888",
    "https": "127.0.0.1:8888"
}

d = {"data": '{"result": {"model": "Homepage", "action": "BuildClass", "parameters": {"id": -6}}}'}
# verify https时是否进行证书验证
# allow_redirects 是否运行重定向
# proxies 代理服务器
# timeout connect 和 read 的超时时间,timeout判断的并不是整个请求的总时间，而是从与服务器连接成功后，客户端开始接受服务器的数据为计算起点的，卡在dns解析上的时间是不计算的
r = requests.post(url,
                  data=d,
                  headers=headers,
                  cookies=CookieJar,
                  verify=False,
                  allow_redirects=False,
                  timeout=(3, 7),
                  #proxies=proxies
                  )
print(r.text)
