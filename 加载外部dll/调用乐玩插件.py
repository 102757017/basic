# -*- coding: UTF-8 -*-
from comtypes import client

'''
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    #调用前必须先注册dll
    os.system("regsvr32 %~sdp0lw.dll")
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
'''






#乐玩插件只支持32位的python，不支持64位的python
lw = client.CreateObject("lw.lwsoft3")
print(lw.ver())

#获取鼠标所指窗口的句柄
hwnd=lw.GetMousePointWindow()
print(hwnd)

#获取该窗口的类名
title=lw.GetWindowClass(hwnd)
print(title)
