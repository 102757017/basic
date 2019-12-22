# -*- coding: UTF-8 -*-
import cv2
from PIL import Image
import os

os.chdir(os.path.dirname(__file__))
cap = cv2.VideoCapture("aaa.mp4")
# 是否成功打开
suc = cap.isOpened()
i=1
#读取前3帧
while suc and i<10:
    suc, frame = cap.read()  # 读取一帧
    cv2.imshow("frame",frame)
    i=i+1
    cv2.waitKey(0)

cap.release()

cv2.destroyAllWindows()
