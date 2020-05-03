# -*- coding: UTF-8 -*-
import datetime
import time
from datetime import timedelta
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


d=timedelta(minutes=2)
print(d,type(d))

print(datetime.datetime.now()-timedelta(days=2))
print('\n')


print("生成时间序列")
import pandas as pd
'''
频率字符串(freq）： 

别名	Offset类型	描述
B	BDay	工作日
C	CDay	定制工作日
D	Day	日历日
W	Week	每周
M	MonthEnd	每月最后一个日历日
SM	SemiMonthEnd	每月15日和最后一个日历日
BM	BMonthEnd	每月15日和最后一个工作日
CBM	CBMonthEnd	定制每月最后一个日历日
MSS	MonthBegin	每月第一个日历日
SMS	SemiMonthBegin	每月1日和15日
BMS	BMonthBegin	每月第一个工作日
CBMS	CBMonthBegin	定制每月第一个工作日
Q	QuarterEnd	每季度最后一个日历日
BQ	BQuarterEnd	每季度最后一个工作日
QS	QuarterBegin	每季度第一个日历日
BQS	BQuarterBegin	每季度第一个工作日
A,Y	YearEnd	每年最后一个日历日
BA,BY	BYearEnd	每年最后一个工作日
AS,YS	YearBegin	每年第一个日历日
BAS,BYS	BYearBegin	每年第一个工作日
H	Hour	每小时
BH	BusinessHour	每工作小时
T,min	Minute	每分钟
S	Second	每秒
L,ms	Milli	毫秒
U,us	Micro	微秒
N	Nano	纳秒
'''

df=pd.date_range('2020-4-26',datetime.date.today(),freq='B').strftime("%Y-%m-%d")
print(df)

df=pd.date_range('2019-1-26',datetime.date.today(),freq='Q').strftime("%Y-%m-%d")
print(df)
