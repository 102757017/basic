# -*- coding: UTF-8 -*-
import requests
import json

url = 'http://httpbin.org/post'


data = "investCheckRequestParam=%s" %  json.dumps({"productId":"181333172208832","investSource":"0","investAmount":"18026.04","bizChannel":"secmkt","tradingType":"35"})
r = requests.post(url, data=data)
print(r.text)
