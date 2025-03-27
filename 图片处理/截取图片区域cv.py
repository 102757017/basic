import cv2
import numpy as np

def ClipRect(img,x, y, width, height):
    # 截取感兴趣的区域 (Region of Interest, ROI)
    roi = img[y:y+height, x:x+width]
    return roi


def ClipEllipse(image, x, y, width, height, output_size=None):
    """
    截取图像中的椭圆区域，背景设为白色
    
    参数:
        image: 输入图像 (BGR格式)
        output_size: 可选，输出图像大小 (width, height)，默认为椭圆外接矩形大小
    返回:
        截取的椭圆区域图像，背景为白色
    """
    
    # 创建椭圆掩模
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    center = (x + width // 2, y + height // 2)
    axes = (width // 2, height // 2)
    cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
    
    # 创建白色背景
    white_bg = np.full_like(image, 255)
    
    # 应用掩模
    result = np.where(mask[:, :, np.newaxis] == 255, image, white_bg)
    
    # 如果需要，裁剪到椭圆外接矩形区域
    if output_size is None:
        result = result[y:y+height, x:x+width]
    else:
        # 调整到指定大小
        result = result[y:y+height, x:x+width]
        result = cv2.resize(result, output_size)
    
    return result


if __name__=="__main__":
    img = cv2.imread('./snap/lout_00000.jpg')
    cliped_image=ClipRect(img,100, 100, 200, 200)
    cliped_image=ClipEllipse(img,100, 100, 400, 200)
    # 显示截取的区域
    cv2.imshow('Cropped Image', cliped_image)
    # 等待按键事件无限时间，然后关闭所有窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()
