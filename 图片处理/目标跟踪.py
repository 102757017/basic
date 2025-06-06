import cv2
import numpy as np
from collections import deque

# --- 全局变量和参数 ---
# 轨迹绘制参数
trajectory_maxlen = 50  # 轨迹点的最大长度
trajectory_points = deque(maxlen=trajectory_maxlen)

# 卡尔曼滤波器参数 (初始设置)
# 状态向量：[x, y, vx, vy, ax, ay] - 6个状态 (位置、速度、加速度)
# 测量向量：[x, y] - 2个测量 (观测到的质心位置)
dim_state = 6
dim_measurement = 2
# dt 将在 main 函数中根据视频帧率动态设置

# 注意：kalman 对象的创建和其参数的设置现在放到了 main 函数内部
# 这样可以确保每次重新运行 main 函数（例如在选择新ROI后）时，
# 卡尔曼滤波器都被正确地初始化，尤其是 dt 的设置。

# 物体中心点、速度和加速度 (从卡尔曼滤波器获得)
estimated_x, estimated_y = 0, 0
estimated_vx, estimated_vy = 0, 0
estimated_ax, estimated_ay = 0, 0

# --- 主程序 ---
def main():
    global estimated_x, estimated_y, estimated_vx, estimated_vy, estimated_ax, estimated_ay
    
    # 初始化视频捕获
    # cap = cv2.VideoCapture(0)  # 使用摄像头
    video_path = 'L-INN2.mp4' # 请替换为你的视频文件路径
    cap = cv2.VideoCapture(video_path) 

    if not cap.isOpened():
        print(f"错误: 无法打开视频流或文件: {video_path}")
        return

    # 获取视频帧率并计算 dt
    fps = cap.get(cv2.CAP_PROP_FPS)
    dt = 1.0 / fps if fps > 0 else 1.0 # 确保fps不为0，避免除以零

    print(f"视频帧率 (FPS): {fps:.2f}")
    print(f"时间步长 (dt): {dt:.4f} 秒")

    # 在main函数中创建卡尔曼滤波器实例
    kalman = cv2.KalmanFilter(dim_state, dim_measurement)

    # 状态转移矩阵 (A)
    kalman.transitionMatrix = np.array([[1, 0, dt, 0, 0.5*dt**2, 0],
                                         [0, 1, 0, dt, 0, 0.5*dt**2],
                                         [0, 0, 1, 0, dt, 0],
                                         [0, 0, 0, 1, 0, dt],
                                         [0, 0, 0, 0, 1, 0],
                                         [0, 0, 0, 0, 0, 1]], np.float32)

    # 测量矩阵 (H)
    kalman.measurementMatrix = np.array([[1, 0, 0, 0, 0, 0],
                                         [0, 1, 0, 0, 0, 0]], np.float32)

    # 过程噪声协方差 (Q) - 描述模型的不确定性
    # 较大的值表示模型不确定性高，更依赖于测量值
    process_noise_scale = 1e-2 # 初始值 1e-3, 1e-2 可能更适合
    kalman.processNoiseCov = np.array([[1, 0, 0, 0, 0, 0],
                                        [0, 1, 0, 0, 0, 0],
                                        [0, 0, 1, 0, 0, 0],
                                        [0, 0, 0, 1, 0, 0],
                                        [0, 0, 0, 0, 0.1, 0],  # 加速度噪声通常较小
                                        [0, 0, 0, 0, 0, 0.1]], np.float32) * process_noise_scale 

    # 测量噪声协方差 (R) - 描述测量值的不确定性 (越小越相信测量值)
    # 较大的值表示测量不确定性高，更依赖于模型预测值
    measurement_noise_scale = 5 # 初始值 1, 5 甚至 10 可能更适合，表示测量本身不确定性较高
    kalman.measurementNoiseCov = np.eye(dim_measurement, dtype=np.float32) * measurement_noise_scale 

    # 估计误差协方差 (P) - 初始不确定性
    kalman.errorCovPost = np.eye(dim_state, dtype=np.float32) * 1

    # 读取第一帧用于ROI选择
    ret, frame = cap.read()
    if not ret:
        print("错误: 无法读取第一帧。")
        cap.release()
        cv2.destroyAllWindows()
        return
    
    print("请在 'Video Frame' 窗口中选择要跟踪的物体区域。")
    print("用鼠标拖动以绘制一个矩形，然后按 'Enter' 键确认，或按 'c' 键取消。")
    
    initial_roi = cv2.selectROI("Video Frame", frame, showCrosshair=True, fromCenter=False)
    cv2.destroyWindow("Video Frame")

    if not (initial_roi[2] > 0 and initial_roi[3] > 0):
        print("ROI 选择已取消或无效。程序退出。")
        cap.release()
        cv2.destroyAllWindows()
        return

    # 创建并初始化 CSRT 跟踪器
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, initial_roi)

    # 初始化卡尔曼滤波器的初始状态 (基于第一次的ROI中心)
    x_init, y_init, w_init, h_init = initial_roi
    initial_centroid = np.array([float(x_init + w_init / 2), float(y_init + h_init / 2)], dtype=np.float32)
    
    # 设置卡尔曼滤波器的初始状态（位置是初始质心，速度和加速度设为0）
    kalman.statePost = np.array([[initial_centroid[0]],  # x
                                  [initial_centroid[1]],  # y
                                  [0.0],                  # vx
                                  [0.0],                  # vy
                                  [0.0],                  # ax
                                  [0.0]], np.float32)     # ay
    
    # 清空轨迹点
    trajectory_points.clear()

    # --- 视频处理主循环 ---
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 更新跟踪器
        success, bbox = tracker.update(frame)

        current_centroid = None
        if success:
            # 提取边界框坐标 (x, y, w, h)
            x, y, w, h = [int(v) for v in bbox]
            
            # 绘制边界框
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # 计算当前物体中心点
            current_centroid = np.array([float(x + w / 2), float(y + h / 2)], dtype=np.float32)
            
            # 卡尔曼滤波器预测 
            kalman.predict() 
            
            # 使用当前检测到的质心进行修正
            measurement = np.array([[current_centroid[0]], [current_centroid[1]]], dtype=np.float32)
            kalman.correct(measurement)
            
            # 从卡尔曼滤波器的后验状态中提取估计值
            estimated_state = kalman.statePost
            estimated_x, estimated_y = estimated_state[0, 0], estimated_state[1, 0]
            estimated_vx, estimated_vy = estimated_state[2, 0], estimated_state[3, 0]
            estimated_ax, estimated_ay = estimated_state[4, 0], estimated_state[5, 0]

            # 更新轨迹点 (使用卡尔曼滤波器估计的位置)
            current_estimated_centroid = (int(estimated_x), int(estimated_y))
            if len(trajectory_points) > 0:
                # 绘制连接前一个轨迹点的线
                cv2.line(frame, trajectory_points[-1], current_estimated_centroid, (0, 255, 0), 2)
            trajectory_points.append(current_estimated_centroid)

        else: # 跟踪失败
            cv2.putText(frame, "Tracking Failed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # 清空轨迹
            trajectory_points.clear()
            
            # 重置卡尔曼滤波器状态，表示不确定性高，且没有运动
            kalman.statePost = np.array([[0.0], [0.0], [0.0], [0.0], [0.0], [0.0]], np.float32)
            kalman.errorCovPost = np.eye(dim_state, dtype=np.float32) * 1000 # 极高不确定性
            
            # 提示用户重新选择ROI，调整Y坐标以适应新增的显示行
            cv2.putText(frame, "Press 'r' to re-select ROI", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # 清空显示值，避免显示旧的速度/加速度
            estimated_x, estimated_y = 0, 0
            estimated_vx, estimated_vy = 0, 0
            estimated_ax, estimated_ay = 0, 0


        # 定义速度和加速度的单位字符串
        speed_unit = 'px/s' if dt != 1.0 else 'px/f'
        accel_unit = 'px/s^2' if dt != 1.0 else 'px/f^2'

        # --- 显示卡尔曼滤波器估计的速度和加速度 ---
        # 显示总速度大小
        vel_magnitude = np.linalg.norm([estimated_vx, estimated_vy])
        cv2.putText(frame, f"Speed: {vel_magnitude:.2f} {speed_unit}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 显示X轴速度分量
        cv2.putText(frame, f"SpeedX: {estimated_vx:.2f} {speed_unit}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 显示Y轴速度分量
        cv2.putText(frame, f"SpeedY: {estimated_vy:.2f} {speed_unit}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 显示总加速度大小
        accel_magnitude = np.linalg.norm([estimated_ax, estimated_ay])
        cv2.putText(frame, f"Acceleration: {accel_magnitude:.2f} {accel_unit}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # 显示X轴加速度分量
        cv2.putText(frame, f"AccelerationX: {estimated_ax:.2f} {accel_unit}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # 显示Y轴加速度分量
        cv2.putText(frame, f"AccelerationY: {estimated_ay:.2f} {accel_unit}", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # 绘制整个轨迹
        for i in range(1, len(trajectory_points)):
            cv2.line(frame, trajectory_points[i-1], trajectory_points[i], (0, 255, 0), 2)


        cv2.imshow("Video Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'): # 用户按下'r'键重新选择ROI
            cap.release() # 释放旧的视频资源
            cv2.destroyAllWindows()
            main() # 重新运行main函数，开始新的选择过程
            return # 退出当前循环，避免重复处理

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
