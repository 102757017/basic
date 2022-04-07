# -*- coding: UTF-8 -*-
import win32gui,win32con,win32api,win32ui
import subprocess
import time


#获取指定句柄窗口的截图
def getno(hwnd):
    #返回参数所指定的窗口的设备环境
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # 通过设备描述表创建创建一个与应用程序的当前显示器兼容的内存设备上下文环境，如果成功，则返回内存设备上下文环境的句柄
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取桌面分辨率
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]

    ck=win32gui.GetClientRect(hwnd)
    ck2 = win32gui.GetWindowRect(hwnd)
    w=ck[2]
    h=ck[3]
    b_h=ck2[3]-ck2[1]-h


    print(w,h)# 图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, b_h), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, "截图.png")



if __name__=="__main__":
    pipe = subprocess.Popen("test.exe", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True).stdout
    time.sleep(2)

    
    #查询句柄
    #第一个参数为父窗口类名，不知道类名时取None,在不同的系统环境下，r12可能变化
    #第二个参数为窗口标题名，不知道标题时取None，FindWindow函数不能模糊查找
    hwnd = win32gui.FindWindow( "#32770", "ArturDents CrackMe #2")
    getno(hwnd)
