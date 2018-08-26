# -*- coding: UTF-8 -*-
import numpy as np 
import statsmodels.tsa.stattools as ts
import pprint
import pandas as pd



def adf(x):
    result = ts.adfuller(x, 1)
    # 对上述函数求得的值进行语义描述
    dfoutput = pd.Series(result[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in result[4].items():
        dfoutput['Critical Value (%s)'%key] = value

    pprint.pprint(dfoutput)
    print("用Test Statistic的绝对值和1%、5%和10% Critical Value 的绝对值比较，若T绝对值大于上述某一个水平值，则表示在多少水平下是平衡序列。 反之，若T绝对值小于三者的绝对值，是非平稳序列。")


# 差分操作，例如d=[12,1],表示做12阶差分，
def diff_ts(ts, d):
    global shift_ts_list
    global last_data_shift_list
    shift_ts_list = []
    last_data_shift_list = []
    tmp_ts = ts
    for i in d:
        last_data_shift_list.append(tmp_ts[-i])
        print(last_data_shift_list)
        shift_ts = tmp_ts.shift(i)
        shift_ts_list.append(shift_ts)
        tmp_ts = tmp_ts - shift_ts
    tmp_ts.dropna(inplace=True)
    return tmp_ts

# 还原操作
def predict_diff_recover(predict_value, d):
    if isinstance(predict_value, float):
        tmp_data = predict_value
        for i in range(len(d)):
            tmp_data = tmp_data + last_data_shift_list[-i-1]
    elif isinstance(predict_value, np.ndarray):
        tmp_data = predict_value[0]
        for i in range(len(d)):
            tmp_data = tmp_data + last_data_shift_list[-i-1]
    else:
        tmp_data = predict_value
        for i in range(len(d)):
            try:
                tmp_data = tmp_data.add(shift_ts_list[-i-1])
            except:
                raise ValueError('What you input is not pd.Series type!')
        tmp_data.dropna(inplace=True)
    return tmp_data


x = np.array([1, 2, 3, 4, 5, 6, 7,9,9,9,9,9,8,8,8,8,8,8])
x=pd.DataFrame(x)
diff_ts(x, d=[1,1])
