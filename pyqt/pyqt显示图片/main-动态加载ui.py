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

		#建立画板
		self.scene = QGraphicsScene(self)
		self.graphicsView.setScene(self.scene)
		self.draw=""
		self.flag=False


		# 将按钮点击事件和槽函数绑定
		self.pushButton.clicked.connect(self.open)
		self.pushButton_4.clicked.connect(self.addText)
		self.pushButton_3.clicked.connect(self.addRect)
		self.pushButton_2.clicked.connect(self.addLine)
		self.pushButton_5.clicked.connect(self.addEllipse)
		self.pushButton_6.clicked.connect(self.deletAll)

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

	def addLine(self):
		self.draw = "Line"

	def addEllipse(self):
		self.draw = "Ellipse"

	def deletAll(self):
		item_list=self.scene.items()
		for item in item_list:
			self.scene.removeItem(item)
		self.draw = ""


	#定义鼠标按下事件
	def mousePressEvent(self,e):
		print("mousePressEvent",e.button())
		# 获取的鼠标点击位置是相对于主窗口的坐标，将其转化为graphicsView内的坐标
		pos = self.graphicsView.mapFrom(self, e.pos())
		self.flag=True
		self.x0=pos.x()
		self.y0=pos.y()
		#如果不使用grabMouse()，将只能响应mousepress事件而不能响应mouserelease事件以及mousemove事件
		self.grabMouse()

		#添加line的子函数
		if self.draw=="Line":
			self.line = QGraphicsLineItem(self.x0, self.y0, self.x0, self.y0)
			self.scene.addItem(self.line)

		#添加Rect的子函数
		if self.draw=="Rect":
                        #前两个参数为坐标，后两个参数为长宽
			self.rect = QGraphicsRectItem(self.x0, self.y0, 0, 0)
			# 设置为可选择，可拖拽
			self.rect.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
			self.scene.addItem(self.rect)

		#添加椭圆的子函数
		if self.draw=="Ellipse":
                        #前两个参数为坐标，后两个参数为长宽
			self.ellipse = QGraphicsEllipseItem(self.x0, self.y0, 0, 0)
			#设置为可选择，可拖拽
			self.ellipse.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
			self.scene.addItem(self.ellipse)


	#定义鼠标移动事件
	def mouseMoveEvent(self,e):
		# 获取的鼠标点击位置是相对于主窗口的坐标，将其转化为graphicsView内的坐标
		pos = self.graphicsView.mapFrom(self, e.pos())
		print("mouseMoveEvent：",pos)
		self.x2=pos.x()
		self.y2=pos.y()

		#修改矩形大小
		if hasattr(self,"rect") and self.draw=="Rect":
			self.rect.setRect(self.x0,self.y0,self.x2-self.x0,self.y2-self.y0)

		#修改直线终点
		if hasattr(self,"line") and self.draw=="Line":
			self.line.setLine(self.x0,self.y0,self.x2,self.y2)

		#修改椭圆大小
		if hasattr(self,"ellipse") and self.draw=="Ellipse":
			self.ellipse.setRect(self.x0,self.y0,self.x2-self.x0,self.y2-self.y0)

	#定义鼠标释放事件
	def mouseReleaseEvent(self,e):
		print("mouseReleaseEvent",e.button())
		# 获取的鼠标点击位置是相对于主窗口的坐标，将其转化为graphicsView内的坐标
		pos = self.graphicsView.mapFrom(self, e.pos())
		self.flag=False
		self.x1=pos.x()
		self.y1=pos.y()
		print("graphicsView坐标：",pos.x(),pos.y())
		self.releaseMouse()

		#添加文字的子函数
		if self.draw=="Text":
			text=QGraphicsTextItem("hello world")
			text.setPos(QPointF(self.x0,self.y0))
			self.scene.addItem(text)



if __name__ == "__main__":
	# 创建了一个PyQt封装的QApplication对象,创建的时候,把系统参数传进去了.顾名思义,这一句创建了一个应用程序对象
	app = QtWidgets.QApplication(sys.argv)
	# #创建一个我们生成的那个窗口，注意把类名修改为MainWindow
	mainWindow = MainWindow()
	mainWindow.show()
	sys.exit(app.exec_())
