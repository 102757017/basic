# -*- coding: UTF-8 -*-
import cv2


#参数0表示第一个摄像头
cap = cv2.VideoCapture(0)

while True:
    #读取摄像头
    ret,frame=cap.read()
    
    #显示摄像头内容
    cv2.imshow("capture", frame)

    #按q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("capture.jpeg", frame)
        break
    
cap.release()
cv2.destroyAllWindows()
