from __future__ import print_function
import numpy as np
import cv2
import sys
import threading

# ================= 全局变量与默认参数 =================
src = None
gray = None
window_name = "Ellipse Detector with Trackbars"
debounce_timer = None

params = {
    'Sigma': 1.0,
    'GradientThreshold': 20,
    'MinPathLength': 60,
    'LineFitErrorThreshold': 1.0,
    'NFAValidation': 1,
    'PFmode': 1
}

# ================= 核心检测函数 =================
def detect_ellipses(image, sigma=1.0, gradient_threshold=20, min_path_length=60, 
                    line_fit_error_threshold=1.0, nfa_validation=True, pf_mode=True):
    """
    封装好的椭圆检测函数 (基于 OpenCV EdgeDrawing 算法)
    
    参数说明:
    :param image: numpy.ndarray, 输入的单通道灰度图像。
    :param sigma: float, 高斯滤波的平滑标准差。在提取边缘前用于平滑图像，值越大抗噪能力越强，但也可能丢失细节。
    :param gradient_threshold: int, 梯度阈值。只有图像中梯度大于该值的像素才会被保留作为边缘的候选点。
    :param min_path_length: int, 最小连续边缘段(Path)的长度。低于该长度的碎小边缘段会被丢弃，调大可过滤噪点生成的短边。
    :param line_fit_error_threshold: float, 拟合误差阈值。在将边缘段拟合为弧线/椭圆时，允许的最大几何误差。
    :param nfa_validation: bool, 是否启用 NFA (Number of False Alarms) 验证机制。开启后可通过内部统计学方法滤除大量虚假椭圆。
    :param pf_mode: bool, 是否启用 Parameter-Free (无参数) 模式。开启后部分内部判断阈值会自动计算，通常能提高泛化能力。
    
    返回说明:
    :return: list of tuples, 包含所有检测到的椭圆数据列表。
             每个元素格式为: (cx, cy, a, b, angle, is_circle)
             - cx, cy: 椭圆中心坐标 (int)
             - a, b: 椭圆的半长轴和半短轴 (int)
             - angle: 椭圆的旋转角度 (float, 度)
             - is_circle: 布尔值，标识它是否为一个标准圆形 (bool)
    """
    ed = cv2.ximgproc.createEdgeDrawing()
    ed_params = cv2.ximgproc_EdgeDrawing_Params()
    
    ed_params.Sigma = sigma
    ed_params.GradientThresholdValue = gradient_threshold
    ed_params.MinPathLength = min_path_length
    ed_params.LineFitErrorThreshold = line_fit_error_threshold
    ed_params.NFAValidation = nfa_validation
    ed_params.PFmode = pf_mode
    ed_params.MinLineLength = 0  # 设置为0以彻底禁用直线检测输出
    
    ed.setParams(ed_params)
    
    # ================================================================
    # 【极其关键】：使用 image.copy()
    # 阻断 OpenCV 底层 C++ 直接在原图上进行 in-place 高斯模糊，防止原图被污染
    # ================================================================
    ed.detectEdges(image.copy())
    ellipses = ed.detectEllipses()
    
    results = []
    if ellipses is not None:
        for i in range(len(ellipses)):
            # 提取中心坐标
            cx = int(ellipses[i][0][0])
            cy = int(ellipses[i][0][1])
            
            # 计算半长轴(a)和半短轴(b)
            a = int(ellipses[i][0][2]) + int(ellipses[i][0][3])
            b = int(ellipses[i][0][2]) + int(ellipses[i][0][4])
            
            angle = ellipses[i][0][5]
            is_circle = (ellipses[i][0][2] == 0) # 标志位判断是否为绝对圆形
            
            results.append((cx, cy, a, b, angle, is_circle))
            
    return results

# ================= 打印 Log 函数 =================
def print_function_call_log(p):
    """当滑块停止拖动时触发，打印结构化的函数调用 Log"""
    log_str = (
        "\n椭圆检测函数调用参数:\n"
        "detect_ellipses(image,\n"
        f"                sigma={p['Sigma']:.1f},\n"
        f"                gradient_threshold={p['GradientThreshold']},\n"
        f"                min_path_length={p['MinPathLength']},\n"
        f"                line_fit_error_threshold={p['LineFitErrorThreshold']:.1f},\n"
        f"                nfa_validation={bool(p['NFAValidation'])},\n"
        f"                pf_mode={bool(p['PFmode'])}\n"
        "                )"
    )
    print(log_str)

# ================= GUI 及交互逻辑 =================
def update_detection():
    """根据当前 params 执行检测并刷新显示"""
    global src, gray, params, window_name, debounce_timer

    # 1. 触发防抖 Log 打印 (0.4秒不修改参数即视为释放鼠标)
    if debounce_timer is not None:
        debounce_timer.cancel()
    
    # 传入当前参数的一份拷贝，防止在等待打印时被修改
    current_params = params.copy()
    debounce_timer = threading.Timer(0.4, print_function_call_log, args=[current_params])
    debounce_timer.daemon = True
    debounce_timer.start()

    # 2. 调用封装好的独立检测函数
    ellipses_data = detect_ellipses(
        gray,
        sigma=params['Sigma'],
        gradient_threshold=params['GradientThreshold'],
        min_path_length=params['MinPathLength'],
        line_fit_error_threshold=params['LineFitErrorThreshold'],
        nfa_validation=bool(params['NFAValidation']),
        pf_mode=bool(params['PFmode'])
    )
    
    # 3. 绘制结果
    result = src.copy()
    for (cx, cy, a, b, angle, is_circle) in ellipses_data:
        color = (0, 255, 0) if is_circle else (0, 0, 255) # 圆为绿，椭圆为红
        cv2.ellipse(result, (cx, cy), (a, b), angle, 0, 360, color, 2, cv2.LINE_AA)
    
    # 4. 界面左上角简单信息提示
    info = f"Sigma={params['Sigma']:.1f} Grad={params['GradientThreshold']} MinLen={params['MinPathLength']} LineFitErr={params['LineFitErrorThreshold']:.1f} NFA={params['NFAValidation']} PF={params['PFmode']}"
    cv2.putText(result, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.imshow(window_name, result)

# ------------------ 滑块回调 ------------------
def on_sigma(val):
    params['Sigma'] = val / 10.0
    update_detection()

def on_gradient(val):
    params['GradientThreshold'] = val
    update_detection()

def on_minpath(val):
    params['MinPathLength'] = val
    update_detection()

def on_linefiterr(val):
    params['LineFitErrorThreshold'] = val / 10.0
    update_detection()

def on_nfa(val):
    params['NFAValidation'] = val
    update_detection()

def on_pf(val):
    params['PFmode'] = val
    update_detection()

# ================= 主程序 =================
def main():
    global src, gray, window_name

    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 'circle.jpg'

    src = cv2.imread(cv2.samples.findFile(fn))
    if src is None:
        print(f'无法读取图像: {fn}')
        return

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    cv2.createTrackbar('Sigma', window_name, int(params['Sigma']*10), 50, on_sigma)
    cv2.createTrackbar('GradientThr', window_name, params['GradientThreshold'], 100, on_gradient)
    cv2.createTrackbar('MinPathLen', window_name, params['MinPathLength'], 200, on_minpath)
    cv2.createTrackbar('LineFitErr', window_name, int(params['LineFitErrorThreshold']*10), 50, on_linefiterr)
    cv2.createTrackbar('NFA_On', window_name, params['NFAValidation'], 1, on_nfa)
    cv2.createTrackbar('PFmode', window_name, params['PFmode'], 1, on_pf)
    
    update_detection()
    
    print("使用滑动条调整参数，实时观察椭圆检测结果变化。")
    print("按任意键退出...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
