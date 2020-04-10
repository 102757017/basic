# -*- coding: UTF-8 -*-

try:
   print('try...')
   r = 10 / int('a')
   print('result:', r)

#捕获ValueError类的错误
except ValueError as e:
    print('ValueError错误信息是:', e)
    
#捕获ZeroDivisionError类的错误
except ZeroDivisionError as e:
    print('ZeroDivisionError错误信息是:', e)

#捕获所有类的错误，Python所有的错误都是从BaseException类派生的
except BaseException as e:
    print('BaseException错误信息是:', e)

#不管有没有出错， finally后面的语句是一定会执行的
finally:
    print('finally后面的语句是一定会执行的')


try:         
   raise ValueError("主动抛出异常，后面的代码不继续执行")
   print("后面的代码")
#捕获ValueError类的错误
except ValueError as e:
    print('ValueError错误信息是:', e)
