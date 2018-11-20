# -*- coding: UTF-8 -*-
import requests
url = 'http://aima.cs.berkeley.edu/data/iris.csv'
u=requests.get(url)
localFile = open('iris.csv','w')
localFile.write(u.text)
localFile.close()
