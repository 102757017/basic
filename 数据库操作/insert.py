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
cursor.execute(r"insert into table1 (链接, 线报,权限,时间) values (NULL, 'Michael','1','2019-1-22')")
#cursor.execute("insert into table1 values (?,?,?,?)",(None,'a','a',time.strftime("%Y-%m-%d %H:%M")))

# 关闭Cursor:
cursor.close()


# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()



# 关闭数据库
conn.close()
