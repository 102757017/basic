from PyQt5 import  QtWidgets
import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import  QBasicTimer




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi('form1.ui', self)


        # 将按钮点击事件和槽函数绑定
        self.radioButton.clicked.connect(self.radio)
        self.checkBox.clicked.connect(self.check)
        self.spinBox.valueChanged.connect(self.spin)
        self.horizontalSlider.valueChanged.connect(self.slide)
        self.horizontalScrollBar.valueChanged.connect(self.slide2)
        self.dateTimeEdit.dateTimeChanged.connect(self.time)
        self.dial.valueChanged.connect(self.turn)
        self.pushButton.clicked.connect(self.start)




    # 定义槽函数
    def radio(self):
        self.lineEdit.setText(str(self.radioButton.isChecked()))
        
    def check(self):
        self.lineEdit_2.setText(str(self.checkBox.isChecked()))

    def spin(self):
        self.lineEdit_3.setText(str(self.spinBox.value()))
        self.horizontalSlider.setValue(self.spinBox.value())

    def slide(self):
        self.lineEdit_3.setText(str(self.horizontalSlider.value()))
        self.spinBox.setValue(self.horizontalSlider.value())

    def slide2(self):
        self.lineEdit_4.setText(str(self.horizontalScrollBar.value()))

    def time(self):
        self.lineEdit_6.setText(self.dateTimeEdit.time().toString())
        self.lineEdit_8.setText(self.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss"))

    def turn(self):
        self.lineEdit_9.setText(str(self.dial.value()))

    def start(self):
        #创建一个定时器
        self.timer = QBasicTimer()
        #启动定时器。该方法的第一个参数为超时时间。第二个参数表示当前超时时间到了以后定时器触发超时事件的接受对象。
        self.timer.start(100, self)
        self.step=0


    # 覆写计时器事件处理函数timerEvent()
    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 1
        self.progressBar.setValue(self.step)
        self.lcdNumber.display(self.step)






if __name__ == "__main__":
    # 创建了一个PyQt封装的QApplication对象,创建的时候,把系统参数传进去了.顾名思义,这一句创建了一个应用程序对象
    app = QtWidgets.QApplication(sys.argv)
    # #创建一个我们生成的那个窗口，注意把类名修改为MainWindow
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
