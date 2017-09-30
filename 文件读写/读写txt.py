# -*- coding: UTF-8 -*-
import os
import sys
os.chdir(sys.path[0])
f = open('覆盖了吗.txt','w') # 覆盖模式
f.write('不会换行') # 不会换行哦
f.close()
f = open('覆盖了吗.txt','w') # 覆盖模式
f.write('不会换行') # 不会换行哦
f.close()
f = open('覆盖了吗.txt','w') # 覆盖模式
f.write('不会换行') # 不会换行哦
f.close()


f = open('filename.txt','a') # 追加模式
f.write('我会换行\n') # 不会换行哦
f.close()
f = open('filename.txt','a') # 追加模式
f.write('我不会换行') # 不会换行哦
f.close()




f = open('filename.txt','r') # 读模式
print('一次只读取一行')
print(f.readline()) # 一次只读取一行
print('\n')
f.close()


f = open('filename.txt','r') # 读模式
print('一次读取整个文件')
print(f.read()) # 一次读取整个文件
print('\n')
f.close()
