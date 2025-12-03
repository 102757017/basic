# -*- coding: UTF-8 -*-
import os
#在OpenCV导入之前禁用Media Foundation 后端硬件加速变换，可以改善msmf后端下摄像头初始化速度
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0" 
import cv2
import time
import datetime

print((f"OpenCV版本:{cv2.__version__}"))
print("msmf test")
t1=datetime.datetime.now()
cap = cv2.VideoCapture(0)
ret,frame=cap.read()
codec = int(cap.get(cv2.CAP_PROP_FOURCC))
fourcc_str = "".join([chr((codec >> 8 * i) & 0xFF) for i in range(4)])
print(codec, fourcc_str)
t2=datetime.datetime.now()-t1
print(t2)
cap.release()

t1=datetime.datetime.now()
cap = cv2.VideoCapture(0)
flag=cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
ret,frame=cap.read()
t2=datetime.datetime.now()-t1
print(t2)
cap.release()

t1=datetime.datetime.now()
cap = cv2.VideoCapture(0)
flag1=cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
flag2=cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
ret,frame=cap.read()
t2=datetime.datetime.now()-t1
print(t2)
cap.release()


t1=datetime.datetime.now()
params = [
    cv2.CAP_PROP_FRAME_WIDTH,1920,
    cv2.CAP_PROP_FRAME_HEIGHT, 1080,
    ]
cap = cv2.VideoCapture(0,cv2.CAP_MSMF,params)
ret,frame=cap.read()
t2=datetime.datetime.now()-t1
print(t2)
cap.release()


print("directshow test")
t1=datetime.datetime.now()
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
mjpg_int = cv2.VideoWriter_fourcc(*'MJPG') 
cap.set(cv2.CAP_PROP_FOURCC, mjpg_int) # directshow后端默认格式是YUY2
ret,frame=cap.read()
codec = int(cap.get(cv2.CAP_PROP_FOURCC))
fourcc_str = "".join([chr((codec >> 8 * i) & 0xFF) for i in range(4)])
print(codec, fourcc_str) 
t2=datetime.datetime.now()-t1
print(t2)
cap.release()

t1=datetime.datetime.now()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
flag=cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
ret,frame=cap.read()
t2=datetime.datetime.now()-t1
print(t2)
cap.release()

t1=datetime.datetime.now()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
flag1=cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
flag2=cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
ret,frame=cap.read()
t2=datetime.datetime.now()-t1
print(t2)
cap.release()
