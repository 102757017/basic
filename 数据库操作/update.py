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


#UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
#当字段名里面有空格时，需要将字段名用[]括起来
#例：#cursor.execute("update table1 set [ts num] = '81620-TBA6-A110-21-0001' where [wico num]=?",(part_num,))
cursor.execute("update table1 set 链接 = 'http://4',权限='10' WHERE 线报 = '吐槽'" )
cursor.execute("update table1 set 链接 = '{}',权限='{}' WHERE 线报 = '吐槽'".format('http://4','10') )


values = cursor.fetchall()
print(values)
print(len(values))



# 提交事务:execute后数据已经进入了数据库,但是如果最后没有commit 的话已经进入数据库的数据会被清除掉，自动回滚
conn.commit()

# 关闭Cursor:
cursor.close()

# 关闭数据库
conn.close()
