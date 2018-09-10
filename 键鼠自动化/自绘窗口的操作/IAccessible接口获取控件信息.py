# -*- coding: UTF-8 -*-
from ctypes import windll, oledll, WinError, byref, POINTER
from ctypes.wintypes import POINT
from comtypes import COMError
from comtypes.automation import VARIANT
from comtypes.client import GetModule

# create wrapper for the oleacc.dll type library
GetModule("oleacc.dll")
# import the interface we need from the wrapper
from comtypes.gen.Accessibility import IAccessible




def AccessibleObjectFromPoint(x, y):
    "Return an accessible object and an index. See MSDN for details."
    pacc = POINTER(IAccessible)()
    var = VARIANT()
    oledll.oleacc.AccessibleObjectFromPoint(POINT(x, y), byref(pacc),
byref(var))
    return pacc, var

def AccessibleObjectFromWindow(hwnd):
    ptr = POINTER(IAccessible)()
    res = oledll.oleacc.AccessibleObjectFromWindow(
      hwnd,0,
      byref(IAccessible._iid_),byref(ptr))
    return ptr

print(AccessibleObjectFromPoint(24, 1060))
print(AccessibleObjectFromPoint(0, 0))
print(AccessibleObjectFromWindow(724966))
