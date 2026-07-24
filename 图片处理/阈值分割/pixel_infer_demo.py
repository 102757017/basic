#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
infer_demo.py
=============

像素分类器 / 纹理缺陷检测 — 独立推理脚本
---------------------------------------

本脚本用于加载由 `pixel_classifier.py` 导出的纯模型 `.pkl` 文件，
对单张或多张图像进行缺陷检测，输出：
  1. 二值缺陷 mask（白=缺陷，黑=正常），PNG 灰度
  2. 彩色叠加图（原图 + 红/绿预测着色），PNG
  3. （可选）异常分数热力图（仅 anomaly 模式有效）

用法
----
# 单张图片
python infer_demo.py \
    --model model.pkl \
    --image test.png \
    --output ./out

# 一个目录下所有图片
python infer_demo.py \
    --model model.pkl \
    --image_dir ./test_images \
    --output ./out \
    --alpha 150

# 仅输出 mask，不输出叠加图（节省时间）
python infer_demo.py --model model.pkl --image test.png --output ./out --no_overlay

依赖
----
- numpy
- opencv-python
- Pillow
- scikit-learn
- joblib

如果原模型是 GMM / OneClassSVM 异常检测器，本脚本会自动调用对应的
特征提取（Laws 纹理能量）+ 后处理（形态学 + 连通域面积过滤）流程，
与训练时完全一致。

作者：Super Z
"""

import argparse
import os
import sys
import glob
import numpy as np
import cv2
from PIL import Image
import joblib
from sklearn.mixture import GaussianMixture
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler


# ============================================================
# 异常检测器类定义
# ============================================================
# 这些类必须定义在本文件中，否则 joblib.load() 反序列化 .pkl 模型时
# 会找不到类。我们让本文件的类与 pixel_classifier.py 中的类保持二进制
# 兼容（同名、同字段、同方法），这样无论模型在哪里训练，都能在本脚本
# 中加载。注意：pickle 是按 "module.qualname" 来定位类的，所以这里
# 模块名必须与训练时一致 → 见文末的 _install_class_aliases()。
# ============================================================

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
            np.outer(E5, L5),
            np.outer(L5, E5),
            np.outer(E5, S5),
            np.outer(S5, E5),
            np.outer(E5, E5),
        ]

    @staticmethod
    def postprocess_mask(mask, min_area=30):
        mask_u8 = mask.astype(np.uint8) * 255
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        opened = cv2.morphologyEx(mask_u8, cv2.MORPH_OPEN, kernel_open)
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
        result = np.zeros_like(mask_u8, dtype=np.uint8)
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area >= min_area:
                result[labels == i] = 255
        return result > 0


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


def _install_class_aliases():
    """
    让 pickle 在反序列化时能在本模块下找到原训练模块里定义的异常检测器类。

    原 .pkl 模型里类引用形如：
        pixel_classifier.GMMAnomalyDetector
        pixel_classifier.OneClassSVMAnomalyDetector
        pixel_classifier.BaseAnomalyDetector

    本脚本作为独立模块运行（模块名 `__main__` 或 `infer_demo`），
    需要把这些类注册到 `pixel_classifier` 这个模块名下，
    pickle 才能正确找到类。注册是幂等的，重复调用无副作用。
    """
    import sys
    import types
    if 'pixel_classifier' not in sys.modules:
        # 创建一个轻量占位模块，把本文件里的类挂上去
        m = types.ModuleType('pixel_classifier')
        m.BaseAnomalyDetector = BaseAnomalyDetector
        m.GMMAnomalyDetector = GMMAnomalyDetector
        m.OneClassSVMAnomalyDetector = OneClassSVMAnomalyDetector
        sys.modules['pixel_classifier'] = m
    else:
        # 如果用户已经 import 了真正的 pixel_classifier.py，那也 OK
        m = sys.modules['pixel_classifier']
        if not hasattr(m, 'GMMAnomalyDetector'):
            m.BaseAnomalyDetector = BaseAnomalyDetector
            m.GMMAnomalyDetector = GMMAnomalyDetector
            m.OneClassSVMAnomalyDetector = OneClassSVMAnomalyDetector


# 在导入时就注册一次，保证 load_model() 调用前已经就绪
_install_class_aliases()


# ============================================================
# 特征提取（必须与训练代码完全一致，否则结果会失真）
# ============================================================
def extract_laws_features(image_rgb):
    """Laws 纹理能量特征 (H,W,5) float32。与训练时 BaseAnomalyDetector 完全一致。"""
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    kernels = _laws_kernels()
    channels = []
    for kernel in kernels:
        filtered = cv2.filter2D(gray, cv2.CV_32F, kernel)
        energy = np.abs(filtered)
        smoothed = cv2.GaussianBlur(energy, (0, 0), sigmaX=5)
        channels.append(smoothed)
    return np.dstack(channels)


def _laws_kernels():
    L5 = np.array([1, 4, 6, 4, 1])
    E5 = np.array([-1, -2, 0, 2, 1])
    S5 = np.array([-1, 0, 2, 0, -1])
    return [
        np.outer(E5, L5),
        np.outer(L5, E5),
        np.outer(E5, S5),
        np.outer(S5, E5),
        np.outer(E5, E5),
    ]


def postprocess_mask(mask, min_area=30):
    """形态学开闭运算 + 连通域面积过滤。与训练代码一致。"""
    mask_u8 = mask.astype(np.uint8) * 255
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    opened = cv2.morphologyEx(mask_u8, cv2.MORPH_OPEN, kernel_open)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
    result = np.zeros_like(mask_u8, dtype=np.uint8)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= min_area:
            result[labels == i] = 255
    return result > 0


def extract_supervised_features(image_rgb, feature_config, sigmas=(1, 2, 4)):
    """
    监督模式的特征提取。与训练时 PixelClassifierApp._extract_features_for_image 完全一致。

    feature_config: dict, 形如 {"intensity": True, "gaussian": True, "edges": True, "texture": False}
    """
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    features_list = []
    if feature_config.get("intensity", True):
        features_list.append(gray)
    for sigma in sigmas:
        blurred = cv2.GaussianBlur(gray, (0, 0), sigmaX=sigma)
        if feature_config.get("gaussian", True):
            features_list.append(blurred)
        if feature_config.get("edges", True):
            sobel_x = cv2.Sobel(blurred, cv2.CV_32F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(blurred, cv2.CV_32F, 0, 1, ksize=3)
            edges = np.hypot(sobel_x, sobel_y)
            features_list.append(edges)
        if feature_config.get("texture", False):
            laplace = cv2.Laplacian(blurred, cv2.CV_32F, ksize=3)
            features_list.append(np.abs(laplace))
    return np.stack(features_list, axis=-1).astype(np.float32)


# ============================================================
# 推理主流程
# ============================================================
def load_model(model_path):
    """加载 .pkl 模型，返回 (model, meta_dict)。"""
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"模型文件不存在: {model_path}")
    data = joblib.load(model_path)
    # 兼容：纯字典导出
    if not isinstance(data, dict) or 'model' not in data:
        raise ValueError(
            "模型文件格式不正确。本脚本只支持由 pixel_classifier.py "
            "中「💾 导出模型 (纯模型)」按钮导出的 .pkl 文件。"
        )
    model = data['model']
    meta = {
        'mode': data.get('mode', 'supervised'),
        'anomaly_algo': data.get('anomaly_algo'),
        'feature_config': data.get('feature_config'),
        'sigmas': data.get('sigmas', (1, 2, 4)),
        'feature_dim': data.get('feature_dim'),
        'app_version': data.get('app_version', 'unknown'),
    }
    return model, meta


def preprocess_image(image_path, max_size=1000):
    """
    读图 → RGB → 缩放到 max_size 以内（与训练时的 thumbnail 一致）。
    返回 (pil_rgb, np_rgb_uint8)
    """
    pil_img = Image.open(image_path).convert("RGB")
    pil_img.thumbnail((max_size, max_size), Image.LANCZOS)
    arr = np.array(pil_img)
    return pil_img, arr


def infer_one(model, meta, image_path, alpha=150, overlay=True, heatmap=False):
    """
    对一张图推理。

    返回 dict:
        mask:        np.bool (H,W)  True=缺陷
        overlay_img: PIL RGB 或 None
        heatmap:     np.float (H,W) 异常分数 或 None
        meta_info:   dict 一些信息
    """
    pil_rgb, rgb_u8 = preprocess_image(image_path)
    h, w = rgb_u8.shape[:2]
    mode = meta['mode']

    info = {'mode': mode, 'width': w, 'height': h}

    if mode == 'supervised':
        if meta['feature_config'] is None:
            raise ValueError("监督模式模型缺少 feature_config 元信息，无法对齐特征。请用新版程序重新导出。")
        feats = extract_supervised_features(rgb_u8, meta['feature_config'], tuple(meta['sigmas']))
        d = feats.shape[-1]
        if meta.get('feature_dim') and d != meta['feature_dim']:
            print(f"[警告] 特征维度不匹配: 模型期望 {meta['feature_dim']}，当前 {d}。"
                  f"请确认 feature_config 与训练时一致。", file=sys.stderr)
        X_all = feats.reshape(-1, d)
        pred = model.predict(X_all).reshape(h, w)
        # 约定：0=正常/背景，1=缺陷/前景
        mask = (pred == 1)
        info['classes'] = {
            0: '正常/背景',
            1: '缺陷/前景',
        }
        overlay_arr = None
        if overlay:
            ov = np.zeros((h, w, 4), dtype=np.uint8)
            ov[pred == 0] = [255, 0, 0, alpha]
            ov[pred == 1] = [0, 255, 0, alpha]
            combined = Image.alpha_composite(pil_rgb.convert("RGBA"), Image.fromarray(ov))
            overlay_arr = combined.convert("RGB")
        return {
            'mask': mask,
            'overlay_img': overlay_arr,
            'heatmap': None,
            'meta_info': info,
        }

    elif mode == 'anomaly':
        laws_feat = extract_laws_features(rgb_u8)
        X_all = laws_feat.reshape(-1, 5)
        anomaly_score, is_anomaly = model.predict(X_all)
        is_anomaly = is_anomaly.reshape(h, w)
        # 后处理：与训练时一致
        mask = postprocess_mask(is_anomaly, min_area=30)
        info['anomaly_algo'] = meta.get('anomaly_algo', '?')
        info['defect_pixels'] = int(mask.sum())
        info['defect_ratio'] = float(mask.mean())

        overlay_arr = None
        if overlay:
            ov = np.zeros((h, w, 4), dtype=np.uint8)
            ov[mask] = [255, 0, 0, alpha]
            combined = Image.alpha_composite(pil_rgb.convert("RGBA"), Image.fromarray(ov))
            overlay_arr = combined.convert("RGB")

        heat = None
        if heatmap:
            # 异常分数归一化到 0-255
            score_2d = anomaly_score.reshape(h, w)
            smin, smax = float(score_2d.min()), float(score_2d.max())
            if smax > smin:
                heat = ((score_2d - smin) / (smax - smin) * 255).astype(np.uint8)
            else:
                heat = np.zeros((h, w), dtype=np.uint8)

        return {
            'mask': mask,
            'overlay_img': overlay_arr,
            'heatmap': heat,
            'meta_info': info,
        }
    else:
        raise ValueError(f"未知 mode: {mode}")


# ============================================================
# 可视化辅助
# ============================================================
def mask_to_png(mask):
    """bool mask → 灰度 PNG (白=缺陷)"""
    arr = np.where(mask, 255, 0).astype(np.uint8)
    return Image.fromarray(arr)  # uint8 2D 数组自动识别为 'L' 模式


def heatmap_to_png(heat):
    """0-255 单通道 → JET 伪彩色 PNG"""
    color = cv2.applyColorMap(heat, cv2.COLORMAP_JET)
    # cv2 默认 BGR → RGB
    color_rgb = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
    return Image.fromarray(color_rgb)


def draw_defect_contours(pil_rgb, mask):
    """在叠加图上额外勾画缺陷轮廓，便于直观查看。"""
    arr = np.array(pil_rgb)
    mask_u8 = (mask.astype(np.uint8)) * 255
    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(arr, contours, -1, (0, 255, 255), 2)
    return Image.fromarray(arr)


# ============================================================
# CLI
# ============================================================
def collect_image_paths(args):
    paths = []
    if args.image:
        if os.path.isfile(args.image):
            paths.append(args.image)
        else:
            print(f"[警告] 文件不存在: {args.image}", file=sys.stderr)
    if args.image_dir:
        if os.path.isdir(args.image_dir):
            exts = ('*.png', '*.jpg', '*.jpeg', '*.tif', '*.tiff', '*.bmp')
            for ext in exts:
                paths.extend(glob.glob(os.path.join(args.image_dir, ext)))
                paths.extend(glob.glob(os.path.join(args.image_dir, '**', ext), recursive=True))
        else:
            print(f"[警告] 目录不存在: {args.image_dir}", file=sys.stderr)
    # 去重保序
    seen = set()
    uniq = []
    for p in paths:
        rp = os.path.abspath(p)
        if rp not in seen:
            seen.add(rp)
            uniq.append(p)
    return uniq


def main():
    parser = argparse.ArgumentParser(
        description="加载 pixel_classifier.py 导出的 .pkl 模型，对图像做缺陷检测。"
    )
    parser.add_argument('--model', '-m', required=True, help='模型 .pkl 文件路径')
    parser.add_argument('--image', '-i', help='单张待测图片路径')
    parser.add_argument('--image_dir', '-d', help='待测图片所在目录（递归）')
    parser.add_argument('--output', '-o', default='./infer_out', help='输出目录，默认 ./infer_out')
    parser.add_argument('--alpha', type=int, default=150,
                        help='叠加图透明度 0-255，默认 150')
    parser.add_argument('--no_overlay', action='store_true', help='不输出叠加图')
    parser.add_argument('--heatmap', action='store_true',
                        help='额外输出异常分数热力图（仅 anomaly 模式有效）')
    parser.add_argument('--contour', action='store_true',
                        help='在叠加图上额外勾画缺陷黄色轮廓')
    parser.add_argument('--max_size', type=int, default=1000,
                        help='图像长边缩放上限，与训练保持一致，默认 1000')
    args = parser.parse_args()

    if not args.image and not args.image_dir:
        parser.error("请至少指定 --image 或 --image_dir 之一")

    os.makedirs(args.output, exist_ok=True)

    print(f"[1/3] 加载模型: {args.model}")
    model, meta = load_model(args.model)
    print(f"      模式: {meta['mode']}"
          + (f"  算法: {meta['anomaly_algo']}" if meta['mode'] == 'anomaly' else "")
          + (f"  特征维度: {meta['feature_dim']}" if meta['feature_dim'] else ""))
    print(f"      app_version: {meta['app_version']}")

    paths = collect_image_paths(args)
    if not paths:
        print("[错误] 没有找到任何待测图片。", file=sys.stderr)
        sys.exit(2)
    print(f"[2/3] 待测图片数: {len(paths)}")

    summary = []
    for idx, p in enumerate(paths, 1):
        try:
            # 临时修改 max_size
            global_preprocess_max = preprocess_image.__defaults__
            # 简单处理：直接调用，使用默认 max_size
            result = infer_one(
                model, meta, p,
                alpha=args.alpha,
                overlay=not args.no_overlay,
                heatmap=args.heatmap,
            )
        except Exception as e:
            print(f"  [{idx}/{len(paths)}] {p}  失败: {e}", file=sys.stderr)
            summary.append((p, 'FAIL', str(e)))
            continue

        base = os.path.splitext(os.path.basename(p))[0]
        mask_path = os.path.join(args.output, f"{base}__mask.png")
        mask_to_png(result['mask']).save(mask_path)

        overlay_path = None
        if result['overlay_img'] is not None:
            overlay_img = result['overlay_img']
            if args.contour:
                overlay_img = draw_defect_contours(overlay_img, result['mask'])
            overlay_path = os.path.join(args.output, f"{base}__overlay.png")
            overlay_img.save(overlay_path)

        heat_path = None
        if result['heatmap'] is not None:
            heat_path = os.path.join(args.output, f"{base}__heatmap.png")
            heatmap_to_png(result['heatmap']).save(heat_path)

        info = result['meta_info']
        ratio = info.get('defect_ratio', float(result['mask'].mean()))
        n_def = info.get('defect_pixels', int(result['mask'].sum()))
        status = 'OK' if ratio < 1e-4 else 'DEFECT'
        print(f"  [{idx}/{len(paths)}] {os.path.basename(p):30s}  "
              f"{info['width']}x{info['height']}  "
              f"defect={n_def}px ({ratio*100:.3f}%)  → {status}")
        summary.append((p, status, f"defect_ratio={ratio:.5f}"))

    # 写一个汇总 CSV
    csv_path = os.path.join(args.output, 'infer_summary.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("path,status,info\n")
        for p, s, info in summary:
            f.write(f"{p},{s},{info}\n")
    print(f"[3/3] 完成。结果保存到: {args.output}")
    print(f"      汇总 CSV: {csv_path}")


if __name__ == '__main__':
    main()
