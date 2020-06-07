#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import time
import os

os.chdir(os.path.dirname(__file__))
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('test.db')

# 创建一个Cursor:
cursor = conn.cursor()

#计算当前日期,localtime表示使用本地时区
cursor.execute("SELECT date('now','localtime')")
values = cursor.fetchall()
print("当前日期:",values)

#计算当前时间
cursor.execute("SELECT datetime('now','localtime')")
values = cursor.fetchall()
print("当前时间:",values)


'''
替换	描述
%d	一月中的第几天，01-31
%f	带小数部分的秒，SS.SSS
%H	小时，00-23
%j	一年中的第几天，001-366
%J	儒略日数，DDDD.DDDD
%m	月，00-12
%M	分，00-59
%s	从 1970-01-01 算起的秒数
%S	秒，00-59
%w	一周中的第几天，0-6 (0 is Sunday)
%W	一年中的第几周，01-53
%Y	年，YYYY
'''
#计算当前的 UNIX 时间戳
cursor.execute("SELECT strftime('%s','now')")
values = cursor.fetchall()
print("当前时间戳:",values)


#根据日期获取时间戳
cursor.execute("SELECT strftime('%s','2020-06-07')")
values = cursor.fetchall()
print("6/7时间戳:",values)


#返回指定格式的时间
cursor.execute("SELECT strftime('%Y---%m---%d %H:%M:%S','now','localtime')")
values = cursor.fetchall()
print("指定格式的时间:",values)


#根据时间戳计算日期
cursor.execute("SELECT date(1092941466,'unixepoch', 'localtime')")
values = cursor.fetchall()
print("时间戳对应的日期:",values)


#根据时间戳计算时间
cursor.execute("SELECT datetime(1092941466, 'unixepoch', 'localtime')")
values = cursor.fetchall()
print("时间戳对应的时间:",values)



#应用
cursor.execute("select * from table1 where table1.时间<date('now')")
values = cursor.fetchall()
print(values)

# Cursor使用完成后应该尽快关闭，释放内存:
cursor.close()


# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()



# 关闭数据库
conn.close()
