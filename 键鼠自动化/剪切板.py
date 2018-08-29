# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QApplication
from PIL import Image, ImageGrab

#设置剪切板内的文本
def setText(txt):
    app = QApplication([])
    clipboard = app.clipboard()
    clipboard.setText(txt)

#获取剪切板内的文本
def getText():
    app = QApplication([])
    clipboard = app.clipboard()
    return clipboard.text()


#保存剪切板中的图片
def save_clipboard_img(path):
    # 如果剪贴板不包括图像数据，这个函数返回空
    im = ImageGrab.grabclipboard()
    # 如果im是Image.Image的实例
    if isinstance(im, Image.Image):
        im.save(path)
    else:
        print("剪切板中没有图片")


save_clipboard_img("剪切板.png")


setText("将此文本复制到剪切板")
#获取剪切板内的文本
print(getText())