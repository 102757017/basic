from PyQt5 import  QtWidgets
import sys
from PyQt5.uic import loadUi


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi('form1.ui', self)


        # 将按钮点击事件和calc槽函数绑定
        self.pushButton.clicked.connect(self.calc)
        self.pushButton_2.clicked.connect(self.open)

        self.actionnew.triggered.connect(self.about)
        self.actionhuihua.triggered.connect(self.huihua)
        self.actionxinc.triggered.connect(self.nWindow)

    # 定义槽函数
    def calc(self):
        c1=float(self.lineEdit.text())
        c2 = float(self.lineEdit_2.text())
        c3=c1+c2
        self.label_3.setText(str(c3))

    def open(self):
        # 设置文件扩展名过滤,
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self,"请打开文件", "F:\我的文档\桌面", "Text Files (*.xlsx;*.xls)")
        self.lineEdit_3.setText(fileName)

    def about(self):
        QtWidgets.QMessageBox.information(self, "标题", "这是第一个PyQt5 GUI程序")


    def huihua(self):
        p=QtWidgets.QMessageBox.information(self, "标题", "选择yes还是no", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        QtWidgets.QMessageBox.information(self, "标题", "yes的代码是16384,no的代码是65536，此选项的代码是："+str(p))
        print(p)
        # 使用infomation信息框

    def nWindow(self):
        #窗口一闪而过是因为MainWindow是个局部变量,他的生命周期随着函数调用完毕就释放了,应该把他改成self的成员变量
        self.MainWindow = QtWidgets.QMainWindow()
        # 创建一个我们生成的那个窗口
        loadUi('form2.ui',self.MainWindow)
        # 显示窗口
        self.MainWindow.show()



if __name__ == "__main__":
    # 创建了一个PyQt封装的QApplication对象,创建的时候,把系统参数传进去了.顾名思义,这一句创建了一个应用程序对象
    app = QtWidgets.QApplication(sys.argv)
    # #创建一个我们生成的那个窗口，注意把类名修改为MainWindow
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
