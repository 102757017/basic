# 4.图像校正.py

import cv2
import numpy as np
import glob
import os

def load_calibration_results(filename="calibration_results.npz"):
    """
    从文件加载相机标定结果
    
    参数:
        filename (str): 标定数据文件名，默认"calibration_results.npz"
    
    返回:
        tuple: 包含以下元素的元组:
            - camera_matrix (numpy.ndarray): 3x3相机内参矩阵
            - dist_coeffs (numpy.ndarray): 畸变系数向量
    
    异常:
        如果文件不存在，返回 (None, None)
    """
    try:
        # 使用numpy加载npz文件（压缩的numpy数据格式）
        data = np.load(filename)
        
        # 从加载的数据中提取相机内参矩阵和畸变系数
        camera_matrix = data['camera_matrix']  # 内参矩阵 [fx, 0, cx; 0, fy, cy; 0, 0, 1]
        dist_coeffs = data['dist_coeffs']      # 畸变系数 [k1, k2, p1, p2, k3, ...]
        
        print(f"成功从 {filename} 加载标定数据。")
        return camera_matrix, dist_coeffs
        
    except FileNotFoundError:
        # 处理文件不存在的情况
        print(f"错误: 标定文件 '{filename}' 未找到。请先运行标定程序。")
        return None, None


def undistort_image(image, camera_matrix, dist_coeffs):
    """
    使用标定参数对图像进行畸变校正
    
    该函数使用相机标定得到的参数，对输入图像进行畸变校正，消除镜头畸变的影响。
    
    参数:
        image (numpy.ndarray): 输入图像（BGR格式）
        camera_matrix (numpy.ndarray): 3x3相机内参矩阵
        dist_coeffs (numpy.ndarray): 畸变系数向量
    
    返回:
        tuple: 包含以下元素的元组:
            - undistorted_img (numpy.ndarray): 校正后的图像
            - new_camera_matrix (numpy.ndarray): 优化后的新相机矩阵
    
    注意:
        - 校正后的图像可能会有黑边，可以通过裁剪ROI区域去除
        - alpha参数控制保留像素的范围（0-1之间）
    """
    # 获取输入图像的尺寸（高度, 宽度）
    h, w = image.shape[:2]
    
    # 获取优化后的新相机矩阵和感兴趣区域(校正后图像中没有黑边的有效像素区域)
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix,      # 原始相机内参矩阵 [fx, 0, cx; 0, fy, cy; 0, 0, 1]
        dist_coeffs,        # 畸变系数向量 [k1, k2, p1, p2, k3, ...]
        (w, h),             # 图像原始尺寸（宽度, 高度）
        1,                  # alpha缩放因子：1=保留所有像素(可能有黑边)，0=只保留有效像素(会裁剪)
        (w, h)              # 期望的输出图像尺寸（宽度, 高度）
        )
    
    # 使用标定参数对图像进行畸变校正
    undistorted_img = cv2.undistort(
        image,              # 输入图像（BGR格式）
        camera_matrix,      # 原始相机内参矩阵 [fx, 0, cx; 0, fy, cy; 0, 0, 1]
        dist_coeffs,        # 畸变系数向量 [k1, k2, p1, p2, k3, ...]
        None,               # 可选的校正变换矩阵（设为None使用默认映射）
        new_camera_matrix   # 优化后的新相机矩阵（用于控制输出图像的视角和尺度）
        )
    
    # （可选步骤）裁剪图像，去除校正产生的黑边区域
    # roi格式: (x, y, width, height) - 有效图像区域的坐标和尺寸
    # x, y, w_roi, h_roi = roi
    # undistorted_img = undistorted_img[y:y+h_roi, x:x+w_roi]
    
    return undistorted_img, new_camera_matrix

# ====================================================================
# 主程序部分
# ====================================================================
if __name__ == '__main__':
    # 1. 加载标定数据
    mtx, dist = load_calibration_results()

    if mtx is not None and dist is not None:
        # 2. 选择一张要校正的图像 (例如，标定图像中的第一张)
        # 你可以修改这里的路径为你想要校正的任何图像
        image_files = glob.glob(os.path.join("calibration_images", '*.jpg'))
        if not image_files:
            print("错误: 在 'calibration_images' 文件夹中找不到用于校正的图像。")
        else:
            image_to_undistort_path = image_files[0]
            print(f"正在校正图像: {image_to_undistort_path}")
            
            original_image = cv2.imread(image_to_undistort_path)
            
            if original_image is None:
                print("错误: 无法读取图像。")
            else:
                # 3. 执行校正
                corrected_image, _ = undistort_image(original_image, mtx, dist)

                # 4. 显示结果
                # 为了方便比较，将原始图像和校正后图像并排显示
                # 首先将它们缩放到相同的高度
                h1, w1 = original_image.shape[:2]
                h2, w2 = corrected_image.shape[:2]
                max_height = max(h1, h2)
                
                # 计算缩放比例
                scale1 = max_height / h1
                scale2 = max_height / h2
                
                resized_original = cv2.resize(original_image, (int(w1 * scale1), int(h1 * scale1)))
                resized_corrected = cv2.resize(corrected_image, (int(w2 * scale2), int(h2 * scale2)))
                
                # 并排拼接
                comparison_image = np.hstack((resized_original, resized_corrected))
                
                # 再次检查拼接后的图像是否过大
                final_h, final_w = comparison_image.shape[:2]
                if final_w > 1920: # 如果宽度超过1920，则整体缩小
                    scale = 1920 / final_w
                    comparison_image = cv2.resize(comparison_image, (int(final_w * scale), int(final_h * scale)))

                cv2.imshow('Original vs Corrected', comparison_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                # (可选) 保存校正后的图像
                output_filename = "corrected_image.jpg"
                cv2.imwrite(output_filename, corrected_image)
                print(f"校正后的图像已保存为 {output_filename}")

