from __future__ import print_function
import numpy as np
import cv2
import sys
import threading

# ================= 全局变量与默认参数 =================
src = None
gray = None
window_name = "Line Detector with Trackbars"
debounce_timer = None

params = {
    'Sigma': 1.0,
    'GradientThreshold': 20,
    'MinPathLength': 50,
    'MinLineLength': 30,                 # 针对直线检测新增：最小直线长度
    'LineFitErrorThreshold': 1.0,
    'MaxDistanceBetweenTwoLines': 1.0,   # 针对直线检测新增：共线合并允许的断裂距离
    'NFAValidation': 1,
    'PFmode': 1
}

# ================= 核心检测函数 =================
def detect_lines(image, sigma=1.0, gradient_threshold=20, min_path_length=50, 
                 min_line_length=30, line_fit_error_threshold=1.0, 
                 max_distance_between_lines=1.0, nfa_validation=True, pf_mode=True):
    """
    封装好的直线检测函数 (基于 OpenCV EdgeDrawing 算法)
    
    参数说明:
    :param image: numpy.ndarray, 输入的单通道灰度图像。
    :param sigma: float, 高斯滤波平滑标准差。值越大抗噪能力越强，但也可能丢失细节。
    :param gradient_threshold: int, 梯度阈值。决定哪些像素能够作为边缘的候选点。
    :param min_path_length: int, 最小连续边缘段(Path)长度。低于此长度的碎小边缘段会被直接丢弃。
    :param min_line_length: int, 最小直线长度。从边缘中提取出来的直线，若短于该值则被丢弃。
    :param line_fit_error_threshold: float, 拟合误差阈值。边缘拟合成直线时允许的最大几何偏差。
    :param max_distance_between_lines: float, 允许共线线段合并的最大断裂距离。用于把断开的共线线段连成一根长线。
    :param nfa_validation: bool, 是否启用 NFA (Number of False Alarms) 验证机制以滤除虚假直线。
    :param pf_mode: bool, 是否启用 Parameter-Free (无参数) 模式，提升阈值的泛化适应能力。
    
    返回说明:
    :return: list of tuples, 包含所有检测到的直线段坐标列表。
             每个元素格式为: (x1, y1, x2, y2) 代表直线的两个端点坐标 (int类型)
    """
    ed = cv2.ximgproc.createEdgeDrawing()
    ed_params = cv2.ximgproc_EdgeDrawing_Params()
    
    ed_params.Sigma = sigma
    ed_params.GradientThresholdValue = gradient_threshold
    ed_params.MinPathLength = min_path_length
    ed_params.MinLineLength = min_line_length
    ed_params.LineFitErrorThreshold = line_fit_error_threshold
    ed_params.MaxDistanceBetweenTwoLines = max_distance_between_lines
    ed_params.NFAValidation = nfa_validation
    ed_params.PFmode = pf_mode
    
    ed.setParams(ed_params)
    
    # 核心修复：传入 image.copy() 防止 OpenCV 底层直接在原图内存上反复做高斯模糊污染图像
    ed.detectEdges(image.copy())
    lines = ed.detectLines()
    
    results = []
    if lines is not None:
        for i in range(len(lines)):
            # 取出直线段的两个端点坐标
            x1, y1, x2, y2 = lines[i][0]
            results.append((int(x1), int(y1), int(x2), int(y2)))
            
    return results

# ================= 打印 Log 函数 =================
def print_function_call_log(p):
    """当滑块停止拖动时触发，打印结构化的函数调用 Log"""
    log_str = (
        "\n直线检测函数调用参数:\n"
        "detect_lines(image,\n"
        f"             sigma={p['Sigma']:.1f},\n"
        f"             gradient_threshold={p['GradientThreshold']},\n"
        f"             min_path_length={p['MinPathLength']},\n"
        f"             min_line_length={p['MinLineLength']},\n"
        f"             line_fit_error_threshold={p['LineFitErrorThreshold']:.1f},\n"
        f"             max_distance_between_lines={p['MaxDistanceBetweenTwoLines']:.1f},\n"
        f"             nfa_validation={bool(p['NFAValidation'])},\n"
        f"             pf_mode={bool(p['PFmode'])}\n"
        "             )"
    )
    print(log_str)

# ================= GUI 及交互逻辑 =================
def update_detection():
    """根据当前 params 执行检测并刷新显示"""
    global src, gray, params, window_name, debounce_timer

    # 1. 触发防抖 Log 打印 (0.4秒不修改参数即视为释放鼠标)
    if debounce_timer is not None:
        debounce_timer.cancel()
    
    current_params = params.copy()
    debounce_timer = threading.Timer(0.4, print_function_call_log, args=[current_params])
    debounce_timer.daemon = True
    debounce_timer.start()

    # 2. 调用封装好的独立检测函数
    lines_data = detect_lines(
        gray,
        sigma=params['Sigma'],
        gradient_threshold=params['GradientThreshold'],
        min_path_length=params['MinPathLength'],
        min_line_length=params['MinLineLength'],
        line_fit_error_threshold=params['LineFitErrorThreshold'],
        max_distance_between_lines=params['MaxDistanceBetweenTwoLines'],
        nfa_validation=bool(params['NFAValidation']),
        pf_mode=bool(params['PFmode'])
    )
    
    # 3. 绘制结果
    result = src.copy()
    for (x1, y1, x2, y2) in lines_data:
        # 使用绿色绘制直线
        cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2, cv2.LINE_AA)
    
    # 4. 界面左上角简单信息提示
    info = (f"Sigma={params['Sigma']:.1f} Grad={params['GradientThreshold']} "
            f"PathLen={params['MinPathLength']} LineLen={params['MinLineLength']} "
            f"FitErr={params['LineFitErrorThreshold']:.1f} MaxDist={params['MaxDistanceBetweenTwoLines']:.1f}")
    cv2.putText(result, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
    
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

def on_minline(val):
    params['MinLineLength'] = val
    update_detection()

def on_linefiterr(val):
    params['LineFitErrorThreshold'] = val / 10.0
    update_detection()

def on_maxdist(val):
    params['MaxDistanceBetweenTwoLines'] = val / 10.0
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
        fn = 'p3.png'  # 默认随便给个常见名字，你自行替换

    src = cv2.imread(cv2.samples.findFile(fn))
    if src is None:
        print(f'无法读取图像: {fn}')
        return

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    # 创建滑块
    cv2.createTrackbar('Sigma', window_name, int(params['Sigma']*10), 50, on_sigma)
    cv2.createTrackbar('GradientThr', window_name, params['GradientThreshold'], 255, on_gradient)
    cv2.createTrackbar('MinPathLen', window_name, params['MinPathLength'], 500, on_minpath)
    cv2.createTrackbar('MinLineLen', window_name, params['MinLineLength'], 500, on_minline)
    cv2.createTrackbar('LineFitErr', window_name, int(params['LineFitErrorThreshold']*10), 50, on_linefiterr)
    cv2.createTrackbar('MaxDist', window_name, int(params['MaxDistanceBetweenTwoLines']*10), 50, on_maxdist)
    cv2.createTrackbar('NFA_On', window_name, params['NFAValidation'], 1, on_nfa)
    cv2.createTrackbar('PFmode', window_name, params['PFmode'], 1, on_pf)
    
    update_detection()
    
    print("使用滑动条调整参数，实时观察直线检测结果变化。")
    print("按任意键退出...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
