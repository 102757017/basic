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



#cursor.execute(r"insert into table1 (question, ans,result,time) values ('1', 'Michael','1','1')")
cursor.execute("insert into table1 values (?,?,?,?)",('a','a','a',time.strftime("%m/%d/%Y %H:%M")))

# 关闭Cursor:
cursor.close()


# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()



# 关闭数据库
conn.close()
