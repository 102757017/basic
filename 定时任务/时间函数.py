# -*- coding: UTF-8 -*-
import datetime
import time
import sched #定时任务模块


now = time.time()#时间戳都以自从1970年1月1日午夜（历元）经过了多长时间来表示。
print('time.time()',type(now))
print(now)
print('\n')


now = time.localtime()
print('time.localtime()',type(now))
print(now)
print('\n')


today = datetime.date.today()
print('datetime.date.today()',type(today))
print(today)
print('\n')

now = datetime.datetime.now()
print('datetime.datetime.now()',type(now))
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
print('datetime.datetime(2017,9,12,17,10,00,597383)',type(Timer))
print(Timer)
print('\n')

datetime_struct = datetime.datetime.fromtimestamp(time.time())
print('时间戳转换为datetime.datetime',type(datetime_struct))
print(datetime_struct)
print('\n')




#将时间戳转换成localtime
time_local = time.localtime(time.time())
print('time.localtime()将时间戳转换成时间数组localtime\n',time_local)
print('\n')

# 格式化成2016-03-20 11:45:39形式
now=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print('strftime()将时间数组time.localtime()转换为字符串\n',now)
print(type(now))
print('\n')


dt = "2016-05-05 20:28:54"
#转换成时间数组
timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
print('strptime()将字符串"2016-05-05 20:28:54"转换成时间数组\n',timeArray)
print('\n')
