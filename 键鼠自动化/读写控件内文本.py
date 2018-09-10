# -*- coding: UTF-8 -*-
import win32gui,win32con,win32api
import subprocess
import time


def getno():
    #查询句柄
    #第一个参数为父窗口类名，不知道类名时取None,在不同的系统环境下，r12可能变化
    #第二个参数为窗口标题名，不知道标题时取None，FindWindow函数不能模糊查找
    hld = win32gui.FindWindow( "#32770", "ArturDents CrackMe #2")
    HwndEx=None
    rect=None
    if hld>0:
        try:
            while rect!=(51, 39):
                #获取hld子窗口内的控件句柄，类名为edit，该函数只能查收下一级子窗口内控件的句柄，查询孙子窗口的句柄需要进行嵌套查询
                #参数1：父窗口句柄
                #参数2：子窗口句柄,从该子窗口开始向后查找，如果取None，则全部遍历一次
                #参数3：查找窗口的类名，不知道类名时取None
                #参数4：查找窗口的的标题,不知道类名时取None，FindWindowEx函数不能模糊查找
                HwndEx=win32gui.FindWindowEx(hld,HwndEx,"Edit",None)
                print("控件句柄：",HwndEx)

                #获取该句柄对应控件的左上角和右下角的坐标，获取的坐标为屏幕坐标
                rect = win32gui.GetWindowRect(HwndEx)
                

                #将屏幕坐标转换为相对于父窗口的坐标
                rect=win32gui.ScreenToClient(hld,(rect[0],rect[1]))
                print("控件左上角在父窗口内的坐标：",rect)

                #获取该句柄对应控件的长度和高度
                ck = win32gui.GetClientRect(HwndEx)
                print("控件的长度和高度：",ck)
                print("\n")



            # 向控件内写入文本，第三个参数不使用，取0
            win32gui.SendMessage(HwndEx, win32con.WM_SETTEXT, 0, "hello world")

            # 向控件内写入回车
            win32gui.PostMessage(HwndEx, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(HwndEx, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

            # 获取控件内文本的长度，要加上截尾的字节
            buf_size = win32gui.SendMessage(HwndEx, win32con.WM_GETTEXTLENGTH, 0, 0) + 1
            print(buf_size)

            # 生成buffer对象
            str_buffer = win32gui.PyMakeBuffer(buf_size*2)

    
            # 获取buffer,得到类似于16进制的东西，将结果传输给str_buffer，参数3控制获取长度
            win32api.SendMessage(HwndEx, win32con.WM_GETTEXT, buf_size, str_buffer)
            # 将buffer转为字符串
            string = bytes(str_buffer).decode('utf-16')
            print("目标控件内的文本为：",string)
        except BaseException as e:
            print('错误信息：',e)
    
    else:
        print("错误！！程序未启动")

if __name__=="__main__":
    pipe = subprocess.Popen("test.exe", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True).stdout 
    time.sleep(2)
    getno()
