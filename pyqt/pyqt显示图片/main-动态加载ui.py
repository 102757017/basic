from PyQt5 import  QtWidgets
import sys
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi('form1.ui', self)

        #设置画板
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.draw=""


        # 将按钮点击事件和槽函数绑定
        self.pushButton.clicked.connect(self.open)
        self.pushButton_4.clicked.connect(self.addText)
        self.pushButton_3.clicked.connect(self.addRect)
        self.pushButton_2.clicked.connect(self.addLine)
        self.pushButton_5.clicked.connect(self.addEllipse)




    # 定义槽函数
    def open(self):
        # 设置文件扩展名过滤,
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self,"请打开文件", "G:\WindowsXP高清晰图片1025乘768[够酷]（想要什么这里都能找到！）", "Text Files (*.jpg;*.bmp)")
        self.lineEdit.setText(fileName)

        pixmap=QPixmap()
        pixmap.load(fileName)
        item=QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)


    def addText(self):
        self.draw="Text"

    def addRect(self):
        self.draw = "Rect"
        rect=QGraphicsRectItem(0,0,50,50)
        self.scene.addItem(rect)

    def addLine(self):
        self.draw = "Line"
        line=QGraphicsLineItem(50,50,150,100)
        self.scene.addItem(line)

    def addEllipse(self):
        self.draw = "Ellipse"
        ellipse=QGraphicsEllipseItem(50,50,150,100)
        self.scene.addItem(ellipse)



    #定义鼠标按下事件
    def mousePressEvent(self,e):
        print("mousePressEvent")
        print("按键编码:",e.button())

        #添加文本的子函数
        if self.draw=="Text":
            #获取的鼠标点击位置是相对于主窗口的坐标，将其转化为graphicsView内的坐标
            pos=self.graphicsView.mapFrom(self, e.pos())
            text = QGraphicsTextItem("hello world")
            # 设置文本位置
            text.setPos(QPointF(pos.x(), pos.y()))
            print("graphicsView坐标：",pos.x(), pos.y())
            self.scene.addItem(text)

        #如果不使用grabMouse()，将只能响应mousepress事件而不能响应mouserelease事件以及mousemove事件
        self.grabMouse()



    #定义鼠标释放事件
    def mouseReleaseEvent(self,e):
        print("mouseReleaseEvent")
        print("按键编码:",e.button())
        # 获取的鼠标点击位置是相对于主窗口的坐标，将其转化为graphicsView内的坐标
        pos = self.graphicsView.mapFrom(self, e.pos())
        print("graphicsView坐标：",pos.x(),pos.y())
        self.releaseMouse()
        
    

    #定义鼠标移动事件
    def mouseMoveEvent(self,e):
        # 获取的鼠标点击位置是相对于主窗口的坐标，将其转化为graphicsView内的坐标
        pos = self.graphicsView.mapFrom(self, e.pos())
        print("mouseMoveEvent：",pos)

        
if __name__ == "__main__":
    # 创建了一个PyQt封装的QApplication对象,创建的时候,把系统参数传进去了.顾名思义,这一句创建了一个应用程序对象
    app = QtWidgets.QApplication(sys.argv)
    # #创建一个我们生成的那个窗口，注意把类名修改为MainWindow
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
