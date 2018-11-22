#!/usr/bin/python
# # -*- coding: UTF-8 -*-
import numpy as np


#当array太大时会产生内存错误，因此处理大型矩阵可以使用np.memmap将矩阵映射到文件，在32位的系统上映射文件不能大于2GB
#r:只读模式
#r+：可读写
#w+：创建或是覆盖已有文件
#c：Copy-on-write: assignments affect data in memory, but changes are not saved to disk. The file on disk is read-only.
f= np.memmap('a.npz', dtype='uint8', mode='r+', shape=(2,2))
print(type(f))
print(f)
f[0][0]=1
#将array中的改变写入文件
f.flush()
print(f)
