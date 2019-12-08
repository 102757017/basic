# -*- coding: UTF-8 -*-
import requests
import pprint
import demjson


#json的格式是字符串，在网络传输的时候用的是字符串
#要查询json 对应key的值，需要将json转换为dict格式
string='''{"code":{"code":0,"message":"SUCCESS"},"data":{"dynStock":{"holdQuantity":0,"sellableQuantity":8,"sku":{";1627207:28320;":{"holdQuantity":0,"oversold":false,"sellableQuantity":8,"stock":8}},"stock":8,"stockType":"normal"}}}'''

#json转换为dict
d = demjson.decode(string)
pprint.pprint(d)

#dict转json
d = demjson.encode(d)
print(d)


f=open('json.txt','rb')
string=f.read()
d = demjson.decode(string)
print(d.keys())
