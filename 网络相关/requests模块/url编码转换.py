#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.parse
import pprint
import json


b1='''{"code":{"code":0,"message":"SUCCESS"},"data":{"dynStock":{"holdQuantity":0,"sellableQuantity":8,"sku":{";1627207:28320;":{"holdQuantity":0,"oversold":false,"sellableQuantity":8,"stock":8}},"stock":8,"stockType":"normal"}}}'''

print("url编码")
text = urllib.parse.quote(b1, 'utf-8')
print(text)


print("url反向转换")
text2=urllib.parse.unquote(text)
print(text2)


