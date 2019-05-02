# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np



if __name__=="__main__":
    os.chdir(os.path.dirname(__file__))
    # 由于opencv不支持读取中文路径，用以下方法代替cv2.imread
    img = cv2.imdecode(np.fromfile('binary.png', dtype=np.uint8), 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #图像运算不能使用+、-、*、/的符号进行计算，否则会出现错误的数据。

    #加法运算
    img=cv2.add(img,img)
    #减法运算
    img=cv2.subtract(img,img)
    #乘法运算
    img=cv2.multiply(img,img)
    #除法运算
    img=cv2.divide(img,img)
    #反色,等同于求补集
    img=cv2.bitwise_not(img)

    #逻辑与，求交集
    img=cv2.bitwise_and(img,img)
    #逻辑或，求并集
    img=cv2.bitwise_or(img,img)
