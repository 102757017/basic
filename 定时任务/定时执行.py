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

Timer = sched_Timer=datetime.datetime(2017,9,12,17,10,00)
print(type(Timer))
print(Timer)

print(datetime.datetime.now()>datetime.datetime(2017,9,8,21,27,00))



flag=1
while flag:
        now = datetime.datetime.now()
        #不能自己使用datetime.datetime.now()==设定时间，因为now()是带毫秒的
        if now.hour==21 and now.minute==55:                
                print("到达指定时间，开始执行代码")
                #此处加入要执行的代码
                flag=0
print("执行完毕")
