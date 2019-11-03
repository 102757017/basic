# -*- coding: UTF-8 -*-
import os,time
import win32api,win32gui
import win32com.client
import subprocess


pipe = subprocess.Popen("test.exe", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True).stdout 
time.sleep(2)

try:
    while True:
            print("Press Ctrl-C to end")
            hld = win32gui.FindWindow( "#32770", "ArturDents CrackMe #2")
            #恢复最小化的窗口，防止最小化的情况下取不到坐标
            #win32gui.ShowWindow(hld,9)            
            #将窗口设置到最顶层
            #win32gui.SetForegroundWindow(hld)
            rect = win32gui.GetWindowRect(hld)
            print("扫描程序主窗口坐标：",rect)

            pos = win32api.GetCursorPos() #返回鼠标的坐标
            print ("鼠标位置：",pos)#打印坐标

            handle= win32gui.WindowFromPoint(pos)
            print ("鼠标处窗口的句柄：",handle)
            
            dif=[0,0]
            dif[0]=pos[0]-rect[0]
            dif[1]=pos[1]-rect[1]
            print ("控件相对坐标：",dif)#打印坐标

            pos2=[0,0]
            pos2[0]=rect[0]+dif[0]
            pos2[1]=rect[1]+dif[1]
            print ("重算鼠标位置：",pos2)#打印坐标


            
            time.sleep(3)

except  KeyboardInterrupt:
    print ('end....')
