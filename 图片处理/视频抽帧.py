import cv2
import os

def video_to_frames(video_path, output_dir, interval=5):
    """
    改进版视频抽帧函数
    参数：
        video_path: 视频文件路径
        output_dir: 图片输出目录
        interval: 抽帧间隔（默认每5帧抽1帧）
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("错误：无法打开视频文件")
        return
    
    # 获取视频基础信息
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    print(f"视频信息：{video_name} | 总帧数：{total_frames} | 帧率：{fps:.2f} FPS")

    # 初始化计数器
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 视频读取结束
        
        # 按间隔抽帧
        if frame_count % interval == 0:
            # 调整分辨率（短边缩放到640）
            h, w = frame.shape[:2]
            min_dim = min(h, w)
            scale = 640 / min_dim
            new_size = (int(w * scale), int(h * scale))
            
            # 使用高质量插值算法
            resized_frame = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)
            
            # 生成文件名
            filename = f"{video_name}_{str(saved_count).zfill(5)}.jpg"
            output_path = os.path.join(output_dir, filename)
            
            # 保存图片（压缩质量为90）
            cv2.imwrite(output_path, resized_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            saved_count += 1
        
        frame_count += 1
        
        # 显示进度（每处理100帧显示一次）
        if frame_count % 100 == 0:
            print(f"处理进度：{frame_count}/{total_frames} 帧 | 已保存 {saved_count} 张")

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print(f"抽帧完成！共保存 {saved_count} 张图片到：{output_dir}")

if __name__ == "__main__":
    # 参数设置（注意使用原始字符串处理Windows路径）
    video_path = "L-INN3.mp4"
    output_dir = r"G:\mp4\L-INN3"  # 使用原始字符串避免转义问题
    
    # 执行抽帧（每5帧抽1帧）
    video_to_frames(video_path, output_dir, interval=5)
