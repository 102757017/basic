# -*- coding: UTF-8 -*-
import requests
import json
import pprint

url = 'https://rpc.zhongtuobang.com/pc/pv?ts=5a79c48f2099c8656d3fa769'


'''
post参数内如果包含了%,传递时会进行转义。
以下为fiddler内截取的post参数，直接复制到到字典d内，%会被转义为%25，post结果会出错
action_mode=apply&username=admin&Pwd=YWRtaW4%3D&_pageStyle=pc
%3D需要转意为“=”,因此Pwd="YWRtaW4="
'''

header={'Accept': 'application/json',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,en-US;q=0.8',
 'Connection': 'keep-alive',
 'Content-Length': '339',
 'Content-Type': 'application/json;charset=UTF-8',
 'Host': 'rpc.zhongtuobang.com',
 'Origin': 'https://wx.zhongtuobang.com',
 'Referer': 'https://wx.zhongtuobang.com/payment/ddk',
 'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; ONEPLUS A3000 Build/NMF26F; '
               'wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
               'Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile '
               'Safari/537.36 MicroMessenger/6.5.23.1180 NetType/WIFI '
               'Language/zh_CN',
 'X-Requested-With': 'com.tencent.mm'}

fiddler={"request_type":"share","events_attr":{"tjData":{"openURL":"https://wx.zhongtuobang.com/payment/ddk","shareURL":"https://wx.zhongtuobang.com/payment/ddk?fromUserID=10709156","d":"ztb_share_wx_friends"}},"url":"https://wx.zhongtuobang.com/payment/ddk","ref_url":"https://wx.zhongtuobang.com/","client_time":1517929780467,"channel":"5ftj2c"}
r = requests.post(url, data=fiddler)
print(r.text)
