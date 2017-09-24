#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import time

# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('test.db')

# 创建一个Cursor:
cursor = conn.cursor()


#UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
cursor.execute("update table1 set 链接 = 'b',权限='b' WHERE 线报 = 'a'" )


values = cursor.fetchall()
print(values)
print(len(values))



# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()

# 关闭Cursor:
cursor.close()

# 关闭数据库
conn.close()
