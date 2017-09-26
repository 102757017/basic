# -*- coding: UTF-8 -*-
import datetime
import time
import sched #定时任务模块


today = datetime.date.today()
print(type(today))
print(today)
print('\n')

now = time.time()#时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示。
print(type(now))
print(now)
print('\n')


now = time.localtime()
print(type(now))
print(now)
print('\n')


# 格式化成2016-03-20 11:45:39形式
now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(type(now))
print(now)
print('\n')

now = datetime.datetime.now()
print(type(now))
print(now)
print(now.year)
print(now.month)
print(now.day)
print(now.hour)
print(now.minute)
print(now.second)
print(now.microsecond)
print('\n')

Timer =datetime.datetime(2017,9,12,17,10,00,597383)
print(type(Timer))
print(Timer)
