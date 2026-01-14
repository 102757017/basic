"""
基于ChArUco板的相机标定程序
使用ChArUco板（结合棋盘格和ArUco标记）进行相机标定
优点：比传统棋盘格更稳定，能提供更多可识别的角点
"""

import cv2
import numpy as np
import glob
import os


def save_calibration_results(camera_matrix, dist_coeffs, filename="calibration_results.npz"):
    """
    将相机标定结果保存到文件
    
    参数:
        camera_matrix (numpy.ndarray): 3x3相机内参矩阵
        dist_coeffs (numpy.ndarray): 畸变系数向量
        filename (str): 保存的文件名，默认"calibration_results.npz"
    """
    print(f"正在将标定结果保存到 {filename}...")
    np.savez(filename, camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
    print("保存成功！")


def calibrate_camera_with_charuco(image_folder="calibration_images", squares_x=5, squares_y=7, 
                                  square_length=0.035, marker_length=0.0175):
    """
    使用ChArUco板进行相机标定的主函数
    
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
            如果标定失败，返回 (None, None, None)
    """
    
    # ==================== 1. 创建ChArUco板和检测器 ====================
    
    # 创建ArUco字典：使用6x6的250个标记的预定义字典
    # 6x6表示每个小方块里面的黑白图案是6x6比特的二进制网格
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    
    # 创建ChArUco板：将棋盘格和ArUco标记结合
    # 参数：(方格数X, 方格数Y), 方格物理长度, 标记物理长度, ArUco字典
    board = cv2.aruco.CharucoBoard((squares_x, squares_y), square_length, 
                                   marker_length, dictionary)
    
    # 配置ChArUco检测器参数
    charuco_params = cv2.aruco.CharucoParameters()      # ChArUco特定参数
    detector_params = cv2.aruco.DetectorParameters()    # 标记检测参数
    refiner_params = cv2.aruco.RefineParameters()       # 角点优化参数
    
    # 创建ChArUco检测器
    detector = cv2.aruco.CharucoDetector(board, charuco_params, 
                                         detector_params, refiner_params)

    # ==================== 2. 初始化数据存储容器 ====================
    
    all_charuco_corners = []    # 存储所有图像的角点像素坐标
    all_charuco_ids = []        # 存储所有图像的角点ID
    all_image_points = []       # 存储图像坐标系中的2D点(像素坐标)
    all_object_points = []      # 存储世界坐标系中的3D点(物理坐标，单位：米)
    
    # ==================== 3. 读取并处理标定图像 ====================
    
    # 获取文件夹中的所有图像文件
    image_files = glob.glob(os.path.join(image_folder, '*.png')) + \
                  glob.glob(os.path.join(image_folder, '*.jpg'))
    
    # 检查是否有图像文件
    if not image_files:
        print(f"错误: 在文件夹 '{image_folder}' 中未找到图像文件。")
        return None, None, None
        
    print(f"找到 {len(image_files)} 张图像")
    print(f"使用 {len(image_files)} 张图像进行标定...")

    img_size = None      # 存储图像尺寸 (width, height)
    valid_count = 0      # 有效图像计数器

    # 遍历所有图像文件
    for fname in image_files:
        # 读取图像
        img = cv2.imread(fname)
        if img is None:
            print(f"警告: 无法读取图像 {fname}，跳过。")
            continue
            
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 如果是第一张有效图像，记录图像尺寸
        if img_size is None:
            img_size = gray.shape[::-1]  # (width, height)

        # 检测ChArUco板
        # charuco_corners: 检测到的角点像素坐标 (N, 1, 2)
        # charuco_ids: 角点对应的ID (N, 1)
        # marker_corners: 检测到的ArUco标记角点
        # marker_ids: ArUco标记的ID
        charuco_corners, charuco_ids, marker_corners, marker_ids = detector.detectBoard(gray)
        
        # 检查是否检测到足够多的角点（至少20个用于标定）
        if charuco_corners is not None and len(charuco_corners) >= 20:
            # 存储检测到的角点和ID
            all_charuco_corners.append(charuco_corners)
            all_charuco_ids.append(charuco_ids)

            # 获取对应的3D世界坐标点
            # board.getChessboardCorners() 返回棋盘格所有角点的3D坐标
            # 通过charuco_ids索引获取当前检测到的角点的3D坐标
            obj_points = board.getChessboardCorners()[charuco_ids.flatten()]
            
            # 存储对应关系
            all_object_points.append(obj_points)                          # 3D世界坐标
            all_image_points.append(charuco_corners.reshape(-1, 2))       # 2D图像坐标
            
            valid_count += 1
            print(f"有效图像 {valid_count}: {os.path.basename(fname)} - 检测到 {len(charuco_corners)} 个角点")

    # ==================== 4. 检查是否有足够多的有效图像 ====================
    
    if valid_count < 1:
        print("错误: 未能在任何图像中检测到足够的ChArUco角点。")
        return None, None, None

    print(f"\n成功使用 {valid_count} 张有效图像进行标定")

    # ==================== 5. 执行相机标定 ====================
    
    # 标定标志位，0表示使用默认参数
    calibration_flags = 0
    
    # 使用OpenCV的calibrateCamera函数进行相机标定
    # 参数说明:
    # ret: 平均重投影误差（像素单位），值越小标定质量越好
    # camera_matrix: 相机内参矩阵 [fx, 0, cx; 0, fy, cy; 0, 0, 1]
    #     fx, fy: 焦距（像素单位）
    #     cx, cy: 主点坐标（图像中心点）
    # dist_coeffs: 畸变系数 [k1, k2, p1, p2, k3, ...]
    #     k1, k2, k3: 径向畸变系数
    #     p1, p2: 切向畸变系数
    # rvecs: 每张图像的旋转向量（世界坐标系到相机坐标系的旋转）
    # tvecs: 每张图像的平移向量（世界坐标系到相机坐标系的平移）
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        all_object_points,   # 3D世界坐标点集合（列表的列表）
        all_image_points,    # 2D图像坐标点集合（列表的列表）  
        img_size,           # 图像尺寸 (width, height)
        None,               # 初始相机矩阵（设为None让OpenCV自动计算）
        None,               # 初始畸变系数（设为None让OpenCV自动计算）
        flags=calibration_flags  # 标定标志位
    )

    # 返回标定结果: 内参矩阵, 畸变系数, 重投影误差
    return camera_matrix, dist_coeffs, ret



if __name__ == '__main__':
    # 调用标定函数
    camera_matrix, dist_coeffs, error = calibrate_camera_with_charuco(image_folder="calibration_images")

    # 检查标定是否成功
    if camera_matrix is not None:
        # 打印标定结果
        print("\n相机内参矩阵 (Camera Matrix):")
        print("[[fx,  0, cx]")
        print(" [ 0, fy, cy]")
        print(" [ 0,  0,  1]]")
        print(camera_matrix)
        
        print("\n畸变系数 (Distortion Coefficients):")
        print("[k1, k2, p1, p2, k3, ...]")
        print(dist_coeffs)
        
        print(f"\n平均重投影误差 (Reprojection Error): {error:.4f} 像素")

        # 保存标定结果到文件
        save_calibration_results(camera_matrix, dist_coeffs)

    else:
        print("\n标定失败。")
        print("可能的原因：")
        print("1. 未找到标定图像")
        print("2. 图像中未检测到足够的ChArUco角点")
        print("3. 图像质量不佳或光照条件不好")
        print("4. ChArUco板参数设置不正确")

    print("\n程序结束。")
