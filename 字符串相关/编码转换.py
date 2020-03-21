#!/usr/bin/python
# -*- coding: UTF-8 -*-
import chardet
import urllib.parse
import sys
import locale
import html
from binascii import a2b_hex,b2a_hex


print("当前系统shell标准输出的编码", sys.stdout.encoding)
print("文件系统的编码", sys.getfilesystemencoding())

# 使用encode()将str转换为bytes，bytes就是一串hex数据，主要用于网络传输，同一个str根据编码方式不同可以转换为不同的bytes，web传输一般用UTF-8编码，串口传输一般用ASCII编码
# 使用decode()将bytes转换为str


b = 'hello world'
# 含有中文的str无法用ASCII编码，因为中文编码的范围超过了ASCII编码的范围
print(r"'hello world'→",b.encode('ascii'),r"encode('ascii'):")
def trans(s):
    return "b'%s'" % ''.join('\\x%.2x' % x for x in s)
print(r"b'hello world'==",trans(b'hello world'))
print(r"'f1ff'→",a2b_hex("f1ff"),"a2b_hex()")
print("\n")

b = "中文"
print(r"'中文'→", b.encode('utf-8'),r"encode('utf-8'):")
print(r"'中文'→", b.encode('GBK'),r"encode('GBK'):")
print(r"'中文'→", b.encode('GB2312'),r"encode('GB2312'):")
print(r"'中文'→", b.encode('GB18030'),r"encode('GB18030'):")
print(r"'中文'→", b.encode('unicode_escape'),r"encode('Unicode'):")


s = '\\u4e2d\\u6587'
print(r"'\\u4e2d\\u6587'→",s.encode('ascii'),r"encode('ascii'):")
print(r"\x：是16进制的意思，\d：十进制；\o：八进制；后边跟两位，则表示单字节编码")
print(r"\x表示十六进制的bytes型变量,0x表示十六进制的int变量")
print("\n")


print(r"b'hello world'→",b'hello world'.decode('ascii'),r"decode('ascii'):")
print(r"b'\x4a'==b'J'→0x4a==",ord(b'J'),"ord()",)
#多位数的转换
#signed:表示是否要区分正负数含义
#byteorder:big代表正常顺序，即f1ff。little反之，代表反序fff1；
print(r"b'\xff\x00'→0xff00==",int.from_bytes(b'\xff\x00', byteorder='big', signed=False),"int.from_bytes()")
print(r"b'\xf1\xff'→",b2a_hex(b'\xf1\xff'),"b2a_hex()")


print("\n")
print("0x4a→",chr(0x4a),"chr()")
print("0x4a→",bytes([0x4a]),"bytes([]):")
print("0xf1f2f3==15856371→",(15856371).to_bytes(3,byteorder='big', signed=False),"int.to_bytes(byteorder='big')")
print("0xf1f2f3==15856371→",(15856371).to_bytes(4,byteorder='big', signed=False),"int.to_bytes(4)")
print("0xf1f2f3==15856371→",(15856371).to_bytes(3,byteorder='little', signed=False),"int.to_bytes(byteorder='little')")


print("\n")
print("屏蔽特殊的字符、比如如果url里面的空格或中文！url里面是不允许出现空格的")
b = urllib.parse.quote(b)
print(b)
print("\n")

print("url反向转换")
b = urllib.parse.unquote(b)
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
url = "htttp://taobao.com?id=123&ampuser=456"
print("原始url", url)
print("反转义", html.unescape(url))
html.unescape('a=1&amp;b=2')
