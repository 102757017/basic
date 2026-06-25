import os
import sys
# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
processors_dir = os.path.join(script_dir, "dll")
os.add_dll_directory(processors_dir)




from pyAAMED import pyAAMED
import cv2
import numpy as np
from tkinter import Tk, Scale, HORIZONTAL, Label, Frame
from PIL import Image, ImageTk

# --------------------------------------------
# 1. 读取并预处理图像
# --------------------------------------------
imgC = cv2.imread('circle.jpg')
if imgC is None:
    print("错误: 找不到图片 circle.jpg，请检查路径！")
    sys.exit()

imgG = cv2.cvtColor(imgC, cv2.COLOR_BGR2GRAY)
imgG = cv2.resize(imgG, (500, 500))      # 统一大小便于显示

# --------------------------------------------
# 2. 初始化 AAMED
# --------------------------------------------
aamed = pyAAMED(600, 600)                # 参数根据实际需要调整

# --------------------------------------------
# 3. 创建 tkinter 窗口
# --------------------------------------------
root = Tk()
root.title("AAMED Detection (一体化控制)")

# 用于显示图像的 Frame
frame = Frame(root)
frame.pack(padx=10, pady=10)

# 显示图像的 Label
img_label = Label(frame)
img_label.pack()

# --------------------------------------------
# 4. 更新函数（滑块拖动时调用）
# --------------------------------------------
def update_params(val=None):
    # 读取滑块值（范围已在滑块定义中设定）
    angle = angle_slider.get() / 100.0    # 0~3.14
    dist  = dist_slider.get()  / 10.0     # 0~10
    supp  = supp_slider.get()  / 100.0    # 0~1

    # 设置参数
    aamed.setParameters(angle, dist, supp)

    # 复制原图用于绘制
    display = imgG.copy()

    # 运行算法（结果保存在 display 中）
    aamed.run_AAMED(display)

    # 绘制检测结果（会额外弹出一个名为 "AMED" 的窗口）
    aamed.drawAAMED(display)

    # 立即关闭 "AMED" 窗口（避免干扰）
    # 使用 waitKey(1) 让 OpenCV 有时间完成绘制，然后销毁
    cv2.waitKey(1)
    try:
        cv2.destroyWindow("AMED")
    except cv2.error:
        pass   # 如果窗口不存在则忽略

    # 将 OpenCV 图像（灰度）转换为 RGB，再转为 PIL Image
    if len(display.shape) == 3:
        display_rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
    else:
        display_rgb = cv2.cvtColor(display, cv2.COLOR_GRAY2RGB)

    pil_img = Image.fromarray(display_rgb)
    tk_img = ImageTk.PhotoImage(pil_img)

    # 更新 Label
    img_label.config(image=tk_img)
    img_label.image = tk_img   # 保持引用，防止被垃圾回收

# --------------------------------------------
# 5. 创建滑块控件
# --------------------------------------------
# Angle 滑块 (0~314, 对应 0~3.14)
Label(root, text="Angle (0~3.14)").pack()
angle_slider = Scale(root, from_=0, to=314, orient=HORIZONTAL,
                     length=400, command=update_params)
angle_slider.set(104)          # 初始值 1.04
angle_slider.pack()

# Dist 滑块 (0~100, 对应 0~10)
Label(root, text="Dist (0~10)").pack()
dist_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL,
                    length=400, command=update_params)
dist_slider.set(34)            # 初始值 3.4
dist_slider.pack()

# Supp 滑块 (0~100, 对应 0~1)
Label(root, text="Supp (0~1)").pack()
supp_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL,
                    length=400, command=update_params)
supp_slider.set(77)            # 初始值 0.77
supp_slider.pack()

# --------------------------------------------
# 6. 首次更新显示
# --------------------------------------------
update_params()

# --------------------------------------------
# 7. 启动 tkinter 主循环
# --------------------------------------------
root.mainloop()

# 程序结束时清理 OpenCV 窗口（如果有残留）
cv2.destroyAllWindows()
