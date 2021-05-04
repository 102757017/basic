#!/usr/bin/python
# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import datetime


x=["2020-05-01","2020-05-02","2020-05-03","2020-05-04"]
x=[datetime.datetime.strptime(i, "%Y-%m-%d").date() for i in x]
print(x)
y=[1,2,4,3]

plt.plot(x,y,color='red')

plt.show()
