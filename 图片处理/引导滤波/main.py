# -*- coding: utf-8 -*-
"""
光照不均匀处理工具（多尺度引导滤波核心层 + 三种任务预设）
依赖：pip install opencv-contrib-python pillow numpy
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import cv2


# ---------------- 引导滤波基础函数 ----------------

def guided_filter(gray, radius, eps):
    """单尺度引导滤波"""
    return cv2.ximgproc.guidedFilter(gray, gray, radius, eps)


def multi_scale_guided_filter(gray, radii=[5, 15, 30, 60], eps=0.01, weights=None):
    """
    多尺度引导滤波融合
    gray: float32 [0,1] 单通道
    radii: 多个滤波半径列表，从小到大
    weights: 各尺度权重，默认均匀
    返回: 融合后的 base_layer
    """
    if weights is None:
        weights = [1.0 / len(radii)] * len(radii)
    
    # 归一化权重
    weights = np.array(weights, dtype=np.float32)
    weights /= weights.sum()
    
    # 多尺度分解与融合
    base_fused = np.zeros_like(gray, dtype=np.float32)
    for r, w in zip(radii, weights):
        base = guided_filter(gray, r, eps)
        base_fused += base * w
        
    return np.clip(base_fused, 0, 1)


# ---------------- 任务处理函数 ----------------

def base_for_binarization_multiscale(base, strength=1.0):
    """任务1升级：多尺度拉平光照"""
    target = float(np.mean(base))
    out = base + (target - base) * strength
    return np.clip(out, 0, 1)


def base_for_shadow(base, gain=1.6, offset=0.35):
    """任务2：提亮暗部"""
    x = (base - offset) * gain
    out = 1.0 / (1.0 + np.exp(-x))
    out = (out - out.min()) / (out.max() - out.min() + 1e-8)
    out = base * 0.25 + out * 0.75
    return np.clip(out, 0, 1)


def base_for_highlight(base, gamma=0.45):
    """任务3：提亮亮部"""
    out = np.power(np.clip(base, 1e-6, 1.0), gamma)
    out = out / out.max()
    return np.clip(out, 0, 1)


TASKS = {
    "① 二值化预处理（多尺度拉平）": base_for_binarization_multiscale,
    "② 提亮暗部细节（S曲线）":   base_for_shadow,
    "③ 提亮亮部细节（Gamma）":   base_for_highlight,
}


# ---------------- 主处理流程 ----------------

def process_image(img_bgr, task_name, radius=30, eps=0.01,
                  strength=1.0, gain=1.6, offset=0.35, gamma=0.45,
                  color_mode="lab", use_multiscale=True):
    img_f = img_bgr.astype(np.float32) / 255.0

    if color_mode == "lab":
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB).astype(np.float32) / 255.0
        L = lab[..., 0]
        
        # 根据是否启用多尺度选择滤波方式
        if use_multiscale and task_name.startswith("①"):
            # 多尺度引导滤波：小半径保边缘，大半径去光照
            base = multi_scale_guided_filter(L, radii=[5, 15, 30, 60], eps=eps)
        else:
            base = guided_filter(L, radius, eps)
            
        fn = TASKS[task_name]
        if fn is base_for_binarization_multiscale:
            base_adj = fn(base, strength)
        elif fn is base_for_shadow:
            base_adj = fn(base, gain, offset)
        else:
            base_adj = fn(base, gamma)
            
        detail = L - base
        lab[..., 0] = np.clip(base_adj + detail, 0, 1)
        out = cv2.cvtColor((lab * 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
        return out, base, detail
    else:
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        
        if use_multiscale and task_name.startswith("①"):
            base = multi_scale_guided_filter(gray, radii=[5, 15, 30, 60], eps=eps)
        else:
            base = guided_filter(gray, radius, eps)
            
        fn = TASKS[task_name]
        if fn is base_for_binarization_multiscale:
            base_adj = fn(base, strength)
        elif fn is base_for_shadow:
            base_adj = fn(base, gain, offset)
        else:
            base_adj = fn(base, gamma)
            
        detail = img_f - base[..., None]
        out = np.clip((base_adj[..., None] + detail) * 255, 0, 255).astype(np.uint8)
        return out, base, detail


# ---------------- Tkinter 界面 ----------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("光照不均匀处理（多尺度引导滤波）")
        self.geometry("1180x720")
        self.img_bgr = None
        self._result = None
        self._base = None
        self._build_ui()

    def _build_ui(self):
        left = ttk.Frame(self, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left, text="任务模式", font=("", 10, "bold")).pack(anchor="w")
        self.task_var = tk.StringVar(value=list(TASKS.keys())[0])
        self.task_box = ttk.Combobox(left, textvariable=self.task_var,
                                     values=list(TASKS.keys()), state="readonly", width=26)
        self.task_box.pack(anchor="w", pady=(2, 10))
        self.task_box.bind("<<ComboboxSelected>>", self._on_task_change)

        # 引导滤波参数
        gf = ttk.LabelFrame(left, text="引导滤波参数", padding=8)
        gf.pack(fill=tk.X, pady=5)
        
        # 多尺度开关（仅任务①有效，外层 row 常驻以保证控件顺序）
        self.multiscale_var = tk.BooleanVar(value=True)
        self.multiscale_row = ttk.Frame(gf)
        self.multiscale_row.pack(fill=tk.X)
        self.multiscale_chk = ttk.Checkbutton(self.multiscale_row, text="启用多尺度融合（推荐）",
                                              variable=self.multiscale_var,
                                              command=self._on_multiscale_toggle)
        self.multiscale_chk.pack(anchor="w", pady=(0, 5))
        
        self.radius_frame, self.radius = self._slider(gf, "单尺度 Radius", 5, 80, 30)
        self.eps_frame, self.eps = self._slider(gf, "Eps（边缘保持）", 0.001, 0.1, 0.01, step=0.001)

        # 任务专属参数
        self.task_frame = ttk.LabelFrame(left, text="base_layer 处理参数", padding=8)
        self.task_frame.pack(fill=tk.X, pady=5)
        
        self.slider_strength_frame, self.slider_strength = self._slider(self.task_frame, "拉平强度 strength", 0.0, 1.0, 1.0, step=0.05)
        self.slider_gain_frame, self.slider_gain = self._slider(self.task_frame, "暗部增益 gain", 0.5, 4.0, 1.6, step=0.1)
        self.slider_offset_frame, self.slider_offset = self._slider(self.task_frame, "暗部阈值 offset", 0.0, 1.0, 0.35, step=0.05)
        self.slider_gamma_frame, self.slider_gamma = self._slider(self.task_frame, "亮部 gamma", 0.1, 1.0, 0.45, step=0.05)

        # 色彩模式
        cm = ttk.LabelFrame(left, text="色彩模式", padding=8)
        cm.pack(fill=tk.X, pady=5)
        self.color_var = tk.StringVar(value="lab")
        ttk.Radiobutton(cm, text="LAB 亮度通道（保色，推荐）", variable=self.color_var,
                        value="lab", command=self.schedule_apply).pack(anchor="w")
        ttk.Radiobutton(cm, text="灰度（等价原版）", variable=self.color_var,
                        value="gray", command=self.schedule_apply).pack(anchor="w")

        # 按钮
        btns = ttk.Frame(left)
        btns.pack(fill=tk.X, pady=12)
        ttk.Button(btns, text="打开图片", command=self.open_image).pack(fill=tk.X, pady=2)
        ttk.Button(btns, text="应用处理", command=self.apply).pack(fill=tk.X, pady=2)
        ttk.Button(btns, text="保存结果", command=self.save_image).pack(fill=tk.X, pady=2)
        ttk.Button(btns, text="导出 base_layer", command=self.save_base).pack(fill=tk.X, pady=2)

        self.status = ttk.Label(left, text="未加载图片", foreground="gray")
        self.status.pack(anchor="w", pady=6)

        # 右侧图像区
        right = ttk.Frame(self, padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = {}
        for i, name in enumerate(["原图", "处理结果", "base_layer(光照图)", "detail_layer(细节)"]):
            f = ttk.LabelFrame(right, text=name, padding=4)
            f.grid(row=i // 2, column=i % 2, sticky="nsew", padx=5, pady=5)
            self.canvas[name] = ttk.Label(f, anchor="center")
            self.canvas[name].pack(fill=tk.BOTH, expand=True)
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)
        right.columnconfigure(1, weight=1)

        self._on_task_change()

    def _slider(self, parent, label, lo, hi, init, step=1):
        f = ttk.Frame(parent)
        f.pack(fill=tk.X, pady=2)
        ttk.Label(f, text=label, width=22).pack(side=tk.LEFT)
        v = tk.DoubleVar(value=init)
        s = ttk.Scale(f, from_=lo, to=hi, variable=v, length=180)
        s.pack(side=tk.LEFT, fill=tk.X, expand=True)
        val = ttk.Label(f, text=f"{init:.3f}", width=7)
        val.pack(side=tk.RIGHT)
        
        def on_change(x):
            val.configure(text=f"{float(x):.3f}")
            self.schedule_apply()
            
        s.configure(command=on_change)
        return f, v

    def _on_task_change(self, event=None):
        t = self.task_var.get()
        is_task1 = t.startswith("①")
        
        for child in self.task_frame.winfo_children():
            child.pack_forget()
        
        # 多尺度融合仅对任务①生效，其它预设隐藏该控件
        if is_task1:
            self.multiscale_chk.pack(anchor="w", pady=(0, 5))
        else:
            self.multiscale_chk.pack_forget()
            
        # 根据任务模式动态显示参数
        if is_task1:
            self.slider_strength_frame.pack(fill=tk.X, pady=2)
            # 多尺度模式下隐藏单尺度Radius滑块
            if self.multiscale_var.get():
                self.radius_frame.pack_forget()
            else:
                self.radius_frame.pack(fill=tk.X, pady=2)
        elif t.startswith("②"):
            self.slider_gain_frame.pack(fill=tk.X, pady=2)
            self.slider_offset_frame.pack(fill=tk.X, pady=2)
            self.radius_frame.pack(fill=tk.X, pady=2)
        elif t.startswith("③"):
            self.slider_gamma_frame.pack(fill=tk.X, pady=2)
            self.radius_frame.pack(fill=tk.X, pady=2)
            
        self.status.configure(text=f"当前任务：{t}")
        self.schedule_apply()

    def _on_multiscale_toggle(self):
        """多尺度开关切换时同步 Radius 滑块显隐（仅任务①）"""
        if self.task_var.get().startswith("①"):
            if self.multiscale_var.get():
                self.radius_frame.pack_forget()
            else:
                self.radius_frame.pack(fill=tk.X, pady=2)
        self.schedule_apply()

    def schedule_apply(self):
        if hasattr(self, '_debounce_id'):
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(120, self.apply)

    def open_image(self):
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"), ("所有文件", "*.*")])
        if not path:
            return
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            messagebox.showerror("错误", "无法读取图片")
            return
        self.img_bgr = img
        self._show("原图", img)
        self.status.configure(text=f"已加载：{path}")
        self.apply()

    def apply(self):
        if self.img_bgr is None:
            return
        try:
            result, base, detail = process_image(
                self.img_bgr, self.task_var.get(),
                radius=int(self.radius.get()), eps=float(self.eps.get()),
                strength=float(self.slider_strength.get()),
                gain=float(self.slider_gain.get()), offset=float(self.slider_offset.get()),
                gamma=float(self.slider_gamma.get()),
                color_mode=self.color_var.get(),
                use_multiscale=self.multiscale_var.get())
        except Exception as e:
            messagebox.showerror("处理失败", str(e))
            return
        self._result = result
        self._base = base
        self._show("处理结果", result)
        self._show("base_layer(光照图)", (np.clip(base, 0, 1) * 255).astype(np.uint8))
        d = np.clip((detail + 0.5) * 255, 0, 255).astype(np.uint8)
        self._show("detail_layer(细节)", d)

    def _show(self, name, img):
        h, w = img.shape[:2]
        scale = min(520 / w, 320 / h, 1.0)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        from PIL import Image, ImageTk
        photo = ImageTk.PhotoImage(Image.fromarray(img))
        self.canvas[name].configure(image=photo)
        self.canvas[name].image = photo

    def save_image(self):
        if self._result is None:
            return
        path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                            filetypes=[("JPG", "*.jpg"), ("PNG", "*.png")])
        if path:
            cv2.imwrite(path, self._result)
            self.status.configure(text=f"已保存：{path}")

    def save_base(self):
        if self._base is None:
            return
        path = filedialog.asksaveasfilename(title="保存 base_layer",
                                            defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")])
        if path:
            cv2.imwrite(path, (np.clip(self._base, 0, 1) * 255).astype(np.uint8))
            self.status.configure(text=f"base_layer 已保存：{path}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
