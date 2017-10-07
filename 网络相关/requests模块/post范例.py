# -*- coding: UTF-8 -*-
import requests

url = 'http://httpbin.org/post'
d = {'key1': 'value1', 'key2': 'value2'}
r = requests.post(url, data=d)
print(r.text)
