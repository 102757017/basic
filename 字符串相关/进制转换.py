#!/usr/bin/python
# -*- coding: UTF-8 -*-

n = 106
print("显示十进制数据：%d" % n)
print("显示八进制数据：%o" % n)
print("显示大写的十六进制数据：%X" % n)
print("显示小写的十六进制数据：%x" % n)
print("显示十进制对应的ascii码图形：%c" % n)
print("显示字符串：%s" % n)
print("\n")

# int本身不需要进制转换，print时可以打印出不同进制
# 使用Python内置函数：bin()、hex()可实现int到str的进制转换
print("10进制int转换为2进制字符串", bin(n), type(bin(n)))


print("10进制int转为16进制字符串", hex(n), type(bin(n)))


print("2进制int转换到16进制字符串", hex(0b10101011), type(hex(0b10101011)))


print("16进制int转换到2进制字符串", bin(0xab), type(bin(0xab)))


# 使用int()可实现str到int的进制转换
print("2进制字符串转为10进制int", int("10101011", 2))
print("16进制字符串转为10进制int", int("0xab", 16))
print("16进制字符串转为10进制int", int("ab", 16))
print("\n")


n = 65535
print("显示十进制数据：%d" % n)
print("显示大写的十六进制数据：%X" % n)
print("\n")

print("16进制字符串转为10进制int", int("FFFF", 16))
print("16进制字符串转为8位的2进制字符串，并且高位补0：", '{:08b}'.format(int("F", 16)))
print("16进制字符串转为8位的2进制字符串，:高位不补0：", '{:8b}'.format(int("F", 16)))
