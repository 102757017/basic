#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import pandas.io.sql as sql

#控制中文标题对齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


conn = sqlite3.connect('test.db')
# 创建一个Cursor:
cursor = conn.cursor()

# sql 命令
sql_cmd = "select 链接,时间 from table1 where 线报='{}' and 权限='{}'".format('快去买奶粉','20')
print(sql.read_sql(sql_cmd,conn))
