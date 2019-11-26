#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pyqtgraph as pg
import numpy as np
from time import sleep


import pyqtgraph.examples
pyqtgraph.examples.run()


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg


app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# 打开抗锯齿
pg.setConfigOptions(antialias=True)

#添加一个子视图
p2 = win.addPlot(title="多条曲线")
p2.plot([1,2,3,4,5,6,6,7,8,8,9,9,7,7], pen=(255,0,0), name="红色曲线")
p2.plot(np.random.normal(size=110)+5, pen=(0,255,0), name="绿色曲线")
p2.plot(np.random.normal(size=120)+10, pen=(0,0,255), name="蓝色曲线")

#换行，如果不换行，下一个子视图将显示在右边
win.nextRow()



#添加一个子视图
p6 = win.addPlot(title="动态图")
#设置曲线颜色
curve = p6.plot(pen='y')
xdata = np.linspace(0, 8*np.pi, 1000)
ydata=np.sin(xdata)
i=0
ptr = 0
def update():
    global i
    if i<len(xdata):
        i+=1
        curve.setData(xdata[0:i],ydata[0:i])

#设置一个定时器
timer = QtCore.QTimer()
#设置定时器执行的函数
timer.timeout.connect(update)
#每隔5ms执行一次定时器
timer.start(5)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
