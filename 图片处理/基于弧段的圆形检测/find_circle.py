import cv2
import numpy as np
import logging # 导入 logging 模块

# 配置 logging
# 将日志级别设置为 DEBUG，以便看到所有调试信息
logging.basicConfig(level=logging.INFO, 
                    format='%(levelname)s: %(message)s')

def fit_circle_to_arc(arc_points):
    """
    使用最小二乘法拟合2D点集到圆。
    返回(中心x, 中心y, 半径) 或在拟合失败时返回None。
    """
    if len(arc_points) < 3:
        logging.debug("      fit_circle_to_arc: 弧段点数少于3，无法拟合。")
        return None

    A = np.zeros((len(arc_points), 3))
    B = np.zeros((len(arc_points), 1))
    
    for i, p in enumerate(arc_points):
        x, y = p[0], p[1]
        A[i, 0] = x
        A[i, 1] = y
        A[i, 2] = 1
        B[i, 0] = x**2 + y**2
        
    try:
        if np.linalg.matrix_rank(A) < 3:
            logging.debug("      fit_circle_to_arc: 矩阵A的秩不足3，无法唯一确定圆。")
            return None

        p_vec, residuals, rank, s = np.linalg.lstsq(A, B, rcond=None)
        
        A_val = p_vec[0, 0]
        B_val = p_vec[1, 0]
        C_val = p_vec[2, 0]
        
        center_x = A_val / 2.0
        center_y = B_val / 2.0
        
        radius_sq = C_val + center_x**2 + center_y**2
        
        if radius_sq < 1: 
            logging.debug(f"      fit_circle_to_arc: 半径平方为{radius_sq:.2f}，无效半径（小于1）。")
            return None 
        
        radius = np.sqrt(radius_sq)
        
        return (center_x, center_y, radius)
    except np.linalg.LinAlgError as e:
        logging.debug(f"      fit_circle_to_arc: 线性代数错误: {e}")
        return None
    except Exception as e:
        logging.debug(f"      fit_circle_to_arc: 发生意外错误: {e}")
        return None

def validate_circle_completeness(circle, all_arcs_from_contour, min_arc_length, image_shape):
    """
    根据轮廓中与拟合圆接近的点的总角度跨度，验证拟合圆的完整性。
    """
    if circle is None:
        return False

    center_x, center_y, radius = circle
    
    if radius <= 5: 
        logging.debug(f"      validate_circle_completeness: 半径 {radius:.1f} 过小 (<= 5)。")
        return False
    diagonal = np.sqrt(image_shape[0]**2 + image_shape[1]**2)
    if radius > diagonal * 0.75: 
        logging.debug(f"      validate_circle_completeness: 半径 {radius:.1f} 过大 (> {diagonal * 0.75:.1f})。")
        return False

    buffer = 0.5 * radius 
    if not (0 - buffer < int(center_x) < image_shape[1] + buffer and
            0 - buffer < int(center_y) < image_shape[0] + buffer):
        logging.debug(f"      validate_circle_completeness: 圆心 ({center_x:.1f}, {center_y:.1f}) 距离图像边界过远。")
        return False

    angles = []
    
    radius_tolerance_factor = 0.15 
    radius_tolerance = radius * radius_tolerance_factor

    for arc in all_arcs_from_contour:
        for p in arc:
            px, py = p[0], p[1]
            dist_to_center = np.sqrt((px - center_x)**2 + (py - center_y)**2)
            if abs(dist_to_center - radius) < radius_tolerance:
                angles.append(np.arctan2(py - center_y, px - center_x))
    
    if not angles:
        logging.debug("      validate_circle_completeness: 没有足够的点与拟合圆接近。")
        return False
        
    sorted_angles = np.sort(np.unique(angles)) 
    
    if len(sorted_angles) < 2: 
        logging.debug("      validate_circle_completeness: 独特的角度点少于2。")
        return False 
    
    segment_diffs = np.zeros(len(sorted_angles))
    segment_diffs[:-1] = np.diff(sorted_angles)
    segment_diffs[-1] = (sorted_angles[0] + 2 * np.pi) - sorted_angles[-1]
    
    longest_gap = np.max(segment_diffs)
    actual_arc_radians = (2 * np.pi) - longest_gap
    required_arc_radians = min_arc_length * (2 * np.pi)
    
    if actual_arc_radians < required_arc_radians:
        logging.debug(f"      validate_circle_completeness: 检测到的弧长 ({actual_arc_radians:.2f} rad) 小于所需 ({required_arc_radians:.2f} rad)。")
        return False
    
    return True

def calculate_curvature(p1, p2, p3):
    """
    计算三点形成的曲率 (角度变化，单位为度)
    """
    v1_raw = p2 - p1
    v2_raw = p3 - p2
    
    if np.linalg.norm(v1_raw) < 1e-6 or np.linalg.norm(v2_raw) < 1e-6:
        return 0.0
    
    angle1 = np.arctan2(v1_raw[1], v1_raw[0])
    angle2 = np.arctan2(v2_raw[1], v2_raw[0])
    
    curvature = np.degrees(angle2 - angle1)
    
    if curvature > 180:
        curvature -= 360
    elif curvature < -180:
        curvature += 360
        
    return curvature

def segment_into_arcs(points, max_angle_diff=45): 
    """
    将轮廓点分割为弧段，基于曲率变化。
    """
    num_points = len(points)
    if num_points < 3: 
        return [points] if num_points > 0 else [] 
        
    arcs = []
    current_arc = [points[0]]
    
    for i in range(1, num_points):
        p1 = points[(i - 1 + num_points) % num_points] 
        p2 = points[i]                                  
        p3 = points[(i + 1) % num_points]               

        curvature = calculate_curvature(p1, p2, p3)
        
        if abs(curvature) > max_angle_diff:  
            if len(current_arc) >= 8: 
                arcs.append(np.array(current_arc))
            current_arc = [points[i]] 
        else:
            current_arc.append(points[i])
    
    if len(current_arc) >= 8: 
        arcs.append(np.array(current_arc))

    return arcs


def detect_occluded_circles(image, min_arc_length=0.3, reference_radius=None, radius_tolerance_factor=0.20):
    """
    专门检测被遮挡圆的方法
    min_arc_length: 最小弧长比例 (0.3表示至少需要30%的圆弧)
    reference_radius: (可选) 一个参考半径，用于过滤检测到的圆。
    radius_tolerance_factor: (如果提供了reference_radius) 允许的半径偏差百分比。
                             例如，0.20意味着半径应在 [reference_radius * 0.8, reference_radius * 1.2] 之间。
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("1. 灰度图", gray)           # 注释掉中间调试窗口
    # cv2.waitKey(10)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # cv2.imshow("2. 模糊图", blurred)         # 注释掉中间调试窗口
    # cv2.waitKey(10)
    
    edges = cv2.Canny(blurred, 30, 80) 
    # cv2.imshow("3. Canny 边缘", edges)       # 注释掉中间调试窗口
    # cv2.waitKey(10)

    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    detected_circles = []
    image_height, image_width = image.shape[0], image.shape[1]
    
    logging.info(f"检测到 {len(contours)} 个原始轮廓。")

    debug_contours_image = image.copy()
    if len(contours) > 20: 
        cv2.drawContours(debug_contours_image, contours[::(len(contours)//10+1) or 1], -1, (0,0,255), 1)
    else:
        cv2.drawContours(debug_contours_image, contours, -1, (0,0,255), 1)
    # cv2.imshow("4. 所有原始轮廓", debug_contours_image) # 注释掉中间调试窗口
    # cv2.waitKey(100)

    for i_contour, contour in enumerate(contours):
        if len(contour) < 15:  
            logging.debug(f"\n处理轮廓 {i_contour} (点数: {len(contour)}) - 跳过，点数过少。")
            continue
            
        logging.debug(f"\n处理轮廓 {i_contour} (点数: {len(contour)})")
        points = contour.reshape(-1, 2) 
        
        arcs = segment_into_arcs(points) 
        
        if not arcs:
            logging.debug(f"    轮廓 {i_contour}: 未能分割出有效弧段。")
            continue
        
        debug_arcs_image = image.copy()
        for arc_idx, arc in enumerate(arcs):
            color = ((arc_idx * 50 + 100) % 255, (arc_idx * 100 + 50) % 255, (arc_idx * 150 + 150) % 255)
            if len(arc) > 1:
                cv2.polylines(debug_arcs_image, [arc], False, color, 2) 
        # cv2.imshow(f"5. 轮廓 {i_contour} 的弧段", debug_arcs_image) # 注释掉中间调试窗口
        # cv2.waitKey(10)

        for i_arc, arc in enumerate(arcs):
            if len(arc) < 8:  
                logging.debug(f"    弧段 {i_arc} (轮廓 {i_contour}, 点数: {len(arc)}) - 跳过，点数过少。")
                continue
            
            x, y, w, h = cv2.boundingRect(arc)
            min_dim = 10 
            aspect_ratio_max = 5.0 
            
            if w <= min_dim or h <= min_dim:
                logging.debug(f"    弧段 {i_arc} (轮廓 {i_contour}, 点数: {len(arc)}) 边界框过小/扁平 (w={w}, h={h}), 视为直线，跳过拟合。")
                continue
            
            aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else float('inf')
            if aspect_ratio > aspect_ratio_max:
                logging.debug(f"    弧段 {i_arc} (轮廓 {i_contour}, 点数: {len(arc)}) 边界框宽高比过大 ({aspect_ratio:.2f}), 视为直线，跳过拟合。")
                continue

            logging.debug(f"    处理弧段 {i_arc} (轮廓 {i_contour}, 点数: {len(arc)}), 边界框 (w={w}, h={h}, AR={aspect_ratio:.2f})")
            
            circle = fit_circle_to_arc(arc) 
            
            if circle: 
                cx, cy, r = circle
                logging.debug(f"      拟合圆参数: 中心=({cx:.1f}, {cy:.1f}), 半径={r:.1f}")
                
                diagonal = np.sqrt(image_width**2 + image_height**2)
                if not (5 < r < diagonal * 0.75): 
                    logging.debug(f"      *** 跳过拟合圆: 半径 {r:.1f} 不在合理范围 (5, {diagonal * 0.75:.1f})。")
                    continue

                # 新增的半径范围过滤
                if reference_radius is not None:
                    lower_bound = reference_radius * (1 - radius_tolerance_factor)
                    upper_bound = reference_radius * (1 + radius_tolerance_factor)
                    if not (lower_bound <= r <= upper_bound):
                        logging.debug(f"      *** 跳过拟合圆: 半径 {r:.1f} 不在参考范围 [{lower_bound:.1f}, {upper_bound:.1f}]。")
                        continue
                
                if validate_circle_completeness(circle, arcs, min_arc_length, image.shape):
                    is_duplicate = False
                    for dcx, dcy, dr in detected_circles:
                        dist_center = np.sqrt((cx - dcx)**2 + (cy - dcy)**2)
                        if dist_center < 15 and abs(r - dr) / dr < 0.20: 
                            is_duplicate = True
                            logging.debug(f"      检测到重复圆: 拟合圆 ({int(cx)}, {int(cy)}, {int(r)}) 与现有圆 ({int(dcx)}, {int(dcy)}, {int(dr)}) 接近。")
                            break
                    
                    if not is_duplicate:
                        detected_circles.append(circle)
                        logging.debug(f"      --> 检测到! 圆: 中心=({int(cx)}, {int(cy)}), 半径={int(r)}")
                else:
                    logging.debug(f"      拟合圆 ({int(cx)}, {int(cy)}, {int(r)}) 未通过完整性验证。")
            else:
                logging.debug(f"      弧段 {i_arc} 拟合圆失败（返回 None）。")

    return detected_circles

# 测试代码
if __name__ == '__main__':
    # 加载图像
    image_path = 'p2.jpg' # 更改为你的图像文件名
    test_image = cv2.imread(image_path)

    if test_image is None:
        logging.error(f"错误: 无法加载图像 '{image_path}'。请确保文件存在且路径正确。")
    else:
        # 假设 contour.jpg 中期望检测的圆半径大约是 100 像素
        # 你需要根据实际图像中圆的大小来调整这些值
        expected_radius = 30 
        radius_tol = 0.25 # 允许半径在 100 +/- 25% 之间 (即 75 到 125)
        min_arc_length_test = 0.3 #圆的完整度

        logging.info(f"检测被遮挡的圆 (参考半径: {expected_radius}, 容差: {radius_tol*100:.0f}%) 完整度:{min_arc_length_test}")
        
        detected_circles_result = detect_occluded_circles(
            test_image.copy(), 
            min_arc_length=min_arc_length_test,
            reference_radius=expected_radius,       # 传入参考半径
            radius_tolerance_factor=radius_tol      # 传入半径容差因子
        )

        logging.info(f"最终检测到 {len(detected_circles_result)} 个潜在的圆:")

        output_image = test_image.copy()
        for i, (cx, cy, r) in enumerate(detected_circles_result):
            logging.info(f"  圆 {i+1}: 中心=({int(cx)}, {int(cy)}), 半径={int(r)}")
            cv2.circle(output_image, (int(cx), int(cy)), int(r), (0, 255, 0), 2) 
            cv2.circle(output_image, (int(cx), int(cy)), 3, (0, 0, 255), -1) 

        cv2.imshow("原始图像", test_image)
        cv2.imshow("检测到的被遮挡的圆", output_image)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
