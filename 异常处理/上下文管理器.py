# -*- coding: UTF-8 -*-

'''
with语句时用于对try except finally 的优化，让代码更加美观，打开文件的时候，为了能正常释放文件的句柄，
都要加个try，然后再finally里把f close掉，但是这样的代码不美观，finally就像个尾巴，一直托在后面，
尤其是当try里面的语句时几十行
with还支持文件锁，进程锁、数据库连接等操作
'''
with open('test.txt', 'r') as f:
   data = f.read()
