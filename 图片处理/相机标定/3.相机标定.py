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
    使用文件夹中的图像对相机进行ChArUco标定 - 修正版本
    """
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    board = cv2.aruco.CharucoBoard((squares_x, squares_y), square_length, marker_length, dictionary)
    
    # 使用CharucoDetector而不是ArucoDetector
    charuco_params = cv2.aruco.CharucoParameters()
    detector_params = cv2.aruco.DetectorParameters()
    refiner_params = cv2.aruco.RefineParameters()
    detector = cv2.aruco.CharucoDetector(board, charuco_params, detector_params, refiner_params)

    # 存储所有数据
    all_charuco_corners = []
    all_charuco_ids = []
    all_image_points = []  # 新增：存储图像点
    all_object_points = [] # 新增：存储对象点
    
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

        # 使用CharucoDetector检测板子
        charuco_corners, charuco_ids, marker_corners, marker_ids = detector.detectBoard(gray)
        
        # 如果检测到足够的角点
        if charuco_corners is not None and len(charuco_corners) >= 4:
            # 关键修正：匹配图像点和对象点
            current_object_points = []
            current_image_points = []
            
            # 手动创建对象点（3D坐标）
            for corner_id in charuco_ids:
                # 根据ID计算在板子上的3D位置
                obj_point = board.getChessboardCorners()[corner_id[0]]
                current_object_points.append(obj_point)
                current_image_points.append(charuco_corners[charuco_ids.tolist().index(corner_id)])
            
            current_object_points = np.array(current_object_points, dtype=np.float32)
            current_image_points = np.array(current_image_points, dtype=np.float32)
            
            # 存储数据
            all_charuco_corners.append(charuco_corners)
            all_charuco_ids.append(charuco_ids)
            all_object_points.append(current_object_points)
            all_image_points.append(current_image_points)
            
            valid_count += 1
            print(f"有效图像 {valid_count}: {os.path.basename(fname)} - 检测到 {len(charuco_corners)} 个角点")

    if valid_count < 1:
        print("错误: 未能在任何图像中检测到足够的ChArUco角点。")
        return None, None, None

    print(f"\n成功使用 {valid_count} 张有效图像进行标定")

    # 使用标准的calibrateCamera函数，与C++示例一致
    calibration_flags = 0
    
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        all_object_points, 
        all_image_points, 
        img_size, 
        None, 
        None,
        flags=calibration_flags
    )

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
