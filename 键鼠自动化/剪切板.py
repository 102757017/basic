# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap

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


#设置剪切板内的图片
def setImage(img):
    app = QApplication([])
    clipboard = app.clipboard()
    clipboard.setPixmap(QPixmap(img))

def getImage():
    app = QApplication([])
    clipboard = app.clipboard()
    img=clipboard.pixmap()
    return img


setText("将此文本复制到剪切板")
#获取剪切板内的文本
print(getText())


setImage("截图.jpg")
print(type(getImage()))