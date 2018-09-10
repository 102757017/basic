#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from memorpy import *
import psutil


print(windll.kernel32) 
print(hex(windll.kernel32.GetModuleHandleA("kernel32.dll")))
