import cv2
import os
import shutil
import tempfile
import numpy as np
from PIL import Image

# 模型文件与脚本同级
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILES = ["detect.prototxt", "detect.caffemodel", "sr.prototxt", "sr.caffemodel"]


def build_detector():
    """加载 WeChatQRCode 模型。
    OpenCV 的 C++ 层用窄字符路径打开文件，当目录名含中文时（如"图片处理\二维码识别"）
    会静默失败并报 "returned a result with an exception set"。这里把模型复制到纯 ASCII
    临时目录再加载，绕开编码问题。"""
    model_paths = [os.path.join(BASE_DIR, f) for f in MODEL_FILES]
    missing = [p for p in model_paths if not os.path.exists(p)]
    if missing:
        for p in missing:
            print(f"错误：模型文件 {os.path.basename(p)} 不存在（查找路径：{p}）。")
        return None

    if all(ord(c) < 128 for c in BASE_DIR):
        paths = model_paths
        tmp_dir = None
    else:
        tmp_dir = tempfile.mkdtemp(prefix="qrcode_")
        paths = [os.path.join(tmp_dir, f) for f in MODEL_FILES]
        for src, dst in zip(model_paths, paths):
            shutil.copyfile(src, dst)

    try:
        return cv2.wechat_qrcode_WeChatQRCode(*paths)
    except Exception as e:
        print(f"初始化 WeChatQRCode 失败: {e}")
        print("请检查OpenCV版本是否支持WeChatQRCode模块，以及模型文件是否完整且正确。")
        return None
    finally:
        # 模型已读入内存，可安全删除副本
        if tmp_dir:
            shutil.rmtree(tmp_dir, ignore_errors=True)


def imread_any(image_path):
    """兼容 OpenCV 读不了的格式（GIF / WEBP / 中文路径）。
    先试 cv2.imread（带中文路径支持），失败再回退 Pillow。"""
    if not os.path.exists(image_path):
        print(f"错误：图片文件 {image_path} 不存在。")
        return None

    # cv2.imread 对含中文的路径在部分平台上会返回 None，用 fromfile 绕开编码问题
    try:
        img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            return img
    except Exception:
        pass

    # OpenCV 4.x 不支持 GIF，需用 Pillow 打开再转 BGR
    try:
        with Image.open(image_path) as pil_img:
            pil_img.seek(0)  # 动图只取第一帧
            if pil_img.mode != "RGB":
                pil_img = pil_img.convert("RGB")
            return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"读取图片失败: {image_path} ({e})")
        return None


def detect_qrcode(image_path):
    detector = build_detector()
    if detector is None:
        return []

    img = imread_any(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}。请确保图片路径正确且图片未损坏。")
        return []

    # 进行亮度与对比度增强
    # 提高图像对比度和亮度可能有助于检测，但这对于解码问题可能无用
    img_enhanced = cv2.convertScaleAbs(img, alpha=1.2, beta=40)

    # 检测并解码二维码
    try:
        results, points = detector.detectAndDecode(img_enhanced)
    except cv2.error as e:
        # cv2.error 表示解码阶段就失败了（编码不兼容等），此时 results 拿不到
        print(f"二维码检测失败: {e}")
        print("这通常意味着QR码内容编码不兼容（如GBK），而WeChatQRCode默认尝试UTF-8解码。")
        print("建议尝试换用pyzbar等支持更多编码的库。")
        return []

    # OpenCV 的 wechat_qrcode 返回的 results 已是 Python str；
    # 若内部按 latin-1 之类误解码，会看到乱码，此时逆解码回字节再用 GBK 还原。
    final_decoded_results = []
    for res_str in results:
        if not res_str:
            final_decoded_results.append("[空内容]")
            continue
        try:
            # 误解码的典型特征：包含 U+FFFD 替换字符，或存在非 GBK 可映射的孤立高位字符
            is_garbled = "�" in res_str
            if not is_garbled:
                for candidate in ("latin-1", "cp1252"):
                    try:
                        fixed = res_str.encode(candidate).decode("gbk")
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        continue
                    # 还原成功且结果可打印，认为原串是误解码
                    if fixed.isprintable() and fixed != res_str:
                        is_garbled = True
                        res_str = fixed
                    break
            final_decoded_results.append(res_str)
        except Exception:
            final_decoded_results.append(f"[原始内容 (可能乱码): {res_str}]")

    return final_decoded_results


# 使用示例
if __name__ == "__main__":
    image_file = os.path.join(BASE_DIR, "2.gif")  # 用绝对路径，GIF 需由 Pillow 读取
    result = detect_qrcode(image_file)
    if result:
        print("检测到的二维码内容：")
        for i, content in enumerate(result):
            print(f"{i+1}. {content}")
    else:
        print("未检测到二维码或检测失败。")
