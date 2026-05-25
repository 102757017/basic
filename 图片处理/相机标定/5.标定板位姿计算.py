import cv2
import numpy as np
import glob
import os

# ========== 1. 加载标定结果 ==========
def load_calibration_results(filename="calibration_results.npz"):
    try:
        data = np.load(filename)
        camera_matrix = data['camera_matrix']
        dist_coeffs = data['dist_coeffs']
        print(f"成功从 {filename} 加载标定数据。")
        return camera_matrix, dist_coeffs
    except FileNotFoundError:
        print(f"错误: 标定文件 '{filename}' 未找到。")
        return None, None

# ========== 2. ChArUco 板参数 ==========
SQUARES_X = 5          # X方向方格数量（列数）
SQUARES_Y = 7          # Y方向方格数量（行数）
SQUARE_LENGTH = 0.035  # 每个方格的实际长度（米，3.5cm）
MARKER_LENGTH = 0.0175 # ArUco标记的实际长度（米，1.75cm）
ARUCO_DICT = cv2.aruco.DICT_6X6_250

# 创建 ArUco 字典和 ChArUco 板对象
dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
board = cv2.aruco.CharucoBoard((SQUARES_X, SQUARES_Y), SQUARE_LENGTH, MARKER_LENGTH, dictionary)

# 创建 ChArUco 检测器（与标定时相同）
charuco_params = cv2.aruco.CharucoParameters()
detector_params = cv2.aruco.DetectorParameters()
refiner_params = cv2.aruco.RefineParameters()
detector = cv2.aruco.CharucoDetector(board, charuco_params, detector_params, refiner_params)

# ========== 3. 位姿估计函数 ==========
def estimate_pose_charuco(image, camera_matrix, dist_coeffs):
    """
    检测 ChArUco 板并估算其在相机坐标系下的位姿。
    返回: (rvec, tvec, success, charuco_corners, charuco_ids)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 检测 ChArUco 板（与标定时一致）
    charuco_corners, charuco_ids, marker_corners, marker_ids = detector.detectBoard(gray)
    
    if charuco_corners is None or len(charuco_corners) < 4:
        print("未检测到足够的 ChArUco 角点（至少需要4个）。")
        return None, None, False, None, None
    
    # 获取检测到的角点对应的 3D 世界坐标
    # board.getChessboardCorners() 返回所有棋盘格角点的 3D 坐标（按固定顺序排列）
    # 通过 charuco_ids 索引获取当前检测到的角点的 3D 坐标
    obj_points = board.getChessboardCorners()[charuco_ids.flatten()]   # 形状 (N, 3)
    img_points = charuco_corners.reshape(-1, 2)                         # 形状 (N, 2)
    
    # 使用 solvePnP 计算位姿（更加通用且稳定）
    success, rvec, tvec = cv2.solvePnP(obj_points, img_points, camera_matrix, dist_coeffs,
                                       flags=cv2.SOLVEPNP_ITERATIVE)
    if not success:
        print("solvePnP 解算失败。")
        return None, None, False, charuco_corners, charuco_ids
    
    return rvec, tvec, True, charuco_corners, charuco_ids

# ========== 4. 辅助函数：旋转向量 -> 欧拉角 ==========
def rvec_to_euler(rvec):
    R, _ = cv2.Rodrigues(rvec)
    sy = np.sqrt(R[0,0]**2 + R[1,0]**2)
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2,1], R[2,2])
        y = np.arctan2(-R[2,0], sy)
        z = np.arctan2(R[1,0], R[0,0])
    else:
        x = np.arctan2(-R[1,2], R[1,1])
        y = np.arctan2(-R[2,0], sy)
        z = 0
    return np.array([x, y, z])   # roll, pitch, yaw 弧度

# ========== 5. 可视化：在图像上绘制坐标轴 ==========
def draw_axis(image, camera_matrix, dist_coeffs, rvec, tvec, length=0.05):
    """
    在图像上绘制相机坐标轴（X:红, Y:绿, Z:蓝）。
    length: 坐标轴长度（米，建议与 SQUARE_LENGTH 同数量级，如 0.05 m）
    """
    axis_points = np.float32([[length,0,0], [0,length,0], [0,0,length]]).reshape(-1,3)
    imgpts, _ = cv2.projectPoints(axis_points, rvec, tvec, camera_matrix, dist_coeffs)
    imgpts = imgpts.reshape(-1,2).astype(int)
    # 原点投影
    origin_2d, _ = cv2.projectPoints(np.float32([[0,0,0]]), rvec, tvec, camera_matrix, dist_coeffs)
    origin_2d = tuple(origin_2d.reshape(-1,2).astype(int)[0])
    image = cv2.line(image, origin_2d, tuple(imgpts[0]), (0,0,255), 3)   # X轴 红
    image = cv2.line(image, origin_2d, tuple(imgpts[1]), (0,255,0), 3)   # Y轴 绿
    image = cv2.line(image, origin_2d, tuple(imgpts[2]), (255,0,0), 3)   # Z轴 蓝
    return image

# ========== 主程序 ==========
if __name__ == '__main__':
    # 加载相机内参
    mtx, dist = load_calibration_results()
    if mtx is None or dist is None:
        exit(1)
    
    # 选择一张包含 ChArUco 板的图像（可使用标定图像中的一张）
    image_files = glob.glob(os.path.join("calibration_images", '*.jpg')) + \
                  glob.glob(os.path.join("calibration_images", '*.png'))
    if not image_files:
        print("错误: 在 'calibration_images' 文件夹中找不到图像。")
        exit(1)
    
    img_path = image_files[0]
    print(f"读取 {img_path}")
    img = cv2.imread(img_path)
    if img is None:
        print("无法读取图像。")
        exit(1)
    
    # 估计位姿
    rvec, tvec, success, corners, ids = estimate_pose_charuco(img, mtx, dist)
    
    if not success:
        print("位姿计算失败")
    else:
        print("===== ChArUco 板相对于相机的位姿 =====")
        print(f"旋转向量 (Rodrigues):\n{rvec}")
        print(f"平移向量 (米):\n{tvec}")
        
        # 转换为欧拉角
        euler_rad = rvec_to_euler(rvec)
        euler_deg = np.degrees(euler_rad)
        print(f"欧拉角 (弧度) [roll, pitch, yaw]: {euler_rad}")
        print(f"欧拉角 (角度) [roll, pitch, yaw]: {euler_deg}")
        
        # 可视化：绘制坐标轴和检测到的 ChArUco 角点
        img_out = draw_axis(img.copy(), mtx, dist, rvec, tvec, length=SQUARE_LENGTH * 2)
        if corners is not None:
            cv2.aruco.drawDetectedCornersCharuco(img_out, corners, ids, (0,255,0))
        
        # 显示结果
        cv2.imshow("ChArUco Pose Estimation", img_out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # 保存结果
        cv2.imwrite("charuco_pose_result.jpg", img_out)
        print("结果图像已保存为 charuco_pose_result.jpg")
