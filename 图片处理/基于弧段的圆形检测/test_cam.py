from __future__ import print_function

import numpy as np
import cv2 as cv
import random as rng
import sys

def main():
    # 打开摄像头或视频文件
    try:
        fn = sys.argv[1]
        cap = cv.VideoCapture(fn)  # 视频文件
        print(f"正在处理视频文件: {fn}")
    except IndexError:
        cap = cv.VideoCapture(0)  # 默认摄像头
        print("正在使用摄像头")

    # 检查是否成功打开
    if not cap.isOpened():
        print('无法打开摄像头或视频文件')
        return

    # 创建EdgeDrawing对象
    ed = cv.ximgproc.createEdgeDrawing()

    EDParams = cv.ximgproc_EdgeDrawing_Params()
    # 这些参数影响所有边缘检测
    EDParams.MinPathLength = 60     # 所有弧段都必须满足 MinPathLength 要求，如果有任何一个弧段长度 < MinPathLength，该弧段会被丢弃
    EDParams.PFmode = True           # 设置为True可能提高检测精度但会降低速度    
    EDParams.NFAValidation = True    # 设置为False可能检测到更多特征但可能有更多误检

    # 注意：MinLineLength 参数已移除，因为我们不需要直线检测
    
    ed.setParams(EDParams)

    print("按 'q' 键退出，按 'p' 键暂停")

    paused = False

    while True:
        if not paused:
            # 读取视频帧
            ret, src = cap.read()
            if not ret:
                print("无法读取视频帧或视频结束")
                break

            # 转换为灰度图
            gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

            # 创建用于显示结果的图像副本
            ssrc = src.copy() * 0  # 边缘段显示
            esrc = src.copy()      # 椭圆显示

            # 检测边缘（必须在detectEllipses()之前调用）
            ed.detectEdges(gray)

            # 获取检测结果
            segments = ed.getSegments()     # 边缘段
            ellipses = ed.detectEllipses()  # 椭圆

            # 绘制检测到的边缘段
            for i in range(len(segments)):
                color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
                cv.polylines(ssrc, [segments[i]], False, color, 1, cv.LINE_8)

            # 绘制检测到的圆和椭圆，并打印信息
            circle_count = 0
            ellipse_count = 0
            
            if ellipses is not None:  # 检查是否找到圆和椭圆
                for i in range(len(ellipses)):
                    center = (int(ellipses[i][0][0]), int(ellipses[i][0][1]))
                    major_axis = int(ellipses[i][0][2]) + int(ellipses[i][0][3])
                    minor_axis = int(ellipses[i][0][2]) + int(ellipses[i][0][4])
                    axes = (major_axis, minor_axis)
                    angle = ellipses[i][0][5]
                    
                    # 判断是否为圆：长轴和短轴相等（允许1像素的误差）
                    if abs(major_axis - minor_axis) <= 1:
                        color = (0, 255, 0)  # 绿色表示圆
                        circle_count += 1
                        # 在图像上添加文字标签
                        cv.putText(esrc, f'Circle {circle_count}', 
                                  (center[0] + 10, center[1] - 10), 
                                  cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                    else:
                        color = (0, 0, 255)  # 红色表示椭圆
                        ellipse_count += 1
                        # 在图像上添加文字标签
                        cv.putText(esrc, f'Ellipse {ellipse_count}', 
                                  (center[0] + 10, center[1] - 10), 
                                  cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                    
                    cv.ellipse(esrc, center, axes, angle, 0, 360, color, 2, cv.LINE_AA)

            # 在图像上显示计数信息
            info_text = f'Circles: {circle_count}, Ellipses: {ellipse_count}'
            cv.putText(esrc, info_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # 显示结果
            cv.imshow("Source Video", src)
            cv.imshow("Detected Edge Segments", ssrc)
            cv.imshow("Detected Circles and Ellipses", esrc)

        # 键盘控制
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):  # 退出
            break
        elif key == ord('p'):  # 暂停/继续
            paused = not paused
            if paused:
                print("视频暂停，按 'p' 继续")
            else:
                print("视频继续播放")

    # 释放资源
    cap.release()
    cv.destroyAllWindows()
    print('Done')

if __name__ == '__main__':
    print(__doc__)
    main()
