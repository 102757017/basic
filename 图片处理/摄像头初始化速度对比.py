# -*- coding: UTF-8 -*-
import cv2
import time
import datetime

print((f"OpenCV版本:{cv2.__version__}"))
print("msmf test")
t1=datetime.datetime.now()
cap = cv2.VideoCapture(0)
ret,frame=cap.read()
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




print("directshow test")
t1=datetime.datetime.now()
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
ret,frame=cap.read()
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
