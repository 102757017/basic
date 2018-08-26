# -*- coding: UTF-8 -*-
import configparser
import os


    
#在传递键值对数据时，会将键名 全部转化为小写
conf = configparser.ConfigParser()
if os.path.isfile("seting.ini"):
    conf.read("seting.ini")
    level  = conf.get("logging", "level")
    host=conf.get("mysql","host")
    port=conf.get("mysql","port")
else:
    conf.add_section('logging')
    conf.set('logging', 'level', '20')
    conf.add_section('mysql')
    conf.set('mysql', 'host', '127.0.0.1')
    conf.set('mysql', 'port', '80')
    conf.write(open('seting.ini', 'w'))


port=conf.get("mysql","port")
print('获取指定的section下的option', type(port), port)

