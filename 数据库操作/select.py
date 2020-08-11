#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import time
import os
import pprint

os.chdir(os.path.dirname(__file__))
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('test.db')

# 创建一个Cursor:
cursor = conn.cursor()


#where后面的多个条件用AND和OR连接运算，where前面的字段用逗号连接
#如果字段名内有空格，将字段名加[]
cursor.execute("select * from table1 where [线报]='{}' and 权限='{}'".format('快去撸毛','30'))

'''
模糊搜索
通配符	                        描述
%	                        替代一个或多个字符
_	                        仅替代一个字符
[charlist]	                字符列中的任何单一字符
[^charlist]或者[!charlist]	不在字符列中的任何单一字符
'''
cursor.execute("select * from table1 where [线报] like '{}'".format("快去%"))
#同一个cursor执行代码，后一个会覆盖前一个



#取结果集的下一行
values = cursor.fetchone()
print(values)
print(type(values))
print(len(values))
print('\n')


'''cursor只能用一次，即每用完一次之后记录其位置，
等到下次再取的时候是从游标处再取而不是从头再来，
fetch完所有的数据之后，这个cursor将不再有使用价值了，即不再能fetch到数据了。
'''
values = cursor.fetchall()
print(values)
print(type(values))
pprint.pprint(len(values))

# Cursor使用完成后应该尽快关闭，释放内存:
cursor.close()


# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()



# 关闭数据库
conn.close()
