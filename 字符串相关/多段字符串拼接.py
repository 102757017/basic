# -*- coding: UTF-8 -*-
import os
import sys
import urllib.parse
import pprint
import json

os.chdir(sys.path[0])


x_itemid = "XXXX"
x_uid = "XXXX"
submitref = "XXXX"
sparam1 = "XXXX"
sparam2 = "XXXX"

confirm_url = "https://buy.taobao.com/auction/confirm_order.htm?x-itemid=%s&x-uid=%s&submitref=%s&sparam1=%s&sparam2=%s" % (
    x_itemid, x_uid, submitref, sparam1, sparam2)
print(confirm_url)

print('我叫{}，今年{}岁。'.format('小明', 18))

print('我叫{0}，今年{1}岁。他们都叫我{0}'.format('小明', 18))

print('我大哥是{name}，今年{age}岁。'.format(name='阿飞', age=20))

# 使用元组传参,前面要加*号
infos = ('钢铁侠', 66, '小辣椒')
print('我是{}，身价{}亿。'.format(*infos))
print('我是{2}，身价{1}亿。'.format(*infos))

# 使用字典传参,前面要加*号
infos = ['鹰眼', "箭", '黑寡妇']
print('我是{}，我用{}。'.format(*infos))
print('我是{2}，我爱{0}。'.format(*infos))

# 使用字典传参，前面要加**号
venom = {'name': '毒液', 'weakness': '火'}
print('我是{name}，我怕{weakness}。'.format(**venom))


# 方括号用法：用列表传递位置参数
infos = ['阿星', 9527]
food = ['霸王花', '爆米花']
print('我叫{0[0]}，警号{0[1]}，爱吃{1[0]}。'.format(infos, food))

# 混合使用多种数据
names = ['皮卡丘']
dic = {'name': '妙蛙花'}
skills = ('十万伏特', '飞叶快刀')
text = '我是{names[0]}，我会{skills[0]}。我是{dic[name]}，我会{skills[1]}。'
text = text.format(names=names, skills=skills, dic=dic)
print(text)


# 对于非数字类型，精度指定最大字段宽度
print('{0:.3}'.format('哇哈哈哈哈哈'))

# 转换为二进制
print("10进制int转换为2进制字符串", '{:b}'.format(255))
print("10进制int转为8进制字符串", '{:o}'.format(255))
print("10进制int转换到16进制字符串", '{:x}'.format(255))
print("10进制int用Unicode解码为字符串", '{:c}'.format(255))

# int转换为二进制字符串并且高位补0
print("10进制int转换为8位的2进制字符串,数字补零 (填充左边, 宽度为8)：", '{:0>8b}'.format(10))
print("10进制int转换为8位的2进制字符串,数字补X (填充右边, 宽度为8)：", '{:X<8b}'.format(10))

# 科学记数法 默认精度为 6 位
print('{:e}'.format(1234567.1234567))

# 百分比格式显示
print('{:%}'.format(1))

# 保留3位小数
print('	{:.3f}'.format(3.1415926))

# 带符号保留3位小数
print('	{:+.3f}'.format(-3.1415926))

# 逗号分隔的数字
print('{:,}'.format(1234567789))