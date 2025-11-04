# 3.相机标定.py

import cv2
import numpy as np
import glob
import os

# ... (save_calibration_results 和 calibrate_camera_with_charuco 函数的开头部分不变) ...
def save_calibration_results(camera_matrix, dist_coeffs, filename="calibration_results.npz"):
    """将相机标定结果保存到文件"""
    print(f"正在将标定结果保存到 {filename}...")
    np.savez(filename, camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
    print("保存成功！")

def calibrate_camera_with_charuco(image_folder="calibration_images", squares_x=5, squares_y=7, square_length=0.035, marker_length=0.0175):
    """
    使用文件夹中的图像对相机进行ChArUco标定
    """
    # (这部分函数代码保持不变)
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    board = cv2.aruco.CharucoBoard((squares_x, squares_y), square_length, marker_length, dictionary)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)

    all_charuco_corners = []
    all_charuco_ids = []
    
    image_files = glob.glob(os.path.join(image_folder, '*.png')) + glob.glob(os.path.join(image_folder, '*.jpg'))
    if not image_files:
        print(f"错误: 在文件夹 '{image_folder}' 中未找到图像文件。")
        return None, None, None
        
    print(f"找到 {len(image_files)} 张图像")
    print(f"使用 {len(image_files)} 张图像进行标定...")

    img_size = None

    for fname in image_files:
        img = cv2.imread(fname)
        if img is None:
            print(f"警告: 无法读取图像 {fname}，跳过。")
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if img_size is None:
            img_size = gray.shape[::-1] # (width, height)

        corners, ids, rejected = detector.detectMarkers(gray)

        if ids is not None and len(ids) > 0:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
            for corner in corners:
                cv2.cornerSubPix(gray, corner, winSize=(3, 3), zeroZone=(-1, -1), criteria=criteria)
            
            charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
            
            if charuco_retval > 4:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)

    if len(all_charuco_corners) < 1:
        print("错误: 未能在任何图像中检测到足够的ChArUco角点。")
        return None, None, None

    # ==================== 【关键修改】 ====================
    # 为普通相机设置一个更简单的标定模型，防止过拟合
    # 我们不使用 CALIB_RATIONAL_MODEL，让它计算一个基本的5系数模型
    # 这里我们甚至可以传入一个空的 flags=0，但为了明确，我们先这样写
    calibration_flags = 0 
    # 如果畸变非常小，可以尝试更强的约束，例如：
    # calibration_flags = cv2.CALIB_ZERO_TANGENT_DIST # 忽略切向畸变
    # calibration_flags = cv2.CALIB_FIX_K1 | cv2.CALIB_FIX_K2 | cv2.CALIB_FIX_K3 # 假设完全没有径向畸变

    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_charuco_corners, 
        all_charuco_ids, 
        board, 
        img_size, 
        None, 
        None,
        flags=calibration_flags  # <--- 在这里添加 flags 参数
    )
    # =======================================================

    return camera_matrix, dist_coeffs, ret


# ====================================================================
# 主程序部分 (保持不变)
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
