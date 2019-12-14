#!/usr/bin/python
# -*- coding: UTF-8 -*-
import chardet
import urllib.parse
import sys
import locale
import html

print("当前系统shell标准输出的编码",sys.stdout.encoding)


print ("文件系统的编码",sys.getfilesystemencoding())



b='test str'
b=b.encode('ascii')
#含有中文的str无法用ASCII编码，因为中文编码的范围超过了ASCII编码的范围
print("将'test str'转换为ascii：")
print(b)
print(chardet.detect(b))
print("\n")


print("将ascii码的'test str'再转换为unicode码：")
b=b.decode('ascii')
print(b)
print("\n")


b="中文"
print("将'中文'转换为utf-8编码：",b.encode('utf-8'))
print("将'中文'转换为GBK编码：",b.encode('GBK'))
print("将'中文'转换为GB2312编码：",b.encode('GB2312'))
print("将'中文'转换为GB18030编码：",b.encode('GB18030'))
print(r"\x：是16进制的意思，\d：十进制；\o：八进制；后边跟两位，则表示单字节编码")
print("\n")
print("将'中文'转换为Unicode编码：",b.encode('unicode_escape'))
print("\n")




#解码
s='\\u653e\\u5f03\\u4fee\\u6539'
print("s:",s)
s2=s.encode('utf-8')
print("首先将string转换为bytes：",s2)
s3=s2.decode('unicode_escape')
print("然后将bytes进行解码：",s3)



print("\n")
print("屏蔽特殊的字符、比如如果url里面的空格或中文！url里面是不允许出现空格的")
b=urllib.parse.quote(b)
print(b)
print("\n")

print("url反向转换")
b=urllib.parse.unquote(b)
print(b)
print("\n")


'''
html中也存在转义符号，以下是一些例子
字符		转义字符
"		&quot;
&		&amp;
<		&lt;
>		&gt;
'''
url="htttp://taobao.com?id=123&ampuser=456"
print("原始url",url)
print("反转义",html.unescape(url))
html.unescape('a=1&amp;b=2')
