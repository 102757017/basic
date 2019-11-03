# -*- coding: UTF-8 -*-
import sys
from pywinauto import backend
from pywinauto.application import Application,WindowSpecification
import pprint
import types


#获取桌面根节点的element_info
deskinfo=backend.registry.backends["uia"].element_info_class()

#获取子节点的element_info
childinfo=deskinfo.children()
pprint.pprint(childinfo)

#获取子节点的对应进程的pid
pid=childinfo[1].process_id

#绑定该进程
app = Application(backend="uia").connect(process=pid)

#获取该进程的顶层窗口
dlg_spec = app.top_window()

#获取顶层窗口以下的树形结构
#dlg_spec.print_control_identifiers()


def print_control_identifiers(self, depth=None, filename=None):
    WindowSpecification.print_control_identifiers(self, depth=None, filename=None)


dlg_spec.print_control_identifiers=types.MethodType(print_control_identifiers,dlg_spec)
dlg_spec.print_control_identifiers()
