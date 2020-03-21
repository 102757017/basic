#!/usr/bin/python
# -*- coding: UTF-8 -*-
import struct
import pprint
'''
在Python中list中的数据可能不会被存储为连续的字节块
将python值转换为C结构很重要，即将它们打包成连续的数据字节，或者将一个连续的字节块分解成Python对象,这可以用于处理存储在文件中或来自网络连接以及其他源的二进制数据
'''

'''
1byte(字节)=8bit,在32 位的系统上,各数据类型占用空间如下：
每个格式前可以有一个数字,表示这个类型的个数,如s格式表示一定长度的字符串,4s表示长度为4的字符串;4i表示四个int
格式符       C语言类型                 Python类型        占用字节(byte)
x            pad byte(填充字节)                    
c            char                      bytes             1             char相当于signed char或者unsigned char，但是这取决于编译器！
b            signed char               integer           1             signed char取值范围是 -128 到 127
B            unsigned char             integer           1             unsigned char 取值范围是 0 到 255
?            _Bool                     bool              1
h            short                     数字              2             取值范围为-2^15~2^15
H            unsigned short            数字              2             取值范围为0~2^16
i            int                       数字              4             取值范围为-2^31~2^31
I(大写的i)   unsigned int              数字               4             取值范围为0~2^32
l(小写的L)   long                      数字              4/8           32位python：int，long均占四字节，两者没有区别。64位python：int占四字节，long占8字节
L            unsigned long             数字              4             取值范围为0~2^32
q            long long                 数字              8             只适用于64位机器
Q            unsigned long long        数字              8
f            float                     数字              4
d            double                    数字              8
s            char[]                    bytes           自定义
p(小写)      char[]                    bytes           自定义 
P(大写)      void *                    long              
'''


# >表示big-endian，是指数据的低位保存在内存的高地址中，这是符合人平时的读写习惯的字节序
o=struct.pack('>2H', 3011,506)
print(o)

# <表示little-endian，是指数据的低位保存在内存的低地址中,一般X86 cpu采用Little Endian，而PowerPC处理器则采用了Big Endian
o=struct.pack('<2H', 3011,506)
print(o)

s=b"c30bfa01"
print(struct.pack('>8s', s))


#打包结构体数据
a=b'hello'
b="世界".encode("utf-8")
c=2
d=45.123
s=struct.pack('5s6sif',a,b,c,d)
print(s)

#解包结构体数据
o=struct.unpack('5s6sif',s)
print(o)