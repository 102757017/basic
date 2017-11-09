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
print(now.tm_year)
print(now.tm_mon)
print(now.tm_mday)
print(now.tm_hour)
print(now.tm_min)
print(now.tm_sec)
print(now.tm_wday)
print(now.tm_yday)
print(now.tm_isdst)
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

timestamp = datetime.datetime.timestamp(datetime_struct)
print('datetime.datetime转换为时间戳',type(timestamp))
print(timestamp)
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

#时间数组转换成时间戳,时间戳的单位是秒
timeStamp=int(time.mktime(timeArray))
print('time.mktime()将时间数组转换为时间戳\n',timeStamp)
print('\n')


