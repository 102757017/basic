import cv2
import win32print
import win32ui
import win32con
from PIL import Image, ImageWin # 确保 ImageWin 被导入
import os

# ... generate_high_res_charuco 函数与上一个版本相同，保持尺寸调整后的参数 ...
def generate_high_res_charuco():
    # ChArUco参数
    squares_x = 5          # X方向方格数量（列数）
    squares_y = 7          # Y方向方格数量（行数）
    square_length = 0.035  # 每个方格的实际长度（单位：米，3.5cm）
    marker_length = 0.0175 # ArUco标记的实际长度（单位：米，1.75cm）
    margin_cm = 0.5        # 图像边距（单位：厘米，0.5cm）
    
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250) #每个小方块里面的黑白图案是6x6比特的二进制网格
    board = cv2.aruco.CharucoBoard((squares_x, squares_y), square_length, marker_length, dictionary)
    
    target_dpi = 600       #打印dpi
    physical_width_cm = squares_x * square_length * 100
    physical_height_cm = squares_y * square_length * 100
    total_physical_width_cm = physical_width_cm + 2 * margin_cm
    total_physical_height_cm = physical_height_cm + 2 * margin_cm
    image_total_width_px = int(total_physical_width_cm / 2.54 * target_dpi)
    image_total_height_px = int(total_physical_height_cm / 2.54 * target_dpi)
    margin_px = int(margin_cm / 2.54 * target_dpi)
    
    board_image = board.generateImage(
        outSize=(image_total_width_px, image_total_height_px),
        marginSize=margin_px,
        borderBits=1 
    )
    
    output_filename = f"charuco_dpi{target_dpi}.png"
    cv2.imwrite(output_filename, board_image)
    print(f"生成高分辨率ChArUco板PNG: {output_filename}")
    print(f"图像像素尺寸: {image_total_width_px}x{image_total_height_px} 像素")
    print(f"板子内部物理尺寸: {physical_width_cm:.2f} x {physical_height_cm:.2f} cm")
    print(f"总物理尺寸 (含边距): {total_physical_width_cm:.2f} x {total_physical_height_cm:.2f} cm")
    print(f"目标打印DPI: {target_dpi}")
    
    return output_filename, target_dpi


def print_image_raw(image_path, target_dpi):
    hDC = None # 初始化
    try:
        # 1. 获取打印机和设备上下文
        printer_name = win32print.GetDefaultPrinter()
        print(f"\n尝试打印到默认打印机: {printer_name}")
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)

        # 2. 获取打印机信息
        printable_width_px = hDC.GetDeviceCaps(win32con.HORZRES)
        printable_height_px = hDC.GetDeviceCaps(win32con.VERTRES)
        print(f"打印机分辨率: {hDC.GetDeviceCaps(win32con.LOGPIXELSX)}x{hDC.GetDeviceCaps(win32con.LOGPIXELSY)} DPI")
        print(f"打印机可打印区域: {printable_width_px}x{printable_height_px} 像素")

        # 3. 加载图像
        pil_img = Image.open(image_path)
        img_width, img_height = pil_img.size
        print(f"加载图像尺寸: {img_width}x{img_height} 像素")

        if img_width > printable_width_px or img_height > printable_height_px:
            print(f"错误: 图像尺寸大于可打印区域。")
            return

        # 4. 开始打印作业
        hDC.StartDoc(os.path.basename(image_path))
        hDC.StartPage()

        # 使用 ImageWin.Dib.draw() 这种方法直接将DIB数据流式传输到设备，避免创建巨大的GDI位图对象

        # 将PIL图像转换为DIB对象
        dib = ImageWin.Dib(pil_img)

        # 计算居中位置
        start_x = (printable_width_px - img_width) // 2
        start_y = (printable_height_px - img_height) // 2
        start_x = max(0, start_x)
        start_y = max(0, start_y)

        # 定义目标矩形区域 (left, top, right, bottom)
        dest_rect = (start_x, start_y, start_x + img_width, start_y + img_height)

        # 直接将DIB绘制到打印机DC
        # dib.draw() 需要一个设备上下文的句柄 (HDC)，而不是 pywin32 对象
        # hDC.GetHandleOutput() 提供了这个句柄
        dib.draw(hDC.GetHandleOutput(), dest_rect)
        
        # ============================================

        hDC.EndPage()
        hDC.EndDoc()
        print("打印作业发送成功！请检查打印机。")

    except Exception as e:
        print(f"打印时发生错误: {e}")
    finally:
        # 只需要释放打印机DC即可
        if hDC:
            hDC.DeleteDC()


# ====================================================================
# 主程序
# ====================================================================
if __name__ == "__main__":
    output_png_path, board_target_dpi = generate_high_res_charuco()
    if os.path.exists(output_png_path):
        #print_image_raw(output_png_path, board_target_dpi)
        pass
    else:
        print("PNG文件未生成，无法打印。")

