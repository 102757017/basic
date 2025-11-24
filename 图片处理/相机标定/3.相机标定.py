import cv2
import numpy as np
import glob
import os

def save_calibration_results(camera_matrix, dist_coeffs, filename="calibration_results.npz"):
    """将相机标定结果保存到文件"""
    print(f"正在将标定结果保存到 {filename}...")
    np.savez(filename, camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
    print("保存成功！")

def calibrate_camera_with_charuco(image_folder="calibration_images", squares_x=5, squares_y=7, square_length=0.035, marker_length=0.0175):
    """
    参数:
        image_folder (str): 包含标定图像的文件夹路径，默认"calibration_images"
        squares_x (int): ChArUco板X方向(宽度)的方格数量
        squares_y (int): ChArUco板Y方向(高度)的方格数量
        square_length (float): 每个方格的实际物理长度(单位:米)
        marker_length (float): 每个ArUco标记的实际物理长度(单位:米)
    
    返回:
        tuple: 包含以下元素的元组:
            - camera_matrix (numpy.ndarray): 3x3相机内参矩阵
            - dist_coeffs (numpy.ndarray): 畸变系数向量 [k1, k2, p1, p2, k3, ...]
            - reprojection_error (float): 平均重投影误差，用于评估标定质量
    异常:
        如果未找到有效图像或标定失败，返回 (None, None, None)
    """
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)#每个小方块里面的黑白图案是6x6比特的二进制网格
    board = cv2.aruco.CharucoBoard((squares_x, squares_y), square_length, marker_length, dictionary)
    
    # 配置ChArUco检测器参数
    charuco_params = cv2.aruco.CharucoParameters()      # ChArUco特定参数
    detector_params = cv2.aruco.DetectorParameters()    # 标记检测参数
    refiner_params = cv2.aruco.RefineParameters()       # 角点优化参数
    
    # 创建ChArUco检测器
    detector = cv2.aruco.CharucoDetector(board, charuco_params, detector_params, refiner_params)

    all_charuco_corners = []    # 存储所有图像的角点像素坐标
    all_charuco_ids = []        # 存储所有图像的角点ID
    all_image_points = []       # 存储图像坐标系中的2D点(像素坐标)
    all_object_points = []      # 存储世界坐标系中的3D点(物理坐标)
    
    image_files = glob.glob(os.path.join(image_folder, '*.png')) + glob.glob(os.path.join(image_folder, '*.jpg'))
    if not image_files:
        print(f"错误: 在文件夹 '{image_folder}' 中未找到图像文件。")
        return None, None, None
        
    print(f"找到 {len(image_files)} 张图像")
    print(f"使用 {len(image_files)} 张图像进行标定...")

    img_size = None
    valid_count = 0

    for fname in image_files:
        img = cv2.imread(fname)
        if img is None:
            print(f"警告: 无法读取图像 {fname}，跳过。")
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if img_size is None:
            img_size = gray.shape[::-1]  # (width, height)

        # charuco_corners: 检测到的角点像素坐标
        # charuco_ids: 角点对应的ID
        # marker_corners: 检测到的ArUco标记角点
        # marker_ids: ArUco标记的ID
        charuco_corners, charuco_ids, marker_corners, marker_ids = detector.detectBoard(gray)
        
        # 如果检测到足够的角点(至少20个用于标定)
        if charuco_corners is not None and len(charuco_corners) >= 20:
            # 为当前图像创建对象点和图像点列表
            current_object_points = []  # 当前图像的3D世界坐标
            current_image_points = []   # 当前图像的2D像素坐标
            
            # 遍历所有检测到的角点ID
            for corner_id in charuco_ids:
                # 根据角点ID从标定板获取对应的3D世界坐标
                # corner_id[0] 是因为charuco_ids是二维数组，取第一个元素
                obj_point = board.getChessboardCorners()[corner_id[0]]
                current_object_points.append(obj_point)
                
                # 找到当前角点ID对应的像素坐标
                # charuco_ids.tolist().index(corner_id) 找到角点在列表中的索引
                current_image_points.append(charuco_corners[charuco_ids.tolist().index(corner_id)])
            
            # 转换为numpy数组，指定数据类型为float32(OpenCV要求)
            current_object_points = np.array(current_object_points, dtype=np.float32)
            current_image_points = np.array(current_image_points, dtype=np.float32)
            
            # 存储当前图像的数据到总列表中
            all_charuco_corners.append(charuco_corners)
            all_charuco_ids.append(charuco_ids)
            all_object_points.append(current_object_points)
            all_image_points.append(current_image_points)
            
            valid_count += 1
            print(f"有效图像 {valid_count}: {os.path.basename(fname)} - 检测到 {len(charuco_corners)} 个角点")

    # 检查是否有足够多的有效图像进行标定
    if valid_count < 1:
        print("错误: 未能在任何图像中检测到足够的ChArUco角点。")
        return None, None, None

    print(f"\n成功使用 {valid_count} 张有效图像进行标定")

    # 使用OpenCV的calibrateCamera函数进行相机标定
    calibration_flags = 0  # 标定标志位，0表示使用默认参数
    
    # 执行相机标定
    # ret: 重投影误差
    # camera_matrix: 相机内参矩阵 [fx, 0, cx; 0, fy, cy; 0, 0, 1]
    # dist_coeffs: 畸变系数 [k1, k2, p1, p2, k3, ...]
    # rvecs: 每张图像的旋转向量
    # tvecs: 每张图像的平移向量
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        all_object_points,   # 3D世界坐标点集合
        all_image_points,    # 2D图像坐标点集合  
        img_size,           # 图像尺寸 (width, height)
        None,               # 初始相机矩阵(设为None让OpenCV自动计算)
        None,               # 初始畸变系数(设为None让OpenCV自动计算)
        flags=calibration_flags  # 标定标志位
    )

    # 返回标定结果: 内参矩阵, 畸变系数, 重投影误差
    return camera_matrix, dist_coeffs, ret

# ====================================================================
# 主程序部分
# ====================================================================
if __name__ == '__main__':
    # 调用标定函数
    camera_matrix, dist_coeffs, error = calibrate_camera_with_charuco(image_folder="calibration_images")

    if camera_matrix is not None:
        print("\n标定完成!")
        print("相机内参矩阵 (Camera Matrix):")
        print(camera_matrix)
        print("\n畸变系数 (Distortion Coefficients):")
        print(dist_coeffs)
        print(f"\n平均重投影误差 (Reprojection Error): {error}")

        # 保存标定结果
        save_calibration_results(camera_matrix, dist_coeffs)

    else:
        print("\n标定失败。")
