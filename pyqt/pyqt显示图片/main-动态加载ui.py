from PyQt5 import  QtWidgets
import sys
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi('form1.ui', self)


        # 将按钮点击事件和calc槽函数绑定
        self.pushButton.clicked.connect(self.open)


    # 定义槽函数
    def open(self):
        # 设置文件扩展名过滤,
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self,"请打开文件", "G:\WindowsXP高清晰图片1025乘768[够酷]（想要什么这里都能找到！）", "Text Files (*.jpg;*.bmp)")
        self.lineEdit.setText(fileName)

        
        self.scene=QGraphicsScene(self)
        pixmap=QPixmap()
        pixmap.load(fileName)
        item=QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.graphicsView.setScene(self.scene)





if __name__ == "__main__":
    # 创建了一个PyQt封装的QApplication对象,创建的时候,把系统参数传进去了.顾名思义,这一句创建了一个应用程序对象
    app = QtWidgets.QApplication(sys.argv)
    # #创建一个我们生成的那个窗口，注意把类名修改为MainWindow
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
