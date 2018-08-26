# -*- coding: UTF-8 -*-
import numpy as np 
import statsmodels.tsa.stattools as ts
import pprint
import pandas as pd


x = np.array([1, 2, 3, 4, 5, 6, 7])
print(x.shape)
result = ts.adfuller(x, 1)
# 对上述函数求得的值进行语义描述
dfoutput = pd.Series(result[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
for key,value in result[4].items():
    dfoutput['Critical Value (%s)'%key] = value

pprint.pprint(dfoutput)
print("用Test Statistic的绝对值和1%、5%和10% Critical Value 的绝对值比较，若T绝对值大于上述某一个水平值，则表示在多少水平下是平衡序列。 反之，若T绝对值小于三者的绝对值，是非平稳序列。")

'''
adfuller(x, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False)[source]¶
 x: 序列，一维数组
 maxlag：差分次数
 regresion:{c:只有常量，
            ct:有常量项和趋势项，
            ctt:有常量项、线性和二次趋势项，
            nc:无任何选项}
 autolag:{aic or bic: default, then the number of lags is chosen to minimize the corresponding information criterium
 '''
