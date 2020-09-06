# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import pprint

#控制中文标题对齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

#显示所有列
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)    #设置整体宽度
pd.set_option('display.max_rows',20)   #设置最大行数
pd.set_option('display.max_columns', 100) #设置最大列数

#DataFrame创建方法有很多
#1.传入numpy数组创建
#dataframe中索引的概念与数据库不同，,index为行索引（行标题）,columns为列索引（相当于字段名）
df=pd.DataFrame(np.arange(16).reshape((4,4)),index=['a','b','c','d'],columns=['one','two','three','four'])
print(df)
print("shape：",df.shape)
print("行数：",df.index.size)
print("列数：",df.columns.size)
print("\n")

#按行变量dataframe
for row in df.iterrows():
   print(row[1]["one"], row[1]["two"])
print("\n")



print("切片前2行")
print(df.iloc[0:2])
print("\n")

print("切片one,two列")
print(df[["one","two"]])
print("\n")

print("shift函数将dataframe整体向下平移i个单元格创建一个新的dataframe,原dataframe自身不会产生变化，由此缺少的值用NaN填补")
df2=df.shift(1)
print(df2,"\n")

print("将one列转换为索引")
df2=df.set_index(['one'])
print(df2,"\n")

print("将one列,two均转换为索引")
df2=df.set_index(['one',"two"])
print(df2,"\n")

print("将索引转换为列")
df['index'] = df.index
print(df,"\n")

print("dataframe转换为numpy")
print(df.values)
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

#多列运算
print("多列运算")
df['c']= df.apply(lambda x: x['beijing'] + 2 * x['shanghai'], axis=1)
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


print("将dataframe排序")
a=df.sort_values(by="beijing" , ascending=False)
print(a,"\n")

#传入嵌套字典（字典的值也是字典）创建DataFrame
print("传入嵌套字典（字典的值也是字典）创建DataFrame")
nest_dict={'广州':{2015:10,2016:15,2017:12},'深圳':{2015:12,2016:13,2017:14}}  
df2=pd.DataFrame(nest_dict)
print(df2,"\n")

#连接表格
#inner:取交集
#outer:取并集
#left:左外连接
#right:右外连接
print("将两个表按行进行合并")
df3=pd.concat([df, df2],axis=1,join='outer')
print(df3,"\n")


print("将两个表按列进行合并")
df3=pd.concat([df, df2],axis=0)
print(df3,"\n")

print("append等同于concat(axis = 0)")
df3=df.append(df2)
print(df3,"\n")

print("多条件过滤数据")
df4=df3[(df3["beijing"]>102)&(df3["beijing"]<104)]
print(df4,"\n")

print('保留>101的数据，其它数据赋值NaN')
print(df.where(df>101),"\n")

print('保留>101的数据，其它数据赋值50')
print(df.where(df>101,50),"\n")

print('替换=101的数据')
print(df.replace(101,'女'),"\n")

print('根据字典替换数据')
df["shanghai"]=df["shanghai"].map({101:"女",102:"男"})
print(df,"\n")

print("#移动5个值，进行求平均数（5日均线）")
data = df=pd.DataFrame(np.arange(16),columns=['data'])
data['sum'] = data.rolling(5).mean()
print(data)

#读取excel，可以直接读取本地文件，也可以读取网络链接的文件
#header=0表示第0行是标题，第一行是数据
#names:指定自定义的列名
df=pd.read_excel("http://www.csindex.com.cn/uploads/file/autofile/indicator/000905indicator.xls?t=1588256726",header=0,names=["Date","Index Code","Index Chinese Name(Full)","Index Chinese Name","Index English Name(Full)","Index English Name","P/E1","P/E2","D/P1","D/P2"])
print(df,"\n")

#删除重复的行
df.drop_duplicates()
print(df,"\n")


#保存到csv文件
df.to_csv("stock.csv",encoding='utf_8')

#保存到excel文件
df.to_excel("stock.xls",encoding='utf_8')


#读取csv文件，使用自定义的列名
df=pd.read_csv("stock.csv",header=0,encoding="utf-8")
print(df,"\n")



#将数据以压缩格式存储
h5 = pd.HDFStore("Preprocessing",'w', complevel=4, complib='blosc')
h5['data'] = a
h5.close()

#载入数据
h5=pd.HDFStore("Preprocessing","r")
a=h5["data"]
h5.close()
