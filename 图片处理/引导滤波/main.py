import cv2
import numpy as np

def sigmoid_curve(x, gain=4.0, offset=0.5):
    """S形曲线映射函数"""
    sigmoid = 1.0 / (1.0 + np.exp(-gain * (x - offset)))
    min_val = 1.0 / (1.0 + np.exp(-gain * (0 - offset)))
    max_val = 1.0 / (1.0 + np.exp(-gain * (1 - offset)))
    return (sigmoid - min_val) / (max_val - min_val)

def process_image(img, radius, eps, gain, offset):
    """执行引导滤波 + S形曲线增强"""
    img_f = img.astype(np.float32) / 255.0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    
    # 引导滤波提取基础层
    # 注意：ximgproc 模块需要安装 opencv-contrib-python
    base_layer = cv2.ximgproc.guidedFilter(gray, gray, radius, int(eps * 1000) / 1000.0)
    
    # 提取细节层
    detail_layer = img_f - base_layer[..., np.newaxis]
    
    # 应用S形曲线
    base_adjusted = sigmoid_curve(base_layer, gain, offset)
    
    # 融合
    result_f = base_adjusted[..., np.newaxis] + detail_layer
    return np.clip(result_f * 255.0, 0, 255).astype(np.uint8)

def interactive_curve_adjustment(image_path):
    """交互式动态调参主程序"""
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图像: {image_path}")
        return

    # 创建窗口
    window_name = "Dynamic Curve Adjustment"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    # 创建滑动条 (名称, 窗口名, 初始值, 最大值, 回调函数)
    # 半径 radius: 1 - 50
    cv2.createTrackbar('Radius', window_name, 16, 50, lambda x: None)
    # 正则化 eps: 1 - 500 (实际使用时除以1000，即 0.001 - 0.5)
    cv2.createTrackbar('Eps(x1000)', window_name, 100, 500, lambda x: None)
    # 增益 gain: 10 - 100 (实际使用时除以10，即 1.0 - 10.0)
    cv2.createTrackbar('Gain(x10)', window_name, 30, 100, lambda x: None)
    # 中心点 offset: 10 - 90 (实际使用时除以100，即 0.1 - 0.9)
    cv2.createTrackbar('Offset(x100)', window_name, 40, 90, lambda x: None)

    print("滑动条说明：")
    print("1. Radius: 引导滤波半径 (越大光照越平滑)")
    print("2. Eps: 正则化参数 (越大边缘越锐利，但可能放大噪点)")
    print("3. Gain: S曲线增益 (越大对比度越强)")
    print("4. Offset: S曲线中心 (越小提亮暗部越猛)")
    print("按 's' 键保存当前参数和结果，按 'ESC' 退出。")

    while True:
        # 获取滑动条当前值
        radius = cv2.getTrackbarPos('Radius', window_name)
        eps = cv2.getTrackbarPos('Eps(x1000)', window_name) / 1000.0
        gain = cv2.getTrackbarPos('Gain(x10)', window_name) / 10.0
        offset = cv2.getTrackbarPos('Offset(x100)', window_name) / 100.0
        
        # 防止参数为0导致异常
        radius = max(1, radius)
        
        # 执行图像处理
        result = process_image(img, radius, eps, gain, offset)
        
        # 拼接原图和处理后的图进行对比显示
        display = np.hstack([img, result])
        
        # 在图像上绘制当前参数信息
        param_text = f"R:{radius} E:{eps:.3f} G:{gain:.1f} O:{offset:.2f}"
        cv2.putText(display, param_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.imshow(window_name, display)

        # 键盘事件处理
        key = cv2.waitKey(30) & 0xFF
        if key == 27:  # ESC 键退出
            break
        elif key == ord('s'):  # 's' 键保存
            cv2.imwrite("dynamic_adjusted_result.jpg", result)
            print(f"已保存结果。当前最优参数: radius={radius}, eps={eps}, gain={gain}, offset={offset}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 替换为你的测试图像路径
    interactive_curve_adjustment("p1.jpg")
