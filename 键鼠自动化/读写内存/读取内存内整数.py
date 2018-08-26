#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from memorpy import *
import psutil
import os
import time

#首先打开扫雷程序，启动计时器

def processinfo(processName):
    pids = psutil.pids()
    for pid in pids:
        #print(pid)
        p = psutil.Process(pid)
        #print(p.name)
        if p.name() == processName:
            print(pid)
            return pid


#要查询的计时器的内存地址
base_addr=0x0100579C

p=processinfo("winmine.exe")
print("pid:",p)
#转换pid
winp=WinProcess.WinProcess(p)
addr=Address(process=winp,value=base_addr )
addr.symbolic_name=hex(base_addr)
addr.default_type = "int"


print(addr.read(2))

#改写内存中的数据
addr.write(0)
print(addr.read(2))
