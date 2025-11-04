import cv2
import numpy as np
import glob
import os

def calibrate_camera_with_charuco(image_folder="calibration_images", squares_x=5, squares_y=7, square_length=0.035, marker_length=0.0175):
    """
    使用文件夹中的图像对相机进行ChArUco标定
    """
    # 字典和标定板设置
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

        # 检测Aruco标记
        corners, ids, rejected = detector.detectMarkers(gray)

        if ids is not None and len(ids) > 0:
            # 亚像素级精确化角点
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
            for corner in corners:
                cv2.cornerSubPix(gray, corner, winSize=(3, 3), zeroZone=(-1, -1), criteria=criteria)
            
            # 插入ChArUco角点
            charuco_retval, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
            
            # 确保检测到的角点足够多 (至少4个)
            if charuco_retval > 4:
                all_charuco_corners.append(charuco_corners)
                all_charuco_ids.append(charuco_ids)

    if len(all_charuco_corners) < 1: # 检查是否至少有一张有效的图像
        print("错误: 未能在任何图像中检测到足够的ChArUco角点。")
        return None, None, None

    # ==================== 这里是修改的关键点 ====================
    # 
    #   直接删除对 getBoardObjectAndImagePoints 的调用。
    #   下面的 calibrateCameraCharuco 函数会处理所有事情。
    #
    # ==========================================================

    # 现在使用收集到的点进行相机标定
    # 这个函数会接收检测到的角点列表，并自动计算出一切
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
        all_charuco_corners, 
        all_charuco_ids, 
        board, 
        img_size, 
        None, 
        None
    )

    return camera_matrix, dist_coeffs, ret # 返回重投影误差作为第三个值

# 主程序部分
if __name__ == '__main__':
    # 调用函数并解包正确数量的返回值
    camera_matrix, dist_coeffs, error = calibrate_camera_with_charuco(image_folder="calibration_images")

    if camera_matrix is not None:
        print("\n标定完成!")
        print("相机内参矩阵 (Camera Matrix):")
        print(camera_matrix)
        print("\n畸变系数 (Distortion Coefficients):")
        print(dist_coeffs)
        print(f"\n平均重投影误差 (Reprojection Error): {error}")
    else:
        print("\n标定失败。")

