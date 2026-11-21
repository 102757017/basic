# -*- coding: utf-8 -*-
"""
光照不均匀处理工具（引导滤波核心层 + 三种任务预设）
核心层固定用 cv2.ximgproc.guidedFilter 提取，base_layer 按任务不同做不同处理：
  1. 二值化预处理：base 拉平 → 消除明暗差，为 Otsu/自适应阈值做准备
  2. 提亮暗部细节：base 做暗部增益映射，保留亮部不过曝
  3. 提亮亮部细节：base 做亮部压缩映射，保留暗部层次
依赖：pip install opencv-contrib-python pillow numpy
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import cv2


# ---------------- 引导滤波（直接调用 ximgproc） ----------------

def guided_filter(gray, radius, eps):
    """
    gray: float32 [0,1] 单通道
    返回同形状 base_layer（光照图）
    直接调用 cv2.ximgproc.guidedFilter，需要 opencv-contrib-python
    """
    return cv2.ximgproc.guidedFilter(gray, gray, radius, eps)


# ---------------- 三种 base_layer 任务处理 ----------------

def base_for_binarization(base, strength=1.0):
    """任务1：为二值化做准备 —— 把光照图整体拉向常数，压掉明暗差"""
    target = float(np.mean(base))
    out = base + (target - base) * strength
    return np.clip(out, 0, 1)


def base_for_shadow(base, gain=1.6, offset=0.35):
    """任务2：提亮暗部 —— S 形曲线，暗部强提亮、亮部基本不动"""
    x = (base - offset) * gain
    out = 1.0 / (1.0 + np.exp(-x))
    out = (out - out.min()) / (out.max() - out.min() + 1e-8)
    out = base * 0.25 + out * 0.75
    return np.clip(out, 0, 1)


def base_for_highlight(base, gamma=0.45):
    """任务3：提亮亮部细节 —— gamma<1 压缩高光区，拉开亮部层次"""
    out = np.power(np.clip(base, 1e-6, 1.0), gamma)
    out = out / out.max()
    return np.clip(out, 0, 1)


TASKS = {
    "① 二值化预处理（拉平光照）": base_for_binarization,
    "② 提亮暗部细节（S曲线）":   base_for_shadow,
    "③ 提亮亮部细节（Gamma）":   base_for_highlight,
}


# ---------------- 主处理流程 ----------------

def process_image(img_bgr, task_name, radius=30, eps=0.01,
                  strength=1.0, gain=1.6, offset=0.35, gamma=0.45,
                  color_mode="lab"):
    """
    返回 (result_bgr, base_layer, detail_layer)
    color_mode: 'lab' 只在亮度通道处理（保色，推荐）；'gray' 等价原版
    """
    img_f = img_bgr.astype(np.float32) / 255.0

    if color_mode == "lab":
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB).astype(np.float32) / 255.0
        L = lab[..., 0]
        base = guided_filter(L, radius, eps)
        fn = TASKS[task_name]
        if fn is base_for_binarization:
            base_adj = fn(base, strength)
        elif fn is base_for_shadow:
            base_adj = fn(base, gain, offset)
        else:
            base_adj = fn(base, gamma)
        detail = L - base
        lab[..., 0] = np.clip(base_adj + detail, 0, 1)
        out = cv2.cvtColor((lab * 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
        return out, base, detail
    else:  # gray
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
        base = guided_filter(gray, radius, eps)
        fn = TASKS[task_name]
        if fn is base_for_binarization:
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
        self.title("光照不均匀处理（引导滤波核心层）")
        self.geometry("1180x720")
        self.img_bgr = None
        self._result = None
        self._base = None
        self._build_ui()

    def _build_ui(self):
        # 左侧参数区
        left = ttk.Frame(self, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left, text="任务模式", font=("", 10, "bold")).pack(anchor="w")
        self.task_var = tk.StringVar(value=list(TASKS.keys())[0])
        self.task_box = ttk.Combobox(left, textvariable=self.task_var,
                                     values=list(TASKS.keys()), state="readonly", width=26)
        self.task_box.pack(anchor="w", pady=(2, 10))
        self.task_box.bind("<<ComboboxSelected>>", self._on_task_change)

        # 引导滤波参数（固定核心层）
        gf = ttk.LabelFrame(left, text="引导滤波（核心层，固定）", padding=8)
        gf.pack(fill=tk.X, pady=5)
        self.radius_frame, self.radius = self._slider(gf, "Radius（越大越平滑）", 5, 80, 30)
        self.eps_frame, self.eps = self._slider(gf, "Eps（边缘保持）", 0.001, 0.1, 0.01, step=0.001)

        # 任务专属参数
        self.task_frame = ttk.LabelFrame(left, text="base_layer 处理参数", padding=8)
        self.task_frame.pack(fill=tk.X, pady=5)
        
        # 创建滑块并保存 (frame, var) 元组
        self.slider_strength_frame, self.slider_strength = self._slider(self.task_frame, "拉平强度 strength", 0.0, 1.0, 1.0, step=0.05)
        self.slider_gain_frame, self.slider_gain = self._slider(self.task_frame, "暗部增益 gain", 0.5, 4.0, 1.6, step=0.1)
        self.slider_offset_frame, self.slider_offset = self._slider(self.task_frame, "暗部阈值 offset", 0.0, 1.0, 0.35, step=0.05)
        self.slider_gamma_frame, self.slider_gamma = self._slider(self.task_frame, "亮部 gamma", 0.1, 1.0, 0.45, step=0.05)

        # 色彩模式
        cm = ttk.LabelFrame(left, text="色彩模式", padding=8)
        cm.pack(fill=tk.X, pady=5)
        self.color_var = tk.StringVar(value="lab")
        ttk.Radiobutton(cm, text="LAB 亮度通道（保色，推荐）", variable=self.color_var,
                        value="lab", command=self.apply).pack(anchor="w")
        ttk.Radiobutton(cm, text="灰度（等价原版）", variable=self.color_var,
                        value="gray", command=self.apply).pack(anchor="w")

        # 按钮
        btns = ttk.Frame(left)
        btns.pack(fill=tk.X, pady=12)
        ttk.Button(btns, text="打开图片", command=self.open_image).pack(fill=tk.X, pady=2)
        ttk.Button(btns, text="应用处理", command=self.apply).pack(fill=tk.X, pady=2)
        ttk.Button(btns, text="保存结果", command=self.save_image).pack(fill=tk.X, pady=2)
        ttk.Button(btns, text="导出 base_layer", command=self.save_base).pack(fill=tk.X, pady=2)

        self.status = ttk.Label(left, text="未加载图片", foreground="gray")
        self.status.pack(anchor="w", pady=6)

        # 右侧图像区：原图 / 结果 / base / detail 四宫格
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

        self._on_task_change() # 初始化时调用一次，设置初始显示状态

    def _slider(self, parent, label, lo, hi, init, step=1):
        """创建滑块，返回 (frame容器, DoubleVar变量)"""
        f = ttk.Frame(parent)
        f.pack(fill=tk.X, pady=2)
        ttk.Label(f, text=label, width=22).pack(side=tk.LEFT)
        v = tk.DoubleVar(value=init)
        s = ttk.Scale(f, from_=lo, to=hi, variable=v, length=180)
        s.pack(side=tk.LEFT, fill=tk.X, expand=True)
        val = ttk.Label(f, text=f"{init:.3f}", width=7)
        val.pack(side=tk.RIGHT)
        
        # 拖动滑块时更新数值并触发防抖重算
        def on_change(x):
            val.configure(text=f"{float(x):.3f}")
            self.schedule_apply()
            
        s.configure(command=on_change)
        return f, v  # 修复：返回 frame 和 var 的元组

    def _on_task_change(self, event=None):
        """切换任务模式时，动态显示/隐藏对应的参数滑块"""
        t = self.task_var.get()
        
        # 先全部隐藏（操作 frame 容器）
        for child in self.task_frame.winfo_children():
            child.pack_forget()
            
        # 根据任务模式显示对应滑块（操作 frame 容器）
        if t == "① 二值化预处理（拉平光照）":
            self.slider_strength_frame.pack(fill=tk.X, pady=2)
        elif t == "② 提亮暗部细节（S曲线）":
            self.slider_gain_frame.pack(fill=tk.X, pady=2)
            self.slider_offset_frame.pack(fill=tk.X, pady=2)
        elif t == "③ 提亮亮部细节（Gamma）":
            self.slider_gamma_frame.pack(fill=tk.X, pady=2)
            
        self.status.configure(text=f"当前任务：{t}")
        self.apply() # 切换模式后立即刷新一次画面

    def schedule_apply(self):
        """防抖：停止拖动滑块 120ms 后才真正执行重算，避免卡顿"""
        if hasattr(self, '_debounce_id'):
            self.after_cancel(self._debounce_id)
        self._debounce_id = self.after(120, self.apply)

    def open_image(self):
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
                ("JPG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
                ("所有文件", "*.*")
            ])
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
                color_mode=self.color_var.get())
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
        self.canvas[name].image = photo  # 防 GC

    def save_image(self):
        if self._result is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPG", "*.jpg"), ("PNG", "*.png")])
        if path:
            cv2.imwrite(path, self._result)
            self.status.configure(text=f"已保存：{path}")

    def save_base(self):
        if self._base is None:
            return
        path = filedialog.asksaveasfilename(
            title="保存 base_layer",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg"), ("所有文件", "*.*")])
        if path:
            cv2.imwrite(path, (np.clip(self._base, 0, 1) * 255).astype(np.uint8))
            self.status.configure(text=f"base_layer 已保存：{path}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
