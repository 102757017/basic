from PyQt5 import  QtWidgets
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtGui,QtCore,QtWidgets,QtSql

db=QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName('test.db')
if db.open():
    print("db is open")



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        loadUi('form1.ui', self)


        # 将按钮点击事件和calc槽函数绑定
        self.pushButton.clicked.connect(self.show_table)
        self.pushButton_2.clicked.connect(self.search)



    # 定义槽函数
    def show_table(self):
        # 实例化一个可编辑数据模型
        self.model = QtSql.QSqlTableModel()
        self.tableView.setModel(self.model) 
        self.model.setTable('table1') # 设置数据模型的数据表
        self.model.select() # 查询所有数据

    def search(self):
        # 实例化一个可编辑数据模型
        self.model = QtSql.QSqlQueryModel()
        self.tableView.setModel(self.model) 
        self.model.setQuery("select * from table1 where 线报='a' and 权限='a'")

        
        


if __name__ == "__main__":
    # 创建了一个PyQt封装的QApplication对象,创建的时候,把系统参数传进去了.顾名思义,这一句创建了一个应用程序对象
    app = QtWidgets.QApplication(sys.argv)
    # #创建一个我们生成的那个窗口，注意把类名修改为MainWindow
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
