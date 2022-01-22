# -*- coding: UTF-8 -*-
from pywinauto.application import Application
from pywinauto import mouse
import time
import pprint



#连接要操作程序的PID
#app = Application().connect(process=11548)


#连接窗口句柄也可以
#app = Application().connect(handle=0x010f0c)

#自绘窗口设置(backend="uia"),使用uia的搜索速度要比win32慢很多，所以能不用就不用
#Win32 API窗口设置(backend="win32") 
#使用标题、类型等匹配
#app = Application(backend="win32").connect(title_re="无标题 - 记事本", class_name="Notepad")



# 对于Windows中自带应用程序，直接执行，对于外部应用应输入完整路径
app = Application(backend="uia").start('notepad.exe')
#描述Notepad.exe进程中的窗口
#dlg_spec = app.UntitledNotepad
#print(dlg_spec)


#title等于pyInspect中的name
#如果找到了多个相同的窗口，可以指定found_index=0,1,2,3
#title是py_inspect中的name属性，部分电脑系统会获取不到title。#title_re=None, # 正则匹配文字
#auto_id是py_inspect中的automation_id属性
#control_type是py_inspect中的control_type属性
#class_name是py_inspect中的class_name属性。#class_name_re=None, # 正则匹配类名
dlg_spec = app.window(title='无标题 - 记事本')



#等待控件出现，可传入五种参数, 可以组合传参，但要以空格隔开：
#exists: 窗口变成有效的句柄
#visible: 窗口可见，没有隐藏
#enabled: 窗口没有disable
#ready: visible + enable
#active: active
#timeout:设置超时时间，若在n秒内没有等到窗口在wait_for中传入的几种状态，则会抛出TimeoutError。
#retry_interval:超时后，间隔n秒再次重试。
dlg_spec.wait("exists",timeout=5)

#将窗口最大化
dlg_spec.maximize()


#显示控件树，可用的最佳匹配名显示为树中每个控件的列表
#dlg_spec.print_control_identifiers()


#该函数会搜索所有子窗口及孙子窗口，如果找到了多个相同的窗口，可以指定found_index=0,1,2,3
#title是py_inspect中的name属性，部分电脑系统会获取不到title。#title_re=None, # 正则匹配文字
#auto_id是py_inspect中的automation_id属性
#control_type是py_inspect中的control_type属性
#class_name是py_inspect中的class_name属性。#class_name_re=None, # 正则匹配类名
cj=dlg_spec.child_window(auto_id="15", control_type="Edit")
cj.wait("exists",timeout=5)


#显示此控件的属性及支持的操作
pprint.pprint(dir(cj.wrapper_object()))
pprint.pprint(dir(cj.element_info))
print("title:",cj.element_info.name)
print("auto_id:",cj.element_info.automation_id)
print("control_type:",cj.element_info.control_type)
print("class_name:",cj.element_info.class_name)



#可以省略wrapper_object()
# 给控件画个红色框便于看出是哪个,支持'red', 'green', 'blue'
cj.wrapper_object().draw_outline(colour = 'red')
cj.wrapper_object().set_edit_text("我是替换前的文本")
print(cj.exists())

#可以省略wrapper_object()
#uia模式下方法
print(cj.wrapper_object().legacy_properties().get('Value'))
#win32模式下的方法
print(cj.wrapper_object().text_block())



#多级菜单的操作方法
dlg_spec.wrapper_object().menu_select(r"编辑(E)->替换(R)...")


cj2=dlg_spec.child_window(title="查找内容(N):", auto_id="1152", control_type="Edit")
cj2.wait("exists",timeout=5)
cj2.wrapper_object().set_edit_text("我是替换的内容")


cj3=dlg_spec.child_window(title="取消", auto_id="2", control_type="Button")
cj3.wait("exists",timeout=5)
cj3.wrapper_object().click_input()


mouse.click(button='left', coords=(100,100))

#app['替换'].取消.click()





