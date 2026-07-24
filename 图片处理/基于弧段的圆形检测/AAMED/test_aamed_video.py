import os
import sys
# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
processors_dir = os.path.join(script_dir, "dll")
os.add_dll_directory(processors_dir)

from pyAAMED import pyAAMED
import cv2

# 初始化AAMED检测器
aamed = pyAAMED(600, 600)
aamed.setParameters(3.1415926/2, 3.4, 0.77)



cap = cv2.VideoCapture("v1.mp4")  # 使用默认摄像头

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    sys.exit()

print("按 'q' 键退出视频检测")

while True:
    # 读取视频帧
    ret, frame = cap.read()
    
    # 如果读取失败，退出循环
    if not ret:
        print("无法读取视频帧")
        break
    
    # 调整帧大小
    frame = cv2.resize(frame, (500, 500))
    
    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 检测椭圆
    res = aamed.run_AAMED(gray)
    print(f"检测到 {len(res)} 个椭圆")
    
    # 在灰度图像上绘制检测到的椭圆
    aamed.drawAAMED(gray)
    
    # 显示结果
    cv2.imshow('Detected Ellipses', gray)
    
    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
