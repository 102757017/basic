# -*- coding: UTF-8 -*-
from urllib import request   #导入request库中的urllib函数
import urllib
import re          #导入正则表达式库
import time        #导入延时函数库
#import androidhelper  #导入安卓API库

import gzip     #部分网页是采取gzip压缩的，直接读取会得到乱码，需要先解压



temp= open(r"D:\我的文档\桌面\aaa.txt",'r')
a=temp.read()
temp.close()

result = re.findall(r'<a href="(.+?)"  class="s xst" target="_blank">(.+?)</a>\n - \[阅读权限 <span class="xw1">([0-9]+)', a)


print(result)
