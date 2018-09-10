# -*- coding: UTF-8 -*-
from pywinauto.application import Application
import time



#连接要操作程序的PID
#app = Application().connect(process=11548)


#连接窗口句柄也可以
#app = Application().connect(handle=0x010f0c)

#自绘窗口设置(backend="uia")
#Win32 API窗口设置(backend="win32") 
#使用标题、类型等匹配
#app = Application(backend="win32").connect(title_re="无标题 - 记事本", class_name="Notepad")



# 对于Windows中自带应用程序，直接执行，对于外部应用应输入完整路径
app = Application(backend="uia").start('notepad.exe')
#描述Notepad.exe进程中的窗口
#dlg_spec = app.UntitledNotepad
#print(dlg_spec)

dlg_spec = app.window(title='无标题 - 记事本')

#将窗口最大化
dlg_spec.maximize()

#Unicode字符和特殊符号的使用可以通过字典中的项目进行访问（尤其对于中文来说，找不到相应的控件就对其进行字典访问）
dlg_spec = app['无标题 - 记事本']

#显示控件树，可用的最佳匹配名显示为树中每个控件的列表
dlg_spec.print_control_identifiers()


app[' 无标题 - 记事本 '].Edit.set_edit_text("aaaaaaaaa")

app[' 无标题 - 记事本 '].Edit.type_keys("hello world{ENTER}", with_spaces = True)
time.sleep(1)
print(app[' 无标题 - 记事本 '].Edit.texts())
print(app[' 无标题 - 记事本 '].Edit.text_block())
app[' 无标题 - 记事本 '].menu_select("编辑(&E) -> 替换(&R)...")


#app['替换'].取消.click()






