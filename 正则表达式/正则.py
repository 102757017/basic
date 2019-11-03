# -*- coding: UTF-8 -*-
from urllib import request   #导入request库中的urllib函数
import urllib
import re          #导入正则表达式库
import time        #导入延时函数库
#import androidhelper  #导入安卓API库

import gzip     #部分网页是采取gzip压缩的，直接读取会得到乱码，需要先解压


'''
正则表达式没有写好时可能导致回溯过多而死机，需要进行优化
确认使用贪婪匹配与非贪婪匹配那个效率高
尽量少用.*匹配，可以确定字符数量的明确数量，可以确定字符类型的明确类型
复杂的正则可以拆分多个简单的正则逐层匹配
'''

temp='''abcdefghijklmn12345()?op
sfq'''


#匹配除换行符之外的任何单字符1次以上
result = re.findall(r'abc(.+?)lmn', temp) #?可以实现非贪婪或最小匹配
print(result)

#匹配除换行符之外的任何单字符0次以上
result = re.findall(r'abc(.*?)d', temp)
print(result)

#匹配包括换行符的任何单字符1次以上
result = re.findall(r'abc([\s\S]+?)q', temp)
print(result)

#匹配不包括？和:的字符
result = re.findall(r'abc([^?:]+?)h', temp)
print(result)


#匹配1个换行/回车
result = re.findall(r'[\n\r]{1}', temp)
print(result)

#^$*+.()[]{}?|这些字符有特殊的含义，匹配这些字符请在字符串前加r
#匹配1个"\"需要加转意字符
result = re.findall(r'[\\]{1}', temp)
print(result)

#匹配连续的数字
result = re.findall(r'([0-9]+)', temp)
print(result)

#匹配3个数字
result = re.findall(r'[0-9]{3}', temp)
print(result)


#匹配1到3个数字
result = re.findall(r'[0-9]{1,3}', temp)
print(result)
