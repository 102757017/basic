# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np

#DataFrame创建方法有很多
#1.传入numpy数组创建,index为索引,columns为列标题
df=pd.DataFrame(np.arange(16).reshape((4,4)),index=['a','b','c','d'],columns=['one','two','three','four'])
print(df)
print("shape：",df.shape)
print("行数：",df.index.size)
print("列数：",df.columns.size)
print("\n")

#2.用传入等长列表组成的字典来创建
print("用传入等长列表组成的字典来创建")
data={'c':['1','2'],'a':['5','6']}
df=pd.DataFrame(data)
print(df,"\n")

#如果指定了columns名称，则会按照指定顺序创建
print("如果指定了columns名称，则会按照指定顺序创建")
df=pd.DataFrame(data,columns=['c','a'])
print(df,"\n")

#3.传入嵌套字典（字典的值也是字典）创建DataFrame
print("传入嵌套字典（字典的值也是字典）创建DataFrame")
nest_dict={'shanghai':{2015:100,2016:101,2017:102},'beijing':{2015:102,2016:103,2017:104}}  
df=pd.DataFrame(nest_dict)
print(df,"\n")

#增加一列,标题为c，内容都为1
print("增加一列,标题为c，内容都为1")
df['c']=1
print(df,"\n")

#修改c列
print("修改c列")
df['c'][2016]=4
print(df,"\n")


#删除c列
print("删除c列")
del df['c']
print(df,"\n")



#删除行标题为2015、2016这两行
print("删除行标题为2015、2016这两行")
data = df.drop([2015,2016])
print(data,"\n")

#将dataframe整体向下平移1个单元格创建一个新的dataframe,原dataframe自身不会产生变化，由此缺少的值用NaN填补
#只有数据内容产生了移动，索引名不会同时产生移动
print("将dataframe整体向下平移1个单元格")
a=df.shift(1)
print(a,"\n")

a=df.shift(-1)
print("将dataframe整体向上平移1个单元格")
print(a,"\n")

#将数据以压缩格式存储
h5 = pd.HDFStore("Preprocessing",'w', complevel=4, complib='blosc')
h5['data'] = a
h5.close()

#载入数据
h5=pd.HDFStore("Preprocessing","r")
a=h5["data"]
