#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from memorpy import *
import psutil

#根据进程名获取进程pid，如果没有该进程，则返回None
def processinfo(processName):
    pids = psutil.pids()
    for pid in pids:
        # print(pid)
        p = psutil.Process(pid)
        # print(p.name)
        if p.name() == processName:
            print(pid)
            return pid


#预先打开记事本
#要查询的内存地址
base_addr=0x7FFBCA1CE6E0


p=processinfo("notepad.exe")
#转换pid
winp=WinProcess.WinProcess(p)
addr=Address(process=winp,value=base_addr )
addr.symbolic_name=hex(base_addr)
addr.default_type = "bytes"


print(addr.read(10).decode("utf-16-le"))

#改写内存中的数据
addr.write("世界".encode("utf-16-le"))
print(addr.read(10).decode("utf-16-le"))
