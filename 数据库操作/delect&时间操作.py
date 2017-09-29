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


#时间比较
#cursor.execute("delete from table1 where table1.time< '09/03/2017 16:12' ")
cursor.execute("delete from table1 where table1.线报= 'a' ")




# Cursor使用完成后应该尽快关闭，释放内存:
cursor.close()


# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()



# 关闭数据库
conn.close()
