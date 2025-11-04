import numpy as np
import cv2 as cv
import sys
import tkinter as tk

# =================================================================
# 辅助函数 (Utility Functions)
# =================================================================
def get_screen_size():
    """使用tkinter获取屏幕的宽度和高度。"""
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    return screen_width, screen_height

def show_image_in_center(window_name, image, screen_width, screen_height):
    """在屏幕中央显示一个OpenCV窗口。"""
    img_height, img_width = image.shape[:2]
    x = max(0, (screen_width - img_width) // 2)
    y = max(0, (screen_height - img_height) // 2)
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    cv.moveWindow(window_name, x, y)
    cv.imshow(window_name, image)
    
# =================================================================
# 检测函数 (Detection Functions)
# =================================================================
def Detector_Circle(image_path, MinPathLength, PFmode, NFAValidation):
    """
    从指定路径的图像中检测圆和椭圆。
    MinPathLength 所有弧段都必须满足 MinPathLength 要求，如果有任何一个弧段长度 < MinPathLength，该弧段会被丢弃
    PFmode 设置为True可能提高检测精度但会降低速度    
    NFAValidation 设置为False可能检测到更多特征但可能有更多误检
    """
    image = cv.imread(cv.samples.findFile(image_path))
    if image is None:
        print(f'错误: 无法读取图像: {image_path}')
        return None, None
    
    # [已修正] 使用正确的常量 cv.COLOR_BGR2GRAY
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    ed = cv.ximgproc.createEdgeDrawing()
    params = cv.ximgproc_EdgeDrawing_Params()
    params.MinPathLength = MinPathLength
    params.PFmode = PFmode
    params.NFAValidation = NFAValidation
    ed.setParams(params)
    ed.detectEdges(gray)
    ellipses = ed.detectEllipses()
    return image, ellipses

# =================================================================
# 绘制函数 (Drawing Functions) - 已修正
# =================================================================

def draw_ellipses(image, ellipses, roundness_threshold=0.4):
    """
    在图像上循环绘制所有满足条件的椭圆。
    MinLineLength  最小直线长度，尝试在5到100之间调整，值越大，检测到的直线越少但越长
    """
    if ellipses is None:
        print("未检测到任何椭圆或圆的候选对象。")
        return image
    
    output_image = image.copy()
    
    print("\n" + "="*50)
    print(f"开始处理 {len(ellipses)} 个候选对象")
    print("="*50)
    
    drawn_count = 0
    for i, ellipse in enumerate(ellipses):
        center = (int(ellipse[0][0]), int(ellipse[0][1]))
        val1 = int(ellipse[0][2]) # 可能是 半长轴 或 半径
        val2 = int(ellipse[0][3]) # 可能是 半短轴 或 0 (标志位)
        angle = ellipse[0][5]

        print(f"\n--- 候选对象 #{i+1} ---")
        print(f"  原始数据: Center={center}, Val1={val1}, Val2={val2}")

        # [核心修正] 判断是否为 detectEllipses 返回的特殊 "圆" 格式
        if val2 == 0:
            # 这是特殊格式的圆: val1 是半径
            radius = val1
            print("  [判定] 特殊格式 -> 圆 (Val2 is 0)")
            print(f"    -> 半径 = {radius}")
            axes = (radius, radius)
            color = (0, 255, 0) # 绿色表示圆
            cv.ellipse(output_image, center, axes, angle, 0, 360, color, 2, cv.LINE_AA)
            drawn_count += 1
        else:
            # 这是普通格式的椭圆
            semi_major_axis = val1
            semi_minor_axis = val2
            print("  [判定] 普通格式 -> 椭圆")
            
            if semi_major_axis == 0:
                print("    [过滤] 原因: 半长轴为 0，无效数据。")
                continue
            
            roundness = semi_minor_axis / semi_major_axis
            print(f"    计算圆度: {semi_minor_axis} / {semi_major_axis} = {roundness:.4f}")
            
            if roundness < roundness_threshold:
                print(f"    [过滤] 原因: 圆度 {roundness:.4f} < 阈值 {roundness_threshold}")
                continue
            
            print(f"    [绘制] 原因: 圆度满足条件。")
            axes = (semi_major_axis, semi_minor_axis)
            color = (255, 0, 0) # 蓝色表示椭圆
            cv.ellipse(output_image, center, axes, angle, 0, 360, color, 2, cv.LINE_AA)
            drawn_count += 1

    print("\n" + "="*50)
    print(f"处理完成。总共绘制了 {drawn_count} / {len(ellipses)} 个对象。")
    print("="*50)
        
    return output_image






if __name__ == '__main__':
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 'p1.jpg'
        
    screen_w, screen_h = get_screen_size()
    print(f"检测到屏幕尺寸: {screen_w}x{screen_h}")

    print("--- 开始检测圆和椭圆 ---")
    original_image_c, ellipses = Detector_Circle(
        image_path=fn,
        MinPathLength=60,
        PFmode=True,
        NFAValidation=True
    )
    
    if original_image_c is not None:
        ellipse_result_image = draw_ellipses(original_image_c, ellipses, roundness_threshold=0.4)
        
        show_image_in_center("Source Image", original_image_c, screen_w, screen_h)
        show_image_in_center("Detected Circles and Ellipses (FIXED)", ellipse_result_image, screen_w, screen_h)
        cv.waitKey(0)
    else:
        print(f"无法处理图像 {fn} 进行圆形检测。")
    cv.destroyAllWindows()
    print('Done.')
