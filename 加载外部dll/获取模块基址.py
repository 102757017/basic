#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from ctypes import *  

#加载dll，注意dll的版本，32位的dll需要用32位的python加载，64位的dll需要用64位的python加载
lib=windll.LoadLibrary("lw.dll")
print(lib)
