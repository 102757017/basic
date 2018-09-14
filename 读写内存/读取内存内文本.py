#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from memorpy import *
import psutil
from GetDllAdress import GetDllAdress

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
p=processinfo("notepad.exe")

DllAdress=GetDllAdress(p,"MSCTF.dll")

#要查询的内存基址为"MSCTF.dll"+11E6E0
base_addr=DllAdress+0x11E6E0



#转换pid
winp=WinProcess.WinProcess(p)
addr=Address(process=winp,value=base_addr )
addr.symbolic_name=hex(base_addr)
addr.default_type = "bytes"


print(addr.read(10).decode("utf-16-le"))

#改写内存中的数据
addr.write("世界".encode("utf-16-le"))
print(addr.read(10).decode("utf-16-le"))
