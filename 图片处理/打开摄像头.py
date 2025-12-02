# -*- coding: UTF-8 -*-
import cv2


#参数0表示第一个摄像头，注意cv2.CAP_DSHOW/cv2.CAP_MSMF后端的索引号不是共用的，即使都使用索引0，但是使用不同后端打开的会是不同的摄像头
cap = cv2.VideoCapture(0)


# 常见的参数 ID
params = {
    "帧宽度": cv2.CAP_PROP_FRAME_WIDTH,         # 视频帧的宽度
    "帧高度": cv2.CAP_PROP_FRAME_HEIGHT,       # 视频帧的高度
    "帧率": cv2.CAP_PROP_FPS,                  # 视频的帧率（每秒帧数）
    "亮度": cv2.CAP_PROP_BRIGHTNESS,           # 图像的亮度
    "对比度": cv2.CAP_PROP_CONTRAST,           # 图像的对比度
    "饱和度": cv2.CAP_PROP_SATURATION,         # 图像的饱和度
    "色调": cv2.CAP_PROP_HUE,                  # 图像的色调
    "增益": cv2.CAP_PROP_GAIN,                 # 图像的增益
    "曝光": cv2.CAP_PROP_EXPOSURE,             # 图像的曝光值
    "自动曝光": cv2.CAP_PROP_AUTO_EXPOSURE,    # 是否启用自动曝光
    "自动对焦": cv2.CAP_PROP_AUTOFOCUS,        # 是否启用自动对焦
    "白平衡": cv2.CAP_PROP_WB_TEMPERATURE,     # 白平衡温度
    "自动白平衡": cv2.CAP_PROP_AUTO_WB,        # 是否启用自动白平衡
    "背光补偿": cv2.CAP_PROP_BACKLIGHT,        # 背光补偿
    "锐度": cv2.CAP_PROP_SHARPNESS,            # 图像的锐度
    "伽马值": cv2.CAP_PROP_GAMMA,              # 图像的伽马值
}



# 遍历并打印参数值
for name, prop_id in params.items():
    value = cap.get(prop_id)
    print(f"{name}: {value}")
    
print("如果某个参数的值为 0 或 -1，可能表示摄像头不支持该参数")


def get_supported_resolutions_opencv_directshow(cam_index=0):
    # 使用 DirectShow 后端
    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("无法打开摄像头")
        return []
    
    # 预定义常见分辨率
    resolutions = [
        (160, 120),   # QQVGA
        (176, 144),   # QCIF
        (320, 240),   # QVGA
        (352, 288),   # CIF
        (640, 480),   # VGA
        (800, 600),   # SVGA
        (1024, 768),  # XGA
        (1280, 720),  # HD
        (1920, 1080), # Full HD
        (2560, 1440), # QHD
        (3840, 2160)  # 4K
    ]
    
    supported = []
    for width, height in resolutions:
        # 尝试设置分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # 获取实际设置的分辨率
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        if actual_width == width and actual_height == height:
            supported.append((width, height))
    
    cap.release()
    return supported

# 使用示例
supported_res = get_supported_resolutions_opencv_directshow()
print("摄像头支持的分辨率：")
for res in supported_res:
    print(f"{res[0]}x{res[1]}")


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
