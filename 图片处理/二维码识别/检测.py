import cv2
import os

def detect_qrcode(image_path):
    # 检查模型文件是否存在
    model_files = ["detect.prototxt", "detect.caffemodel", "sr.prototxt", "sr.caffemodel"]
    for file in model_files:
        if not os.path.exists(file):
            print(f"错误：模型文件 {file} 不存在。请确保模型文件与脚本在同一目录下，或提供完整路径。")
            # 尝试从常见路径查找，例如在py文件同级目录的model文件夹下
            # if not os.path.exists(os.path.join(os.path.dirname(__file__), "model", file)):
            #     print(f"错误：模型文件 {file} 也不在 {os.path.join(os.path.dirname(__file__), 'model')} 目录下。")
            return []

    # 初始化 WeChat QRCode 检测器
    try:
        detector = cv2.wechat_qrcode_WeChatQRCode(
            "detect.prototxt",
            "detect.caffemodel",
            "sr.prototxt",
            "sr.caffemodel"
        )
    except Exception as e:
        print(f"初始化 WeChatQRCode 失败: {e}")
        print("请检查OpenCV版本是否支持WeChatQRCode模块，以及模型文件是否完整且正确。")
        return []

    # 读取图像
    # 添加一个检查，确保图像文件路径是正确的，并且文件可访问
    if not os.path.exists(image_path):
        print(f"错误：图片文件 {image_path} 不存在。")
        return []

    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}。请确保图片路径正确且图片未损坏。")
        return []

    # 进行亮度与对比度增强
    # 提高图像对比度和亮度可能有助于检测，但这对于解码问题可能无用
    img_enhanced = cv2.convertScaleAbs(img, alpha=1.2, beta=40)

    # 检测并解码二维码
    try:
        results, points = detector.detectAndDecode(img_enhanced)

        # OpenCV的wechat_qrcode模块返回的results已经是字符串，
        # 如果内部解码失败，会直接抛出上面看到的错误，不会返回一个需要我们再次解码的byte对象。
        # 因此，以下尝试不同编码的逻辑，实际上只有在wechat_qrcode_WeChatQRCode
        # 内部某种机制侥幸返回了一个"错误字符串"而不是抛出错误时才可能有用。
        # 在遇到'utf-8' codec can't decode byte 0x81时，此代码块不会被执行。

        # 但是，如果未来OpenCV版本改变了行为，或者某些情况下返回了非标准UTF-8的字符串，
        # 这个逻辑依然有其价值。这里我们假设其返回的是标准Python字符串。
        final_decoded_results = []
        for res_str in results:
            if res_str:
                # 假设OpenCV返回的是已经尝试过UTF-8解码的字符串
                # 如果内部解码失败，它会在 detectAndDecode 处抛出异常，不会到这里。
                # 如果它侥幸返回了一个乱码字符串，我们可以尝试重新编码再解码。
                # 但是直接对Python字符串进行decode('gbk')是不行的。
                # 正确的做法是：假设 res_str 是一个可能的乱码字符串，
                # 并且它原本是GBK编码的，误被按某种编码解码成了这个乱码字符串。
                # 这种情况下，我们需要先将其"逆解码"回字节，再用正确的编码解码。
                # 常见的方法是假设它被错误的latin-1或iso-8859-1解码了。

                try:
                    # 检查是否包含乱码特征，例如常见的问号或替代字符
                    # 这个判断可能不准确，根据实际乱码情况调整
                    if '�' in res_str or any(ord(c) > 127 and c.isprintable() is False for c in res_str):
                        # 尝试从字符串恢复字节，再用GBK解码
                        decoded_res = res_str.encode('latin-1').decode('gbk')
                        final_decoded_results.append(decoded_res)
                    else:
                        final_decoded_results.append(res_str) # 认为是正常字符串
                except Exception:
                    # 如果转换失败，就保留原始字符串，或者标记为二进制数据
                    final_decoded_results.append(f"[原始内容 (可能乱码): {res_str}]")
            else:
                final_decoded_results.append("[空内容]")
        
        return final_decoded_results
    except Exception as e:
        print(f"二维码检测失败: {e}")
        print("这通常意味着QR码内容编码不兼容（如GBK），而WeChatQRCode默认尝试UTF-8解码。")
        print("建议尝试换用pyzbar等支持更多编码的库。")
        return []

# 使用示例
if __name__ == "__main__":
    image_file = "2.gif" # 确保此图片文件存在且可访问
    result = detect_qrcode(image_file)
    if result:
        print("检测到的二维码内容：")
        for i, content in enumerate(result):
            print(f"{i+1}. {content}")
    else:
        print("未检测到二维码或检测失败。")

