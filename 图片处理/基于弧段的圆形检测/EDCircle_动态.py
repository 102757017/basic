from __future__ import print_function
import numpy as np
import cv2
import sys
import threading
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

# ================= 核心检测函数 =================
def detect_ellipses(image, sigma=1.0, gradient_threshold=20, min_path_length=60, 
                    line_fit_error_threshold=1.0, nfa_validation=True, pf_mode=True):
    ed = cv2.ximgproc.createEdgeDrawing()
    ed_params = cv2.ximgproc_EdgeDrawing_Params()
    
    ed_params.Sigma = sigma
    ed_params.GradientThresholdValue = int(gradient_threshold)
    ed_params.MinPathLength = int(min_path_length)
    ed_params.LineFitErrorThreshold = line_fit_error_threshold
    ed_params.NFAValidation = bool(nfa_validation)
    ed_params.PFmode = bool(pf_mode)
    ed_params.MinLineLength = 0  
    
    ed.setParams(ed_params)
    
    ed.detectEdges(image.copy())
    ellipses = ed.detectEllipses()
    
    results = []
    if ellipses is not None:
        for i in range(len(ellipses)):
            cx = int(ellipses[i][0][0])
            cy = int(ellipses[i][0][1])
            a = int(ellipses[i][0][2]) + int(ellipses[i][0][3])
            b = int(ellipses[i][0][2]) + int(ellipses[i][0][4])
            angle = ellipses[i][0][5]
            is_circle = (ellipses[i][0][2] == 0) 
            
            results.append((cx, cy, a, b, angle, is_circle))
            
    return results

# ================= 打印 Log 函数 =================
def print_function_call_log(p):
    log_str = (
        "\n椭圆检测函数调用参数:\n"
        "detect_ellipses(image,\n"
        f"                sigma={p['Sigma']:.1f},\n"
        f"                gradient_threshold={int(p['GradientThreshold'])},\n"
        f"                min_path_length={int(p['MinPathLength'])},\n"
        f"                line_fit_error_threshold={p['LineFitErrorThreshold']:.1f},\n"
        f"                nfa_validation={bool(p['NFAValidation'])},\n"
        f"                pf_mode={bool(p['PFmode'])}\n"
        "                )"
    )
    print(log_str)


# ================= Tkinter GUI 应用程序 =================
class EllipseDetectorApp:
    def __init__(self, root, default_image_path):
        self.root = root
        self.root.title("椭圆检测工具 (Tkinter EdgeDrawing)")
        self.root.geometry("1200x800")
        
        # 全局状态
        self.src = None
        self.gray = None
        self.debounce_timer = None
        self.tk_image = None  # 保持对图片的引用，防止被垃圾回收

        # 创建参数变量
        self.var_sigma = tk.DoubleVar(value=1.0)
        self.var_grad = tk.IntVar(value=24)
        self.var_min_path = tk.IntVar(value=60)
        self.var_line_err = tk.DoubleVar(value=1.0)
        self.var_nfa = tk.IntVar(value=1)
        self.var_pf = tk.IntVar(value=1)

        self.init_ui()
        self.load_initial_image(default_image_path)

    def init_ui(self):
        # 建立左右分栏
        self.left_panel = tk.Frame(self.root, width=300, bg='#f0f0f0')
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.right_panel = tk.Frame(self.root, bg='gray')
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 图像显示标签
        self.img_label = tk.Label(self.right_panel, bg='black')
        self.img_label.pack(fill=tk.BOTH, expand=True)

        # --- 左侧控制面板组件 ---
        tk.Button(self.left_panel, text="打开新图片 (Open Image)", command=self.open_image, 
                  font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white').pack(fill=tk.X, pady=(0, 20), ipady=5)

        self.create_slider("Sigma (高斯平滑)", self.var_sigma, 0.1, 5.0, 0.1)
        self.create_slider("Gradient Threshold (梯度阈值)", self.var_grad, 1, 100, 1)
        self.create_slider("Min Path Length (最小连续长度)", self.var_min_path, 10, 200, 1)
        self.create_slider("Line Fit Error (拟合误差容忍)", self.var_line_err, 0.1, 5.0, 0.1)

        tk.Checkbutton(self.left_panel, text="NFA Validation (统计学去伪)", 
                       variable=self.var_nfa, command=self.on_param_change, bg='#f0f0f0').pack(anchor=tk.W, pady=5)
        
        tk.Checkbutton(self.left_panel, text="PF Mode (无参数模式)", 
                       variable=self.var_pf, command=self.on_param_change, bg='#f0f0f0').pack(anchor=tk.W, pady=5)

        tk.Label(self.left_panel, text="* 调整参数后停顿0.4秒，\n控制台将自动打印当前代码参数", 
                 justify=tk.LEFT, fg='gray', bg='#f0f0f0').pack(side=tk.BOTTOM, pady=20)

    def create_slider(self, label_text, variable, from_, to, resolution):
        """辅助方法：创建滑动条"""
        frame = tk.Frame(self.left_panel, bg='#f0f0f0')
        frame.pack(fill=tk.X, pady=5)
        tk.Label(frame, text=label_text, bg='#f0f0f0').pack(anchor=tk.W)
        slider = tk.Scale(frame, from_=from_, to=to, resolution=resolution, 
                          variable=variable, orient=tk.HORIZONTAL, 
                          command=self.on_param_change)
        slider.pack(fill=tk.X)

    def load_initial_image(self, path):
        """加载初始图片或生成黑板"""
        try:
            self.src = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        except:
            self.src = None
            
        if self.src is None:
            print(f"未能找到默认图片: {path}，启动空白画板。")
            self.src = np.zeros((600, 800, 3), dtype=np.uint8)
            cv2.putText(self.src, "Please open an image...", (250, 300), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            
        self.gray = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)
        self.update_detection()

    def open_image(self):
        """打开文件选择对话框并加载新图"""
        file_path = filedialog.askopenfilename(
            title="选择要检测的图片",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )
        if file_path:
            try:
                new_src = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
                if new_src is not None:
                    self.src = new_src
                    self.gray = cv2.cvtColor(self.src, cv2.COLOR_BGR2GRAY)
                    print(f"\n成功加载新图像: {file_path}")
                    self.update_detection()
                else:
                    print("\n无法读取所选图像格式。")
            except Exception as e:
                print(f"\n加载图像时发生错误: {e}")

    def on_param_change(self, *args):
        """参数修改时触发"""
        self.update_detection()
        
        # 触发防抖 Log 打印
        if self.debounce_timer is not None:
            self.debounce_timer.cancel()
        
        current_params = {
            'Sigma': self.var_sigma.get(),
            'GradientThreshold': self.var_grad.get(),
            'MinPathLength': self.var_min_path.get(),
            'LineFitErrorThreshold': self.var_line_err.get(),
            'NFAValidation': self.var_nfa.get(),
            'PFmode': self.var_pf.get()
        }
        self.debounce_timer = threading.Timer(0.4, print_function_call_log, args=[current_params])
        self.debounce_timer.daemon = True
        self.debounce_timer.start()

    def get_resized_image_for_display(self, img, max_width=900, max_height=750):
        """等比例缩放图片以适应窗口显示大小"""
        h, w = img.shape[:2]
        scale = min(max_width / w, max_height / h)
        if scale < 1.0:
            new_w, new_h = int(w * scale), int(h * scale)
            return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return img

    def update_detection(self):
        """执行检测，绘制结果并刷新到 Tkinter 界面"""
        if self.src is None or self.gray is None:
            return

        # 1. 在原始灰度图上进行检测
        ellipses_data = detect_ellipses(
            self.gray,
            sigma=self.var_sigma.get(),
            gradient_threshold=self.var_grad.get(),
            min_path_length=self.var_min_path.get(),
            line_fit_error_threshold=self.var_line_err.get(),
            nfa_validation=self.var_nfa.get(),
            pf_mode=self.var_pf.get()
        )
        
        # 2. 在原始彩图的副本上进行绘制
        result = self.src.copy()
        for (cx, cy, a, b, angle, is_circle) in ellipses_data:
            color = (0, 255, 0) if is_circle else (0, 0, 255)
            cv2.ellipse(result, (cx, cy), (a, b), angle, 0, 360, color, 2, cv2.LINE_AA)
        
        # 左上角绘制统计数量信息
        info = f"Found {len(ellipses_data)} ellipse(s)"
        cv2.putText(result, info, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 2)
        
        # 3. 准备渲染到 Tkinter (缩放 + 色彩空间转换)
        # 获取当前窗口容纳图片的极限尺寸并缩放
        display_img = self.get_resized_image_for_display(result)
        
        # BGR (OpenCV) -> RGB (PIL)
        display_img_rgb = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
        
        # Numpy array -> PIL Image -> ImageTk
        pil_image = Image.fromarray(display_img_rgb)
        self.tk_image = ImageTk.PhotoImage(image=pil_image)
        
        # 更新 Label
        self.img_label.config(image=self.tk_image)

# ================= 主入口 =================
if __name__ == '__main__':
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = '4.jpg'

    # 创建 Tkinter 主事件循环
    root = tk.Tk()
    app = EllipseDetectorApp(root, fn)
    
    # 启动主循环
    root.mainloop()
