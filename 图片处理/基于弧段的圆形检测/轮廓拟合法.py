import cv2
import numpy as np
import time

class ImageProcessor:
    @staticmethod
    def get_largest_contour(image_path, min_area=500, max_area=50000):
        img = cv2.imread(image_path)
        if img is None:
            return None, None, 0
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 101, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return img, None, 0
            
        valid = [c for c in contours if min_area < cv2.contourArea(c) < max_area]
        if not valid:
            return img, None, 0
            
        largest = max(valid, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        return img, largest, area

def fast_ellipse_fit(contour):
    """使用 OpenCV 原生算法 + 凸包过滤进行极速拟合"""
    start = time.time()
    
    # 1. 至少需要5个点才能拟合椭圆
    if len(contour) < 5:
        return None
        
    # 2. 计算凸包，这一步相当于剔除了轮廓向内凹陷的“噪点/离群点”
    hull = cv2.convexHull(contour)
    
    # 如果凸包点数少于5个，退回到原轮廓
    fit_points = hull if len(hull) >= 5 else contour 
    
    # 3. 使用 OpenCV 的高精度拟合算法 (Direct 或 AMS)
    # cv2.fitEllipseDirect 对遮挡和不完整椭圆更鲁棒
    ellipse = cv2.fitEllipseDirect(fit_points) 
    
    # OpenCV 的返回值格式: ( (xc, yc), (width, height), angle_in_degrees )
    center, axes, angle = ellipse
    
    elapsed = time.time() - start
    print(f"OpenCV极速拟合耗时: {elapsed:.6f} 秒")
    
    return {
        "center": center, 
        "axis": (axes[0]/2, axes[1]/2), # OpenCV返回的是全轴长，转换为半轴长
        "theta": np.radians(angle)      # 转换为弧度以保持与你原代码一致
    }

if __name__ == "__main__":
    img, contour, area = ImageProcessor.get_largest_contour("5.jpg")
    if contour is not None:
        result = fast_ellipse_fit(contour)
        
        if result:
            print(f"拟合成功！圆心: {result['center']}")
            print(f"半轴长度: {result['axis']}")
            print(f"旋转角度 (弧度): {result['theta']:.4f}")
            
            # 可视化
            center = tuple(int(c) for c in result['center'])
            axes = tuple(int(a) for a in result['axis'])
            angle = np.degrees(result['theta'])
            
            cv2.ellipse(img, center, axes, angle, 0, 360, (0, 255, 0), 2)
            cv2.drawContours(img, [contour], -1, (0, 0, 255), 1)
            
            cv2.imshow("Fitted Ellipse", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("拟合失败")
    else:
        print("未找到有效轮廓")
