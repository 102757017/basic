#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import win32process
import win32api
import win32con
import ctypes
import os, sys, string
import win32security
from ntsecuritycon import *
from multiprocessing import Queue
q=Queue(1)

TH32CS_SNAPPROCESS = 0x00000002

class PROCESSENTRY32(ctypes.Structure):
     _fields_ = [("dwSize", ctypes.c_ulong),
                 ("cntUsage", ctypes.c_ulong),
                 ("th32ProcessID", ctypes.c_ulong),
                 ("th32DefaultHeapID", ctypes.c_ulong),
                 ("th32ModuleID", ctypes.c_ulong),
                 ("cntThreads", ctypes.c_ulong),
                 ("th32ParentProcessID", ctypes.c_ulong),
                 ("pcPriClassBase", ctypes.c_ulong),
                 ("dwFlags", ctypes.c_ulong),
                 ("szExeFile", ctypes.c_char * 260)]
def getProcList():
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Process32First = ctypes.windll.kernel32.Process32First
    Process32Next = ctypes.windll.kernel32.Process32Next
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if Process32First(hProcessSnap,ctypes.byref(pe32)) == False:
        print("Failed getting first process.", file=sys.stderr)
        return
    while True:
        yield pe32
        if Process32Next(hProcessSnap,ctypes.byref(pe32)) == False:
            break
    CloseHandle(hProcessSnap)


def GetProcessModules( pid ):
    handle   = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid )
    hModule  = win32process.EnumProcessModules(handle)
    temp=[]
    for i in hModule:
        temp.append([hex(i),debugfile(win32process.GetModuleFileNameEx(handle,i))])
    win32api.CloseHandle(handle)
    return temp


def CloseProcess( pid ):
    handle   = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid )
    exitcode = win32process.GetExitCodeProcess( handle )
    win32api.TerminateProcess(handle, exitcode)
    win32api.CloseHandle(handle)


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

#提升进程权限，priv为权限类型，需要管理员权限才能提升进程权限
def AdjustPrivilege(priv):
     flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
     token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
     id = win32security.LookupPrivilegeValue(None, priv)
     privilege = [(id, win32security.SE_PRIVILEGE_ENABLED)]
     print("非0则提升了进程权限",win32security.AdjustTokenPrivileges(token, False, privilege))

#判断是否具有管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


#提升权限
def GetAuthority(priv):
     if is_admin():
        # 在此处填入需要执行的代码
        print("获取到了管理员权限")
        # 将本进程提升权限，获取DEBUG权限
        AdjustPrivilege(priv)
              
     else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

     a=input("等待")



if __name__ =='__main__':
     GetAuthority(win32security.SE_DEBUG_NAME)












