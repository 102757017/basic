# -*- coding: UTF-8 -*-
from pywinauto import clipboard

format_list=clipboard.GetClipboardFormats()
for x in format_list:
    print(x,clipboard.GetFormatName(x))

print(clipboard.GetData(format_id=format_list[1]))








