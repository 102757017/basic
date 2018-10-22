# -*- coding: UTF-8 -*-
import os
import sys
import pickle
#python中几乎所有的数据类型（列表，字典，集合，类等）都可以用pickle来序列化

os.chdir(sys.path[0])
sample={"1":"a","2":"b","3":"d"}
#将sample对象保存为文件
f = open('pickle_sample', 'wb')
pickle.dump(sample, f)
f.close()

#从文件中读取sample对象
f = open('pickle_sample', 'rb')
load=pickle.load(f)
print(load)