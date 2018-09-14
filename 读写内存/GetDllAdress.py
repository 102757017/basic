#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import win32process
import win32api
import win32con
import os



def GetProcessModules( pid ):
    handle   = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid )
    hModule  = win32process.EnumProcessModules(handle)
    temp=[]
    for i in hModule:
        temp.append([hex(i),debugfile(win32process.GetModuleFileNameEx(handle,i))])
    win32api.CloseHandle(handle)
    return temp


def debugfile(file):
    if (file.split("\\")[-1]=="smss.exe"):
        file = "C:\\WINDOWS\\system32\\smss.exe"
        return file
    elif (file.split("\\")[-1]=="csrss.exe"):
        file = "C:\\WINDOWS\\system32\\csrss.exe"
        return file
    elif (file.split("\\")[-1]=="winlogon.exe"):
        file = "C:\\WINDOWS\\system32\\winlogon.exe"
        return file
    else:
        return file




#输入进程pid和dll文件名，获得dll的内存基址
def GetDllAdress(pid,dllname):
     dlls=GetProcessModules(pid)
     for dllinfo in dlls:
          if os.path.split(dllinfo[1])[1]==dllname:
               print(dllinfo[0],type(dllinfo[0]))
               #获取的地址为16进制的字符串，将字符串转换为int类型
               address=int(dllinfo[0],16)
               return address



if __name__ =='__main__':
     GetDllAdress(2064,"MSCTF.dll")












