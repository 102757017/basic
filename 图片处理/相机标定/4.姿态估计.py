# 4.图像校正.py

import cv2
import numpy as np
import glob
import os

def load_calibration_results(filename="calibration_results.npz"):
    """从文件加载相机标定结果"""
    try:
        data = np.load(filename)
        camera_matrix = data['camera_matrix']
        dist_coeffs = data['dist_coeffs']
        print(f"成功从 {filename} 加载标定数据。")
        return camera_matrix, dist_coeffs
    except FileNotFoundError:
        print(f"错误: 标定文件 '{filename}' 未找到。请先运行标定程序。")
        return None, None

def undistort_image(image, camera_matrix, dist_coeffs):
    """使用标定参数对图像进行校正"""
    h, w = image.shape[:2]
    
    # 获取优化后的相机矩阵，alpha=1 表示保留所有像素，可能会有黑边
    # alpha=0 表示只保留有效像素，会裁剪掉因校正产生的黑边
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    
    # 进行校正
    undistorted_img = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    
    # (可选) 裁剪图像，去除黑边
    # x, y, w, h = roi
    # undistorted_img = undistorted_img[y:y+h, x:x+w]
    
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

