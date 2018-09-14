#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # 在此处填入需要执行的代码
    print("获取到了管理员权限")
    a=input("")
    
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

