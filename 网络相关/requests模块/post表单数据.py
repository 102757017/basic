# -*- coding: UTF-8 -*-
import requests

url = 'http://httpbin.org/post'


'''
post参数内如果包含了%,传递时会进行转义。
以下为fiddler内截取的post参数，直接复制到到字典d内，%会被转义为%25，post结果会出错
action_mode=apply&username=admin&Pwd=YWRtaW4%3D&_pageStyle=pc
%3D需要转意为“=”,因此Pwd="YWRtaW4="

'''

d = {"data": '{"result": {"model": "Homepage", "action": "BuildClass", "parameters": {"id": -6}}}'}
r = requests.post(url, data=d)
print(r.text)
