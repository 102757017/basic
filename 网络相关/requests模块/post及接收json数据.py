# -*- coding: UTF-8 -*-
import requests
import json
import pprint

url = 'http://httpbin.org/post'


data = "investCheckRequestParam=%s" %  json.dumps({"productId":"181333172208832","investSource":"0","investAmount":"18026.04","bizChannel":"secmkt","tradingType":"35"})
r = requests.post(url, data=data)
print(r.text)

#使用r.json()获取到的是dict格式，使用r.text获取到的是string格式
d=r.json()
pprint.pprint(d)
