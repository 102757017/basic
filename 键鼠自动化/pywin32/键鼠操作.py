# -*- coding: UTF-8 -*-
import win32gui,win32con,win32api
import time






#获取鼠标位置
orgin=win32api.GetCursorPos()
print("鼠标原来的位置",orgin)
            

#设置鼠标位置
win32api.SetCursorPos((0,0))


#获取鼠标处窗口的句柄
handle= win32gui.WindowFromPoint(win32api.GetCursorPos())

              
#鼠标左键单击3次
times=3
while times:
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    times -= 1
                    

                
#快捷键Ctrl+C
win32api.keybd_event(17,0,0,0)      # Ctrl
win32api.keybd_event(67,0,0,0)     # C
win32api.keybd_event(67,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)


#Ctrl+C之后必须加延时，否则剪切板可能还未复制完数据
time.sleep(0.5)

