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
    pass
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
