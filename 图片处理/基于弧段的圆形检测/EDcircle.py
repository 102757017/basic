from __future__ import print_function

import numpy as np
import cv2 as cv
import random as rng
import sys



def main():
    try:
        fn = sys.argv[1]
    except IndexError:
        fn = 'p2.jpg'

    # 读取图像
    src = cv.imread(cv.samples.findFile(fn))
    if src is None:
        print(f'无法读取图像: {fn}')
        return
    
    # 转换为灰度图
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    cv.imshow("source", src)

    # 创建用于显示结果的图像副本
    ssrc = src.copy() * 0  # 边缘段显示
    lsrc = src.copy()      # 直线显示
    esrc = src.copy()      # 椭圆显示

    # 创建EdgeDrawing对象
    ed = cv.ximgproc.createEdgeDrawing()

    
    EDParams = cv.ximgproc_EdgeDrawing_Params()
    # 这些参数影响所有边缘检测
    EDParams.MinPathLength = 60     # 所有弧段都必须满足 MinPathLength 要求，如果有任何一个弧段长度 < MinPathLength，该弧段会被丢弃
    EDParams.PFmode = True           # 设置为True可能提高检测精度但会降低速度    
    EDParams.NFAValidation = True    # 设置为False可能检测到更多特征但可能有更多误检


    # 这个参数只影响直线检测,不影响圆形检测！
    EDParams.MinLineLength = 100      # 最小直线长度，尝试在5到100之间调整，值越大，检测到的直线越少但越长

    
    ed.setParams(EDParams)

    # 检测边缘（必须在detectLines()和detectEllipses()之前调用）
    ed.detectEdges(gray)

    # 获取检测结果
    segments = ed.getSegments()     # 边缘段
    lines = ed.detectLines()        # 直线
    ellipses = ed.detectEllipses()  # 椭圆

    # 绘制检测到的边缘段
    for i in range(len(segments)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.polylines(ssrc, [segments[i]], False, color, 1, cv.LINE_8)

    cv.imshow("detected edge segments", ssrc)

    # 绘制检测到的直线
    if lines is not None:  # 检查是否找到直线
        lines = np.uint16(np.around(lines))
        for i in range(len(lines)):
            cv.line(lsrc, 
                   (lines[i][0][0], lines[i][0][1]), 
                   (lines[i][0][2], lines[i][0][3]), 
                   (0, 0, 255), 1, cv.LINE_AA)

    cv.imshow("detected lines", lsrc)

    # 绘制检测到的圆和椭圆，并打印信息
    if ellipses is not None:  # 检查是否找到圆和椭圆
        print("=" * 50)
        print("检测到的圆和椭圆信息:")
        print("=" * 50)
        
        circle_count = 0
        ellipse_count = 0
        
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
                # 计算圆的半径（长轴的一半）
                radius = major_axis // 2
                print(f"圆 {circle_count}: 圆心({center[0]}, {center[1]}), 半径={radius}")
            else:
                color = (0, 0, 255)  # 红色表示椭圆
                ellipse_count += 1
                print(f"椭圆 {ellipse_count}: 圆心({center[0]}, {center[1]}), 长轴={major_axis}, 短轴={minor_axis}, 角度={angle:.2f}°")
            
            cv.ellipse(esrc, center, axes, angle, 0, 360, color, 2, cv.LINE_AA)
        
        print("=" * 50)
        print(f"总计: {circle_count} 个圆, {ellipse_count} 个椭圆")
        print("=" * 50)

    cv.imshow("detected circles and ellipses", esrc)
    cv.waitKey(0)
    print('Done')

if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
