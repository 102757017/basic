import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.mixture import GaussianMixture
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import joblib
import threading
import os

# ======================== 无监督异常检测器基类 ========================
class BaseAnomalyDetector:
    @staticmethod
    def extract_laws_features(image_rgb):
        """输入 RGB 图像 (H,W,3) 0-255，输出 Laws 纹理能量 (H,W,5) float32"""
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
        kernels = BaseAnomalyDetector._laws_kernels()
        channels = []
        for kernel in kernels:
            filtered = cv2.filter2D(gray, cv2.CV_32F, kernel)
            energy = np.abs(filtered)
            smoothed = cv2.GaussianBlur(energy, (0, 0), sigmaX=5)
            channels.append(smoothed)
        return np.dstack(channels)

    @staticmethod
    def _laws_kernels():
        L5 = np.array([1, 4, 6, 4, 1])
        E5 = np.array([-1, -2, 0, 2, 1])
        S5 = np.array([-1, 0, 2, 0, -1])
        return [
            np.outer(E5, L5),  # EL
            np.outer(L5, E5),  # LE
            np.outer(E5, S5),  # ES
            np.outer(S5, E5),  # SE
            np.outer(E5, E5)   # EE
        ]

    @staticmethod
    def postprocess_mask(mask, min_area=30):
        """形态学开闭运算 + 面积过滤"""
        mask = mask.astype(np.uint8) * 255
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
        result = np.zeros_like(mask, dtype=np.uint8)
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area >= min_area:
                result[labels == i] = 255
        return result > 0

# ======================== GMM 异常检测器 ========================
class GMMAnomalyDetector(BaseAnomalyDetector):
    def __init__(self, n_components=5, percentile_threshold=0.1):
        super().__init__()
        self.gmm = None
        self.scaler = None
        self.n_components = n_components
        self.percentile_threshold = percentile_threshold
        self.threshold = None

    def fit(self, features):
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(features)
        self.gmm = GaussianMixture(
            n_components=self.n_components,
            covariance_type='spherical',
            random_state=42,
            tol=0.0001,
            max_iter=100
        )
        self.gmm.fit(X_scaled)
        train_scores = self.gmm.score_samples(X_scaled)
        self.threshold = np.percentile(train_scores, self.percentile_threshold)

    def predict(self, features):
        X_scaled = self.scaler.transform(features)
        log_likelihood = self.gmm.score_samples(X_scaled)
        is_anomaly = log_likelihood < self.threshold
        anomaly_score = -log_likelihood
        return anomaly_score, is_anomaly

# ======================== OneClassSVM 异常检测器 ========================
class OneClassSVMAnomalyDetector(BaseAnomalyDetector):
    def __init__(self, nu=0.0005, gamma=0.01):
        super().__init__()
        self.svm = None
        self.scaler = None
        self.nu = nu
        self.gamma = gamma

    def fit(self, features):
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(features)
        self.svm = OneClassSVM(kernel='rbf', gamma=self.gamma, nu=self.nu, tol=0.001)
        self.svm.fit(X_scaled)

    def predict(self, features):
        X_scaled = self.scaler.transform(features)
        pred = self.svm.predict(X_scaled)
        is_anomaly = pred == -1
        anomaly_score = -self.svm.decision_function(X_scaled)
        return anomaly_score, is_anomaly

# ======================== 主应用程序（带缩放/平移） ========================
class PixelClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("像素分类器 / 纹理缺陷检测 (GMM / OneClassSVM) - 支持缩放")
        self.root.geometry("1280x800")

        # ---------- 数据结构 ----------
        self.images = []
        self.current_idx = 0
        self.model = None
        self.is_trained = False

        # 标记相关
        self.current_class = tk.IntVar(value=0)
        self.brush_size = tk.IntVar(value=5)
        self.overlay_alpha = tk.IntVar(value=150)

        # 特征与模式配置
        self.feature_config = {"intensity": True, "gaussian": True, "edges": True, "texture": False}
        self.sigmas = [1, 2, 4]
        self.mode_var = tk.StringVar(value="supervised")

        # 异常检测参数
        self.anomaly_algo = tk.StringVar(value="gmm")
        self.gmm_components = tk.IntVar(value=5)
        self.percentile_threshold = tk.DoubleVar(value=0.1)
        self.svm_nu = tk.DoubleVar(value=0.0005)
        self.svm_gamma = tk.DoubleVar(value=0.01)

        # 分类器字典
        self.classifiers = {
            "Random Forest (推荐)": lambda: RandomForestClassifier(n_estimators=50, n_jobs=-1, class_weight='balanced'),
            "Gradient Boosting": lambda: HistGradientBoostingClassifier(class_weight='balanced'),
            "KNN (k=5)": lambda: KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
            "Logistic Regression": lambda: LogisticRegression(max_iter=1000, n_jobs=-1, class_weight='balanced')
        }

        # ---------- 缩放/平移状态 ----------
        self.scale = 1.0          # 当前缩放倍率
        self.min_scale = 0.1
        self.max_scale = 10.0
        self.offset_x = 0.0       # 图像左上角在 Canvas 上的 x 偏移
        self.offset_y = 0.0
        self.space_pressed = False        # 空格按下 → 左键拖拽 = 平移
        self.panning = False
        self.pan_start_canvas = (0, 0)
        self.pan_start_offset = (0, 0)
        # 涂抹时的"上一点"，用于在两次事件之间插值，避免快速移动出现断点
        self._last_paint_img_pt = None

        # 性能优化：节流/缓存相关
        self._redraw_after_id = None     # 延迟重绘的 after id（用于滚轮节流）
        self._hires_redraw_after_id = None  # 停止缩放后做高质量重绘的 after id
        self._suppress_redraw = False   # 平移时用 canvas.move 而不触发 _redraw
        self._annotation_item_id = None # 标注层 canvas item id（用于局部替换）
        self._overlay_item_id = None    # 预测层 canvas item id
        self._base_item_id = None       # 原图层 canvas item id

        self._build_ui()

    # ---------------------------- 界面构建 ----------------------------
    def _build_ui(self):
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        main_paned.pack(fill=tk.BOTH, expand=True)

        left_container = tk.Frame(main_paned, width=350, bg='#f0f0f0')
        main_paned.add(left_container, width=350)

        notebook = ttk.Notebook(left_container)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tab_workspace = ttk.Frame(notebook)
        tab_settings = ttk.Frame(notebook)
        notebook.add(tab_workspace, text="🎨 工作区")
        notebook.add(tab_settings, text="⚙️ 模型设置")

        # ========== 工作区 ==========
        img_mgr = tk.LabelFrame(tab_workspace, text="图像管理", padx=5, pady=5)
        img_mgr.pack(fill=tk.X, pady=5, padx=5)
        btn_frame = tk.Frame(img_mgr)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="➕ 添加", command=self.add_image, width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🗑 移除", command=self.remove_current_image, width=12).pack(side=tk.RIGHT, padx=2)
        self.img_listbox = ttk.Combobox(img_mgr, state="readonly")
        self.img_listbox.pack(fill=tk.X, pady=5)
        self.img_listbox.bind("<<ComboboxSelected>>", self._on_image_selected)

        # ----- 缩放控制面板 -----
        zoom_frame = tk.LabelFrame(tab_workspace, text="缩放 / 平移 (新功能)", padx=5, pady=5, fg="#8e44ad")
        zoom_frame.pack(fill=tk.X, pady=5, padx=5)
        tk.Label(zoom_frame, text="滚轮：以光标为中心缩放\n中键拖拽 或 按住空格+左键：平移\n左键拖拽：涂抹（默认）",
                 justify=tk.LEFT, fg="#555").pack(anchor=tk.W)
        zbtns = tk.Frame(zoom_frame)
        zbtns.pack(fill=tk.X, pady=3)
        tk.Button(zbtns, text="➕ 放大", command=lambda: self.zoom_at_center(1.25)).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(zbtns, text="➖ 缩小", command=lambda: self.zoom_at_center(0.8)).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(zbtns, text="🎯 1:1", command=self.reset_zoom_to_1).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(zbtns, text="🖥 适应窗口", command=self.fit_to_window).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        self.scale_var = tk.StringVar(value="缩放: 100%")
        tk.Label(zoom_frame, textvariable=self.scale_var, fg="#27ae60", font=("", 9, "bold")).pack(anchor=tk.W)

        label_frame = tk.LabelFrame(tab_workspace, text="标记工具 (滑动涂抹)", padx=5, pady=5)
        label_frame.pack(fill=tk.X, pady=5, padx=5)
        self.class0_rb = tk.Radiobutton(label_frame, text="正常/背景 (红色)", variable=self.current_class, value=0)
        self.class0_rb.pack(anchor=tk.W)
        self.class1_rb = tk.Radiobutton(label_frame, text="缺陷/前景 (绿色)", variable=self.current_class, value=1)
        self.class1_rb.pack(anchor=tk.W)
        tk.Label(label_frame, text="画笔大小 (图像像素):").pack(anchor=tk.W, pady=(5,0))
        tk.Scale(label_frame, from_=1, to=30, orient=tk.HORIZONTAL, variable=self.brush_size).pack(fill=tk.X)
        tk.Label(label_frame, text="预测遮罩透明度:").pack(anchor=tk.W)
        tk.Scale(label_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.overlay_alpha).pack(fill=tk.X)
        tk.Button(label_frame, text="🧹 清除当前标记", command=self.clear_current_annotations).pack(fill=tk.X, pady=5)

        action_frame = tk.LabelFrame(tab_workspace, text="执行与工程", padx=5, pady=5)
        action_frame.pack(fill=tk.X, pady=5, padx=5)
        self._btn_train = tk.Button(action_frame, text="🚀 训练模型", command=self.train_model, bg='#d9edf7', height=2)
        self._btn_train.pack(fill=tk.X, pady=2)
        self._btn_predict = tk.Button(action_frame, text="🔍 预测当前图像", command=self.predict_current_image, bg='#dff0d8', height=2)
        self._btn_predict.pack(fill=tk.X, pady=2)
        tk.Button(action_frame, text="💾 导出模型 (纯模型)", command=self.export_model_only, bg='#fcf8e3', height=1).pack(fill=tk.X, pady=2)
        prj_frame = tk.Frame(action_frame)
        prj_frame.pack(fill=tk.X, pady=5)
        tk.Button(prj_frame, text="💾 导出工程", command=self.export_project, width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(prj_frame, text="📂 加载工程", command=self.load_project, width=12).pack(side=tk.RIGHT, padx=2)

        # ========== 模型设置 ==========
        mode_frame = tk.LabelFrame(tab_settings, text="1. 选择任务模式", padx=5, pady=5, font=("", 10, "bold"), fg="#c0392b")
        mode_frame.pack(fill=tk.X, pady=5, padx=5)
        tk.Radiobutton(mode_frame, text="监督分类 (需标记正常与缺陷双类)", variable=self.mode_var, value="supervised", command=self._update_ui_state).pack(anchor=tk.W)
        tk.Radiobutton(mode_frame, text="无监督异常检测 (仅需涂抹正常区域)", variable=self.mode_var, value="anomaly", command=self._update_ui_state).pack(anchor=tk.W)

        self.sup_frame = tk.LabelFrame(tab_settings, text="2. 监督学习详细配置", padx=5, pady=5, fg="#2980b9")
        tk.Label(self.sup_frame, text="【模型】选择分类算法:", font=("", 9, "bold")).pack(anchor=tk.W)
        self.clf_var = tk.StringVar()
        self.clf_combo = ttk.Combobox(self.sup_frame, textvariable=self.clf_var, state="readonly")
        self.clf_combo['values'] = list(self.classifiers.keys())
        self.clf_combo.current(0)
        self.clf_combo.pack(fill=tk.X, pady=2)
        self.clf_combo.bind("<<ComboboxSelected>>", lambda e: setattr(self, 'is_trained', False))
        tk.Label(self.sup_frame, text="【特征】勾选多尺度提取特征:", font=("", 9, "bold")).pack(anchor=tk.W, pady=(10,0))
        self.intensity_var = tk.BooleanVar(value=True)
        self.gaussian_var = tk.BooleanVar(value=True)
        self.edges_var = tk.BooleanVar(value=True)
        self.texture_var = tk.BooleanVar(value=False)
        for text, var in [("基础亮度 (Intensity)", self.intensity_var),
                          ("高斯模糊平滑特征", self.gaussian_var),
                          ("边缘特征 (Sobel)", self.edges_var),
                          ("微观纹理 (Laplace)", self.texture_var)]:
            tk.Checkbutton(self.sup_frame, text=text, variable=var, command=self._on_feature_config_change).pack(anchor=tk.W)

        self.anomaly_frame = tk.LabelFrame(tab_settings, text="2. 无监督异常检测详细配置", padx=5, pady=5, fg="#27ae60")
        tk.Label(self.anomaly_frame, text="选择检测算法:", font=("", 9, "bold")).pack(anchor=tk.W)
        algo_frame = tk.Frame(self.anomaly_frame)
        algo_frame.pack(fill=tk.X, pady=2)
        tk.Radiobutton(algo_frame, text="GMM (高斯混合模型)", variable=self.anomaly_algo, value="gmm", command=self._on_anomaly_algo_changed).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(algo_frame, text="OneClassSVM (单类支持向量机)", variable=self.anomaly_algo, value="svm", command=self._on_anomaly_algo_changed).pack(side=tk.LEFT, padx=5)

        self.gmm_frame = tk.Frame(self.anomaly_frame)
        tk.Label(self.gmm_frame, text="GMM 分量数 (Components):").pack(anchor=tk.W)
        tk.Scale(self.gmm_frame, from_=2, to=20, orient=tk.HORIZONTAL, variable=self.gmm_components).pack(fill=tk.X)
        tk.Label(self.gmm_frame, text="异常判定阈值百分位 (%):").pack(anchor=tk.W)
        tk.Scale(self.gmm_frame, from_=0.01, to=5.0, resolution=0.01, orient=tk.HORIZONTAL, variable=self.percentile_threshold).pack(fill=tk.X)
        tk.Label(self.gmm_frame, text="(阈值越小越严格，越容易放过微小缺陷)", fg='gray').pack(anchor=tk.W)

        self.svm_frame = tk.Frame(self.anomaly_frame)
        tk.Label(self.svm_frame, text="SVM 参数 nu (异常比例上限):").pack(anchor=tk.W)
        tk.Scale(self.svm_frame, from_=0.0001, to=0.1, resolution=0.0001, orient=tk.HORIZONTAL, variable=self.svm_nu).pack(fill=tk.X)
        tk.Label(self.svm_frame, text="SVM 参数 gamma (RBF核系数):").pack(anchor=tk.W)
        tk.Scale(self.svm_frame, from_=0.001, to=1.0, resolution=0.001, orient=tk.HORIZONTAL, variable=self.svm_gamma).pack(fill=tk.X)
        tk.Label(self.svm_frame, text="(gamma 越小，决策边界越平滑)", fg='gray').pack(anchor=tk.W)

        self.progress = ttk.Progressbar(left_container, mode='indeterminate')
        # 关键修复：progress 与 status_label 都用 side=BOTTOM，确保 notebook(expand=True)
        # 不会把它们挤没。先 pack 的占据最底部，后 pack 的堆在上方。
        # 渲染顺序（从上到下）：notebook → status_label → progress（最底部，最显眼）
        self.progress.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 5), padx=10)
        self.status_var = tk.StringVar(value="准备就绪 | 提示: 滚轮缩放，空格+左键或中键拖拽平移")
        status_label = tk.Label(left_container, textvariable=self.status_var, wraplength=320, fg='blue', justify=tk.LEFT)
        status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0), padx=5)

        right_frame = tk.Frame(main_paned)
        main_paned.add(right_frame, stretch="always")
        self.canvas = tk.Canvas(right_frame, bg='#333333', cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # ----- 鼠标/键盘事件绑定 -----
        # 涂抹：左键按下与拖拽（仅在非平移模式下）
        self.canvas.bind("<Button-1>", self.on_canvas_left_down)
        self.canvas.bind("<B1-Motion>", self.on_canvas_left_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_left_up)
        # 中键拖拽 = 平移
        self.canvas.bind("<Button-2>", self.on_pan_start)
        self.canvas.bind("<B2-Motion>", self.on_pan_motion)
        self.canvas.bind("<ButtonRelease-2>", self.on_pan_end)
        # 右键拖拽 = 平移（额外便利）
        self.canvas.bind("<Button-3>", self.on_pan_start)
        self.canvas.bind("<B3-Motion>", self.on_pan_motion)
        self.canvas.bind("<ButtonRelease-3>", self.on_pan_end)
        # 滚轮缩放：Windows/Mac
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        # Linux 习惯
        self.canvas.bind("<Button-4>", lambda e: self.on_mouse_wheel_delta(120))
        self.canvas.bind("<Button-5>", lambda e: self.on_mouse_wheel_delta(-120))
        # 空格键切换平移模式
        self.root.bind("<space>", self.on_space_down)
        self.root.bind("<KeyRelease-space>", self.on_space_up)
        # 窗口大小改变时刷新（节流，避免拖拽窗口边时频繁重绘）
        self.canvas.bind("<Configure>", lambda e: self._schedule_redraw(throttle_ms=80))

        self._displayed_img = None
        self._annotation_layer = None
        self._overlay_layer = None
        self._keep_refs = []

        # 当前预测结果（用于缩放后重绘叠加层）
        self._last_prediction_overlay = None  # PIL RGBA Image 或 None

        self._update_ui_state()

    # ---------------------------- UI 动态刷新 ----------------------------
    def _update_ui_state(self):
        mode = self.mode_var.get()
        if mode == "supervised":
            self.anomaly_frame.pack_forget()
            self.sup_frame.pack(fill=tk.X, pady=5, padx=5)
            self.class0_rb.config(text="正常/背景 (红色)")
            self.class1_rb.config(state=tk.NORMAL, text="缺陷/前景 (绿色)")
        else:
            self.sup_frame.pack_forget()
            self.anomaly_frame.pack(fill=tk.X, pady=5, padx=5)
            self.current_class.set(0)
            self.class0_rb.config(text="请涂抹 '正常纹理' 样本区域 (红色)")
            self.class1_rb.config(state=tk.DISABLED, text="缺陷区域由模型自动捕捉")
        self._update_anomaly_params_visibility()

    def _on_anomaly_algo_changed(self):
        self._update_anomaly_params_visibility()
        self.is_trained = False

    def _update_anomaly_params_visibility(self):
        algo = self.anomaly_algo.get()
        if algo == "gmm":
            self.svm_frame.pack_forget()
            self.gmm_frame.pack(fill=tk.X, pady=5)
        else:
            self.gmm_frame.pack_forget()
            self.svm_frame.pack(fill=tk.X, pady=5)

    # ---------------------------- 图像管理 ----------------------------
    def add_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.tif *.tiff")])
        if not path: return
        try:
            pil_img = Image.open(path).convert("RGB")
            pil_img.thumbnail((1000, 1000), Image.LANCZOS)
            img_array = np.array(pil_img)
            h, w = img_array.shape[:2]
            annotations_mask = np.full((h, w), -1, dtype=np.int8)
            self.images.append({
                'path': path, 'image': pil_img, 'array': img_array,
                'annotations': annotations_mask, 'features': None, 'w': w, 'h': h
            })
            self.current_idx = len(self.images) - 1
            # 切换图像时复位缩放并适应窗口
            self._last_prediction_overlay = None
            self.fit_to_window()
            self._update_image_listbox()
            self.is_trained = False
            self.status_var.set(f"已加载: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("错误", f"加载图像失败: {e}")

    def remove_current_image(self):
        if not self.images: return
        del self.images[self.current_idx]
        self.current_idx = max(0, self.current_idx - 1)
        self._last_prediction_overlay = None
        self.fit_to_window()
        self._update_image_listbox()
        self.is_trained = False

    def _update_image_listbox(self):
        names = [f"[{i+1}] {os.path.basename(img['path'])}" for i, img in enumerate(self.images)]
        self.img_listbox['values'] = names
        if self.images:
            self.img_listbox.current(self.current_idx)
        else:
            self.img_listbox.set('')

    def _on_image_selected(self, event=None):
        if not self.images: return
        self.current_idx = self.img_listbox.current()
        # 切换图片时：清空预测叠加层 + 复位缩放 + 全量重绘
        # （_redraw_full 内部已会无条件删除所有图层 item，这里 fit_to_window 即可）
        self._last_prediction_overlay = None
        self.fit_to_window()

    # ---------------------------- 缩放/平移核心 ----------------------------
    def _canvas_to_image_pt(self, cx, cy):
        """Canvas 坐标 → 图像像素坐标（浮点）。范围外也允许返回，调用方自检。"""
        ix = (cx - self.offset_x) / self.scale
        iy = (cy - self.offset_y) / self.scale
        return ix, iy

    def _clamp_scale(self, s):
        return max(self.min_scale, min(self.max_scale, s))

    def _update_scale_label(self):
        self.scale_var.set(f"缩放: {self.scale*100:.0f}%")

    def _apply_zoom(self, factor, cx, cy):
        """以 Canvas 上的 (cx,cy) 为锚点缩放，仅更新 scale/offset，不触发重绘。"""
        new_scale = self._clamp_scale(self.scale * factor)
        if new_scale == self.scale:
            return
        # 锚点对应的图像像素
        ix = (cx - self.offset_x) / self.scale
        iy = (cy - self.offset_y) / self.scale
        self.scale = new_scale
        # 重新计算 offset 使锚点不动: cx = ix*scale + offset_x
        self.offset_x = cx - ix * self.scale
        self.offset_y = cy - iy * self.scale
        self._update_scale_label()

    def zoom_at_canvas_pt(self, factor, cx, cy):
        """以 Canvas 上的 (cx,cy) 为锚点缩放，立即重绘（按钮触发用）。"""
        self._apply_zoom(factor, cx, cy)
        self._redraw_full()

    def _schedule_redraw(self, throttle_ms=16):
        """合并多次重绘请求，下一帧统一处理。连续滚轮时只重绘最后一次。"""
        if self._redraw_after_id is not None:
            self.root.after_cancel(self._redraw_after_id)
        self._redraw_after_id = self.root.after(throttle_ms, self._do_scheduled_redraw)

    def _do_scheduled_redraw(self):
        self._redraw_after_id = None
        self._redraw_full()
        # 取消任何挂起的高质量重绘（避免重复）
        if self._hires_redraw_after_id is not None:
            self.root.after_cancel(self._hires_redraw_after_id)
            self._hires_redraw_after_id = None
        # 安排 200ms 后做一次高质量（LANCZOS）重绘，让画面在停止缩放后变锐利
        self._hires_redraw_after_id = self.root.after(200, self._hires_redraw)

    def _hires_redraw(self):
        self._hires_redraw_after_id = None
        # 只在用户没继续操作时才重绘
        if self._redraw_after_id is None and not self.panning:
            self._redraw_full(force_hq=True)

    def zoom_at_center(self, factor):
        """以当前 Canvas 中心为锚点缩放（按钮触发）。"""
        self.canvas.update_idletasks()
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        self.zoom_at_canvas_pt(factor, cw / 2.0, ch / 2.0)

    def on_mouse_wheel(self, event):
        # event.delta 在 Windows/Mac 上是 120 的倍数
        if event.delta == 0:
            return
        # Mac 上 delta 可能很小，统一规整
        steps = event.delta / abs(event.delta)
        factor = 1.25 if steps > 0 else 0.8
        # 性能优化：立即更新 scale/offset，但延迟 16ms 重绘，合并连续滚轮事件
        self._apply_zoom(factor, event.x, event.y)
        self._schedule_redraw(throttle_ms=16)

    def on_mouse_wheel_delta(self, delta):
        # Linux Button-4/5 简化处理：以画布中心缩放
        factor = 1.25 if delta > 0 else 0.8
        self.canvas.update_idletasks()
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        self.zoom_at_canvas_pt(factor, cw / 2.0, ch / 2.0)

    def reset_zoom_to_1(self):
        """1:1 显示，并把图像左上角放到画布左上角。"""
        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self._update_scale_label()
        self._redraw_full(force_hq=True)

    def fit_to_window(self):
        """适应窗口：把当前图像缩放到正好放进画布（不超出），居中显示。"""
        if not self.images:
            return
        self.canvas.update_idletasks()
        cw = max(self.canvas.winfo_width(), 1)
        ch = max(self.canvas.winfo_height(), 1)
        img_data = self.images[self.current_idx]
        iw, ih = img_data['w'], img_data['h']
        sx = cw / iw
        sy = ch / ih
        s = min(sx, sy)
        # 不放大超过 1.0（适应窗口的常规语义），但允许用户后续手动放大
        s = min(s, 1.0)
        self.scale = self._clamp_scale(s)
        self.offset_x = (cw - iw * self.scale) / 2.0
        self.offset_y = (ch - ih * self.scale) / 2.0
        self._update_scale_label()
        self._redraw_full(force_hq=True)

    # ----- 平移事件 -----
    def on_space_down(self, event):
        # 仅在 canvas / 全局响应，避免在输入控件里按空格也触发
        if isinstance(self.root.focus_get(), (tk.Entry, tk.Spinbox, ttk.Combobox, tk.Text)):
            return
        self.space_pressed = True
        self.canvas.config(cursor="hand2")

    def on_space_up(self, event):
        self.space_pressed = False
        self.canvas.config(cursor="crosshair")

    def on_pan_start(self, event):
        self.panning = True
        self.pan_start_canvas = (event.x, event.y)
        self.pan_start_offset = (self.offset_x, self.offset_y)
        self.canvas.config(cursor="fleur")

    def on_pan_motion(self, event):
        if not self.panning:
            return
        dx = event.x - self.pan_start_canvas[0]
        dy = event.y - self.pan_start_canvas[1]
        new_offset_x = self.pan_start_offset[0] + dx
        new_offset_y = self.pan_start_offset[1] + dy
        delta_x = new_offset_x - self.offset_x
        delta_y = new_offset_y - self.offset_y
        if delta_x == 0 and delta_y == 0:
            return
        self.offset_x = new_offset_x
        self.offset_y = new_offset_y
        # 性能优化：平移不需要重新生成图像，只移动已有 canvas items 即可（O(1)）
        self.canvas.move("all", delta_x, delta_y)

    def on_pan_end(self, event):
        self.panning = False
        self.canvas.config(cursor="hand2" if self.space_pressed else "crosshair")

    # ----- 涂抹事件 -----
    def on_canvas_left_down(self, event):
        if not self.images:
            return
        if self.space_pressed:
            # 空格+左键 = 平移
            self.on_pan_start(event)
            return
        self._last_paint_img_pt = None
        self.paint(event)

    def on_canvas_left_motion(self, event):
        if not self.images:
            return
        if self.panning:
            self.on_pan_motion(event)
            return
        if self.space_pressed:
            # 空格按住时左键运动也视为平移
            self.on_pan_motion(event)
            return
        self.paint(event)

    def on_canvas_left_up(self, event):
        if self.panning:
            self.on_pan_end(event)
        self._last_paint_img_pt = None

    # ---------------------------- 显示重绘 ----------------------------
    def _display_current_image(self):
        """切换图像或大幅变化时调用：复位预测层并重绘。"""
        self.canvas.delete("all")
        self._base_item_id = None
        self._overlay_item_id = None
        self._annotation_item_id = None
        if not self.images:
            return
        self._redraw_full(force_hq=True)

    def _redraw_full(self, force_hq=False):
        """
        根据当前 scale / offset 重绘所有图层。
        force_hq=True 时用 LANCZOS（高质量，慢）；否则用 BILINEAR（交互预览，快）。
        - 切图/适应窗口/1:1/停止缩放后用 LANCZOS
        - 交互缩放过程中用 BILINEAR
        """
        if not self.images:
            self.canvas.delete("all")
            self._base_item_id = None
            self._overlay_item_id = None
            self._annotation_item_id = None
            return
        img_data = self.images[self.current_idx]
        w, h = img_data['w'], img_data['h']

        # 目标显示尺寸
        dw = max(1, int(round(w * self.scale)))
        dh = max(1, int(round(h * self.scale)))

        # 选择重采样算法：交互中 BILINEAR（5-15ms），稳定后 LANCZOS（50-150ms）
        if force_hq or self.scale >= 1.0:
            resample = Image.LANCZOS if force_hq else Image.BILINEAR
        else:
            resample = Image.BILINEAR
        # 缩小时用 LANCZOS 视觉更好且性能尚可；放大时 BILINEAR 更快
        if self.scale < 1.0 and force_hq:
            resample = Image.LANCZOS
        elif self.scale < 1.0:
            resample = Image.BILINEAR

        # === 关键修复：先删除所有图层 item，避免切换图片时旧图层残留 ===
        # 之前 overlay 是条件性删除（if _last_prediction_overlay is not None），
        # 导致切图后旧 overlay 仍在 canvas 上，与新图叠加显示。
        # 现在：无条件删除所有 tag，再按需重建。
        self.canvas.delete("base")
        self.canvas.delete("overlay")
        self.canvas.delete("marker")
        self._base_item_id = None
        self._overlay_item_id = None
        self._annotation_item_id = None

        # 1) 原图
        base = img_data['image'].resize((dw, dh), resample=resample)
        self._displayed_img = ImageTk.PhotoImage(base)
        self._base_item_id = self.canvas.create_image(
            self.offset_x, self.offset_y, anchor=tk.NW,
            image=self._displayed_img, tags=("base",)
        )

        # 2) 预测叠加层（如有）—— 即使没有也要确保旧 overlay 已被删除（上面已做）
        if self._last_prediction_overlay is not None:
            pred_disp = self._last_prediction_overlay.resize((dw, dh), resample=Image.NEAREST)
            self._overlay_layer = ImageTk.PhotoImage(pred_disp)
            self._overlay_item_id = self.canvas.create_image(
                self.offset_x, self.offset_y, anchor=tk.NW,
                image=self._overlay_layer, tags=("overlay",)
            )

        # 3) 标注层
        self._rebuild_annotation_photoimage(dw, dh)
        self._annotation_item_id = self.canvas.create_image(
            self.offset_x, self.offset_y, anchor=tk.NW,
            image=self._annotation_layer, tags=("marker",)
        )
        # 确保 z-order：base < overlay < marker
        if self._overlay_item_id is not None:
            self.canvas.tag_raise("overlay")
        self.canvas.tag_raise("marker")

    def _rebuild_annotation_photoimage(self, dw, dh):
        """根据 ann 数组重建标注层 PhotoImage。dw/dh 为显示尺寸。"""
        img_data = self.images[self.current_idx]
        h, w = img_data['h'], img_data['w']
        ann = img_data['annotations']
        # 性能优化：用 np.where 一次性赋值，比两次布尔索引略快
        overlay = np.zeros((h, w, 4), dtype=np.uint8)
        m0 = ann == 0
        m1 = ann == 1
        overlay[m0] = (255, 0, 0, 150)
        overlay[m1] = (0, 255, 0, 150)
        ann_disp = Image.fromarray(overlay).resize((dw, dh), resample=Image.NEAREST)
        self._annotation_layer = ImageTk.PhotoImage(ann_disp)

    def _refresh_annotation_only(self):
        """
        涂抹后只更新标注层，不重新缩放原图与预测层。
        性能：~15ms（仅重建标注 PhotoImage + 替换 canvas item），
        相比 _redraw_full 的 80-200ms 显著降低卡顿。
        """
        if not self.images:
            return
        img_data = self.images[self.current_idx]
        w, h = img_data['w'], img_data['h']
        dw = max(1, int(round(w * self.scale)))
        dh = max(1, int(round(h * self.scale)))

        self._rebuild_annotation_photoimage(dw, dh)
        # 用 canvas.itemconfig 替换现有 item 的 image，避免 delete/create 开销
        if self._annotation_item_id is not None:
            self.canvas.itemconfig(self._annotation_item_id, image=self._annotation_layer)
            self.canvas.tag_raise(self._annotation_item_id)
        else:
            self.canvas.delete("marker")
            self._annotation_item_id = self.canvas.create_image(
                self.offset_x, self.offset_y, anchor=tk.NW,
                image=self._annotation_layer, tags=("marker",)
            )
            self.canvas.tag_raise("marker")

    def _refresh_annotation_layer(self):
        """保留旧接口名（兼容外部调用），内部走优化路径。"""
        self._refresh_annotation_only()

    # ---------------------------- 涂抹操作 ----------------------------
    def paint(self, event):
        if not self.images:
            return
        img_data = self.images[self.current_idx]
        w, h = img_data['w'], img_data['h']
        cls = self.current_class.get()
        # 画笔半径（图像像素）。UI 上的 brush_size 是图像坐标系下的值，
        # 因此放大后视觉上变小，正是用户期望的"细节涂抹"效果。
        r_img = max(1, self.brush_size.get())

        ix, iy = self._canvas_to_image_pt(event.x, event.y)

        # 在图像坐标系下生成圆盘，必要时在两点之间插值连接
        def stamp(cx, cy):
            y_min, y_max = max(0, int(cy) - r_img), min(h, int(cy) + r_img + 1)
            x_min, x_max = max(0, int(cx) - r_img), min(w, int(cx) + r_img + 1)
            if y_min < y_max and x_min < x_max:
                Y, X = np.ogrid[y_min:y_max, x_min:x_max]
                dist_sq = (Y - cy) ** 2 + (X - cx) ** 2
                m = dist_sq <= r_img ** 2
                img_data['annotations'][y_min:y_max, x_min:x_max][m] = cls

        stamp(ix, iy)
        # 与上一点插值，避免快速拖动出现断点
        if self._last_paint_img_pt is not None:
            lx, ly = self._last_paint_img_pt
            dist = ((ix - lx) ** 2 + (iy - ly) ** 2) ** 0.5
            # 沿连线每隔 r_img/3 像素盖一个章
            step = max(1, r_img / 3.0)
            n = int(dist / step)
            if n > 0:
                for k in range(1, n + 1):
                    t = k / n
                    stamp(lx + (ix - lx) * t, ly + (iy - ly) * t)
        self._last_paint_img_pt = (ix, iy)

        # 性能优化：只重绘标注层（~15ms），不重新缩放原图（~100ms）
        self._refresh_annotation_only()
        self.is_trained = False

    def clear_current_annotations(self):
        if not self.images: return
        self.images[self.current_idx]['annotations'].fill(-1)
        self._refresh_annotation_only()
        self.is_trained = False

    # ---------------------------- 特征配置（监督模式）--------------------
    def _on_feature_config_change(self):
        self.feature_config = {
            "intensity": self.intensity_var.get(),
            "gaussian": self.gaussian_var.get(),
            "edges": self.edges_var.get(),
            "texture": self.texture_var.get()
        }
        for img in self.images:
            img['features'] = None
        self.is_trained = False

    def _extract_features_for_image(self, img_data):
        config = self.feature_config
        gray = cv2.cvtColor(img_data['array'], cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
        features_list = []
        if config["intensity"]:
            features_list.append(gray)
        for sigma in self.sigmas:
            blurred = cv2.GaussianBlur(gray, (0,0), sigmaX=sigma)
            if config["gaussian"]:
                features_list.append(blurred)
            if config["edges"]:
                sobel_x = cv2.Sobel(blurred, cv2.CV_32F, 1, 0, ksize=3)
                sobel_y = cv2.Sobel(blurred, cv2.CV_32F, 0, 1, ksize=3)
                edges = np.hypot(sobel_x, sobel_y)
                features_list.append(edges)
            if config["texture"]:
                laplace = cv2.Laplacian(blurred, cv2.CV_32F, ksize=3)
                features_list.append(np.abs(laplace))
        features = np.stack(features_list, axis=-1).astype(np.float32)
        img_data['features'] = features
        return features

    # ---------------------------- 训练 ----------------------------
    def train_model(self):
        if not self.images:
            messagebox.showwarning("警告", "请先添加图像")
            return
        # 禁用按钮，避免重复点击
        self._set_busy(True, "训练中… 请稍候")
        self.progress.start()
        threading.Thread(target=self._train_worker, daemon=True).start()

    def _train_worker(self):
        try:
            if self.mode_var.get() == "supervised":
                self._set_status("训练中：提取特征…")
                self._train_supervised()
            else:
                self._set_status("训练中：提取 Laws 纹理特征…")
                self._train_anomaly()
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror("训练错误", error_msg))
            self.root.after(0, lambda: self.status_var.set(f"训练失败: {error_msg}"))
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self._set_busy(False))

    def _train_supervised(self):
        X_list, y_list = [], []
        for img in self.images:
            if img['features'] is None:
                self._extract_features_for_image(img)
            feats = img['features']
            ann = img['annotations']
            mask = ann != -1
            if np.any(mask):
                X_list.append(feats[mask])
                y_list.append(ann[mask])
        if not X_list:
            raise ValueError("没有找到任何标注数据，请先涂抹标记")
        X_train = np.vstack(X_list)
        y_train = np.concatenate(y_list)
        unique = np.unique(y_train)
        if len(unique) < 2:
            raise ValueError(f"监督模式需要至少两个类别（0和1），当前只有 {unique}")
        MAX_SAMPLES = 20000
        if len(X_train) > MAX_SAMPLES:
            idx = np.random.choice(len(X_train), MAX_SAMPLES, replace=False)
            X_train, y_train = X_train[idx], y_train[idx]
        clf_builder = self.classifiers[self.clf_var.get()]
        self.model = clf_builder()
        self._set_status(f"训练中：拟合 {self.clf_var.get()} （{len(X_train)} 样本）…")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        msg = f"✅ 监督训练完成! 样本量: {len(X_train)}, 特征维度: {X_train.shape[1]}"
        self.root.after(0, lambda: self.status_var.set(msg))

    def _train_anomaly(self):
        X_list = []
        for img in self.images:
            laws_feat = BaseAnomalyDetector.extract_laws_features(img['array'])
            ann = img['annotations']
            normal_mask = ann == 0
            if np.any(normal_mask):
                X_list.append(laws_feat[normal_mask])
        if not X_list:
            raise ValueError("异常检测模式需要至少100个正常纹理样本（类别0），请涂抹红色标记")
        X_train = np.vstack(X_list)
        if len(X_train) < 100:
            raise ValueError(f"正常样本不足100，当前只有 {len(X_train)} 个，请增加标记")
        algo = self.anomaly_algo.get()
        if algo == "gmm":
            self.model = GMMAnomalyDetector(
                n_components=self.gmm_components.get(),
                percentile_threshold=self.percentile_threshold.get() / 100.0
            )
        else:
            self.model = OneClassSVMAnomalyDetector(
                nu=self.svm_nu.get(),
                gamma=self.svm_gamma.get()
            )
        self._set_status(f"训练中：拟合 {algo.upper()} （{len(X_train)} 样本）…")
        self.model.fit(X_train)
        self.is_trained = True
        msg = f"✅ 异常检测训练完成! 正常样本数: {len(X_train)}, 算法: {algo.upper()}"
        self.root.after(0, lambda: self.status_var.set(msg))

    # ---------------------------- 预测 ----------------------------
    def predict_current_image(self):
        if not self.is_trained or self.model is None:
            messagebox.showwarning("提示", "请先训练模型")
            return
        if not self.images:
            return
        self._set_busy(True, "预测中… 请稍候")
        self.progress.start()
        threading.Thread(target=self._predict_worker, daemon=True).start()

    def _predict_worker(self):
        try:
            img_data = self.images[self.current_idx]
            alpha = self.overlay_alpha.get()
            if self.mode_var.get() == "supervised":
                self._set_status("预测中：提取特征…")
                if img_data['features'] is None:
                    self._extract_features_for_image(img_data)
                feats = img_data['features']
                h, w, d = feats.shape
                X_all = feats.reshape(-1, d)
                self._set_status(f"预测中：推理 {len(X_all)} 个像素…")
                pred = self.model.predict(X_all).reshape(h, w)
                overlay = np.zeros((h, w, 4), dtype=np.uint8)
                overlay[pred == 0] = [255, 0, 0, alpha]
                overlay[pred == 1] = [0, 255, 0, alpha]
                combined = Image.alpha_composite(img_data['image'].convert("RGBA"), Image.fromarray(overlay))
            else:
                self._set_status("预测中：提取 Laws 纹理特征…")
                laws_feat = BaseAnomalyDetector.extract_laws_features(img_data['array'])
                h, w = laws_feat.shape[:2]
                X_all = laws_feat.reshape(-1, 5)
                self._set_status(f"预测中：推理 {len(X_all)} 个像素…")
                _, is_anomaly = self.model.predict(X_all)
                is_anomaly = is_anomaly.reshape(h, w)
                self._set_status("预测中：后处理（形态学 + 连通域过滤）…")
                is_anomaly = self.model.postprocess_mask(is_anomaly, min_area=30)
                overlay = np.zeros((h, w, 4), dtype=np.uint8)
                overlay[is_anomaly] = [255, 0, 0, alpha]
                combined = Image.alpha_composite(img_data['image'].convert("RGBA"), Image.fromarray(overlay))
            self._set_status("预测中：生成叠加图…")
            self._last_prediction_overlay = combined
            self.root.after(0, self._update_prediction_ui)
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror("预测错误", error_msg))
            self.root.after(0, lambda: self.status_var.set(f"预测失败: {error_msg}"))
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self._set_busy(False))

    def _update_prediction_ui(self):
        self._redraw_full(force_hq=True)
        n_defect = int((np.array(self._last_prediction_overlay)[:, :, 3] > 0).sum()) if self._last_prediction_overlay else 0
        self.status_var.set(f"✅ 检测完成 (可滚轮放大查看细节)")

    # ---------------------------- 忙碌状态管理 ----------------------------
    _busy_button_specs = [
        # (控件属性名, 文本)
        ('_btn_train', '🚀 训练模型'),
        ('_btn_predict', '🔍 预测当前图像'),
    ]

    def _set_busy(self, busy, status_prefix=""):
        """训练/预测时禁用主操作按钮，避免重复点击；并在状态栏显示提示。"""
        # 按钮已在 _build_action_frame 中保存为属性，这里直接禁用/启用
        for attr, _ in self._busy_button_specs:
            btn = getattr(self, attr, None)
            if btn is not None:
                btn.config(state=tk.DISABLED if busy else tk.NORMAL)
        if busy and status_prefix:
            self.status_var.set(status_prefix)

    def _set_status(self, text):
        """线程安全地更新状态栏（训练/预测 worker 调用）。"""
        self.root.after(0, lambda: self.status_var.set(text))

    # ---------------------------- 模型导出 (纯模型) ----------------------------
    def export_model_only(self):
        if not self.is_trained or self.model is None:
            messagebox.showwarning("警告", "没有已训练的模型可导出")
            return
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Pickle model", "*.pkl")],
            title="导出纯模型文件 (供 Python 调用)"
        )
        if not filepath:
            return
        try:
            export_dict = {
                'model': self.model,
                'mode': self.mode_var.get(),
                'anomaly_algo': self.anomaly_algo.get() if self.mode_var.get() == "anomaly" else None,
                'feature_config': self.feature_config if self.mode_var.get() == "supervised" else None,
                'sigmas': self.sigmas,
                # 记录监督模式下的特征维度，便于推理时校验
                'feature_dim': self._current_feature_dim(),
                'app_version': 'v2-with-zoom',
            }
            joblib.dump(export_dict, filepath)
            self.status_var.set(f"模型已导出至: {filepath}")
            messagebox.showinfo("成功", "模型导出成功！\n\n可使用 infer_demo.py 进行推理：\n\npython infer_demo.py --model <此文件> --image <待测图片> --output <输出目录>")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    def _current_feature_dim(self):
        """估算当前监督模式的特征维度，供推理脚本校验。"""
        if not self.images:
            return None
        img = self.images[self.current_idx]
        try:
            if img['features'] is None:
                self._extract_features_for_image(img)
            return int(img['features'].shape[-1])
        except Exception:
            return None

    # ---------------------------- 工程导入/导出 ----------------------------
    def export_project(self):
        if not self.images:
            messagebox.showwarning("警告", "没有图像可导出")
            return
        if not self.is_trained:
            if not messagebox.askyesno("提示", "模型尚未训练，是否仍导出当前标注数据？"):
                return
        filepath = filedialog.asksaveasfilename(defaultextension=".pcp", filetypes=[("Project", "*.pcp")])
        if not filepath:
            return
        images_info = []
        for img in self.images:
            y_idx, x_idx = np.where(img['annotations'] != -1)
            cls_vals = img['annotations'][y_idx, x_idx]
            images_info.append({
                'path': img['path'],
                'annotations': list(zip(y_idx, x_idx, cls_vals))
            })
        data = {
            'classifier_name': self.clf_var.get(),
            'model': self.model,
            'feature_config': self.feature_config,
            'images_info': images_info,
            'mode': self.mode_var.get(),
            'anomaly_algo': self.anomaly_algo.get(),
            'gmm_components': self.gmm_components.get(),
            'percentile_threshold': self.percentile_threshold.get(),
            'svm_nu': self.svm_nu.get(),
            'svm_gamma': self.svm_gamma.get(),
            'brush_size': self.brush_size.get(),
            'overlay_alpha': self.overlay_alpha.get()
        }
        joblib.dump(data, filepath)
        self.status_var.set("工程已保存")

    def load_project(self, event=None):
        filepath = filedialog.askopenfilename(filetypes=[("Project", "*.pcp")])
        if not filepath:
            return
        try:
            data = joblib.load(filepath)
            self.mode_var.set(data.get('mode', 'supervised'))
            self.clf_var.set(data['classifier_name'])
            self.feature_config = data['feature_config']
            self.anomaly_algo.set(data.get('anomaly_algo', 'gmm'))
            self.gmm_components.set(data.get('gmm_components', 5))
            self.percentile_threshold.set(data.get('percentile_threshold', 0.1))
            self.svm_nu.set(data.get('svm_nu', 0.0005))
            self.svm_gamma.set(data.get('svm_gamma', 0.01))
            self.brush_size.set(data.get('brush_size', 5))
            self.overlay_alpha.set(data.get('overlay_alpha', 150))
            self.images = []
            for info in data['images_info']:
                path = info['path']
                if not os.path.exists(path):
                    new_path = filedialog.askopenfilename(title=f"找不到图像: {path}\n请手动选择新路径")
                    if not new_path:
                        continue
                    path = new_path
                pil_img = Image.open(path).convert("RGB")
                pil_img.thumbnail((1000, 1000), Image.LANCZOS)
                arr = np.array(pil_img)
                h, w = arr.shape[:2]
                ann_mask = np.full((h, w), -1, dtype=np.int8)
                for (y, x, cls) in info['annotations']:
                    if 0 <= y < h and 0 <= x < w:
                        ann_mask[y, x] = cls
                self.images.append({
                    'path': path, 'image': pil_img, 'array': arr,
                    'annotations': ann_mask, 'features': None, 'w': w, 'h': h
                })
            if not self.images:
                raise ValueError("没有成功加载任何图像")
            self.model = data.get('model')
            self.is_trained = self.model is not None
            self.current_idx = 0
            self._last_prediction_overlay = None
            self.fit_to_window()
            self._update_image_listbox()
            self._update_ui_state()
            self.status_var.set("工程已加载")
        except Exception as e:
            messagebox.showerror("加载错误", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelClassifierApp(root)
    root.mainloop()
