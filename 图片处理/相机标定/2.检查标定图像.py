import cv2
import numpy as np
import glob

def resize_for_display(image, max_width=1280, max_height=720):
    """
    按比例缩放图像以便在屏幕上完整显示。
    :param image: 输入图像
    :param max_width: 显示窗口的最大宽度
    :param max_height: 显示窗口的最大高度
    :return: 缩放后的图像
    """
    original_height, original_width = image.shape[:2]

    # 如果图像本身就小于最大尺寸，则无需缩放
    if original_height <= max_height and original_width <= max_width:
        return image

    # 计算缩放比例
    ratio_w = max_width / original_width
    ratio_h = max_height / original_height
    # 取较小的比例以确保整个图像都能装下
    scale_ratio = min(ratio_w, ratio_h)

    # 计算新的尺寸
    new_width = int(original_width * scale_ratio)
    new_height = int(original_height * scale_ratio)

    # 使用cv2.resize进行缩放
    # cv2.INTER_AREA 适合缩小图像
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return resized_image

# ====================================================================
# 主程序
# ====================================================================

# 初始化参数
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250) #每个小方块里面的黑白图案是6x6比特的二进制网格
# 这里的物理尺寸应与你的标定板生成脚本中的尺寸一致
board = cv2.aruco.CharucoBoard(size=(5, 7),                    # 标定板的网格尺寸 (列数, 行数)
                               squareLength=0.035,             # 每个方格的实际长度 (单位: 米)
                               markerLength=0.0175,            # 每个ArUco标记的实际长度 (单位: 米)
                               dictionary=dictionary           # 使用的ArUco字典
                               )

detector = cv2.aruco.CharucoDetector(board)

# 存储所有图像的角点和ID
all_charuco_corners = []
all_charuco_ids = []
all_image_size = None

# 读取所有标定图像
image_files = glob.glob("calibration_images/*.jpg")
print(f"找到 {len(image_files)} 张标定图像")

# 创建一个可调整大小的窗口
window_name = 'Detected Charuco - Press any key to continue'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

for i, image_file in enumerate(image_files):
    print(f"处理图像 {i+1}/{len(image_files)}: {image_file}")
    
    # 读取图像
    image = cv2.imread(image_file)
    if image is None:
        print(f"  警告: 无法读取图像 {image_file}, 跳过")
        continue
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if all_image_size is None:
        all_image_size = gray.shape[::-1]  # (width, height)
    
    # 检测ChArUco角点
    charuco_corners, charuco_ids, marker_corners, marker_ids = detector.detectBoard(gray)
    
    # 如果至少找到一些角点，则保存用于标定
    if charuco_corners is not None and len(charuco_corners) > 3:
        all_charuco_corners.append(charuco_corners)
        all_charuco_ids.append(charuco_ids)
        
        # 在图像上绘制检测结果（可选，用于可视化）
        image_copy = image.copy()
        cv2.aruco.drawDetectedCornersCharuco(image_copy, charuco_corners, charuco_ids)
        
        # 在显示前缩放图像
        display_image = resize_for_display(image_copy, max_width=1280, max_height=720)
        
        # 使用缩放后的图像进行显示
        cv2.imshow(window_name, display_image)
        
        # 将等待时间延长，以便有足够的时间查看，按任意键继续
        cv2.waitKey(0)
    else:
        print(f"  在图像 {image_file} 中未找到足够的角点，跳过")

cv2.destroyAllWindows()

print(f"\n成功检测到 {len(all_charuco_corners)} 张有效图像用于标定。")
