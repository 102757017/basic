# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np
import math

os.chdir(os.path.dirname(__file__))

 
#img = cv2.imread('test.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('part2.png', dtype=np.uint8), 1)

#图片先转成灰度的
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#给出高斯矩阵的尺寸和标准差，将图片进行高斯模糊
#gray=cv2.GaussianBlur(gray, (3, 3), 0)  

#提取轮廓
gray=cv2.Canny(gray,70,210)


#再把图片转换为二值图
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

def nothing(x):
    pass


cv2.namedWindow('image')

# 创建滚动条
cv2.createTrackbar('r','image',1,10,nothing)
#cv2.createTrackbar('theta','image',180,180,nothing)
cv2.createTrackbar('threshold','image',40,255,nothing)
cv2.createTrackbar('minLineLength','image',5,255,nothing)
cv2.createTrackbar('maxLineGap','image',10,255,nothing)



#根据直线的端点，求直线的角度
def angle(x1,y1,x2,y2):
    L=math.sqrt(np.square(x1-x2)+np.square(y1-y2))
    j=math.acos((x2-x1)/L)/math.pi*180
    return j





img2=img.copy()
while(1):
    cv2.imshow('image',img2)
    k = cv2.waitKey(1) & 0xFF
    #ESC键
    if k == 27:
        break

    # 获取滚动条的位置
    c1 = cv2.getTrackbarPos('r','image')
    #c2 = cv2.getTrackbarPos('theta','image')
    c3 = cv2.getTrackbarPos('threshold','image')
    c4 = cv2.getTrackbarPos('minLineLength','image')
    c5 = cv2.getTrackbarPos('maxLineGap','image')
    
    #参数1：要检测的二值图（一般是阈值分割或边缘检测后的图）
    #参数2：距离r的精度，值越大，考虑越多的线，最大值为图像的对角线
    #参数3：角度θ的精度，值越小，考虑越多的线
    #参数4：累加数阈值，值越小，考虑越多的线，检测到大于几个点共线则判断为一条直线
    #minLineLength：最短长度阈值，比这个长度短的线会被排除
    #maxLineGap：最大直线间隙
    lines=cv2.HoughLinesP(binary, c1, np.pi / 180, c3 , minLineLength=c4, maxLineGap=c5)

    img2=img.copy()
    if lines is not None:
        #将检测的线画出来（注意是极坐标噢）
        for line in lines:
            x1, y1, x2, y2 = line[0]
            j=angle(x1,y1,x2,y2)
            #只显示大于70度，小于115度的直线
            if j>70 and j<115:
                cv2.line(img2, (x1, y1), (x2, y2), (0, 0, 255), 1, lineType=cv2.LINE_AA)
                '''第一个参数是指明在哪幅图像上绘制圆形；
                第二个参数是直线起点坐标。
                第三个参数指直线终点坐标。
                第四个参数表示颜色
                第五个参数表示轮廓线的宽度'''


cv2.destroyAllWindows()

