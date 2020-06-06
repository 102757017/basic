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


#自增字段必须插入空值，以下两种方式插入空值的方法是不一样的。
dt=time.strftime("%m/%d/%Y %H:%M")

#不使用变量
cursor.execute(r"insert into table1 (链接, 线报,权限,时间) values ('http://5', '吐槽','10','2019-1-22')")
#使用变量
cursor.execute(r"insert into table1 (链接, 线报,权限,时间) values ('{}','{}','{}','{}')".format('http://5', '吐槽','10','2019-1-22'))

#防止插入重复数据:先将组合字段设置为唯一键或联合主键，再使用insert or ignore插入数据，忽略已存在数据。若使用insert or replace则可以替换已存在的数据
cursor.execute(r"insert or ignore into table1 (链接, 线报,权限,时间) values ('http://5', '吐槽','10','2019-1-22')")

# 关闭Cursor:
cursor.close()


# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()



# 关闭数据库
conn.close()
