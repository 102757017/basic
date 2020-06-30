#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#解决中文乱码问题
from matplotlib.font_manager import FontProperties 
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10)

df=pd.read_excel("http://www.csindex.com.cn/uploads/file/autofile/indicator/000905indicator.xls?t=1588256726",header=1,names=["Date","Index Code","Index Chinese Name(Full)","Index Chinese Name","Index English Name(Full)","Index English Name","P/E1","P/E2","D/P1","D/P2"],encoding = 'utf_8')
df["Date"]=pd.to_datetime(df["Date"])

#将日期列转换为索引
df=df.set_index(["Date"])


#df对象的索引会传给matplotlib，用来绘制X轴
df[["P/E1","P/E2"]].plot()
plt.legend(loc='best')
plt.show()
