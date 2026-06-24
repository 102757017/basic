import cv2
import numpy as np
import sys

image = None
gray = None
win_name = "Hough Circle Detection"

def nothing(x):
    pass

def main():
    global image, gray

    # 读取图像
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        img_path = "circle.jpg"
    image = cv2.imread(img_path)
    if image is None:
        print(f"错误：无法加载图像 '{img_path}'")
        sys.exit(1)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 可选：轻微高斯模糊，减少噪声
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)

    cv2.namedWindow(win_name)

    # 创建滑块（范围调整得更合理，dp 通常 1~2，此处放大以便观察效果）
    cv2.createTrackbar("dp", win_name, 1, 5, nothing)          # 1~5
    cv2.createTrackbar("minDist", win_name, 10, 200, nothing)  # 1~200
    cv2.createTrackbar("param1", win_name, 100, 300, nothing)  # 1~300
    cv2.createTrackbar("param2", win_name, 30, 200, nothing)   # 1~200
    cv2.createTrackbar("minRadius", win_name, 0, 100, nothing) # 0~100
    cv2.createTrackbar("maxRadius", win_name, 50, 150, nothing)# 0~150

    print("按 ESC 退出，拖动滑块实时调参。参数非法时会自动修正。")

    while True:
        # 获取当前滑块值
        dp = cv2.getTrackbarPos("dp", win_name)
        minDist = cv2.getTrackbarPos("minDist", win_name)
        param1 = cv2.getTrackbarPos("param1", win_name)
        param2 = cv2.getTrackbarPos("param2", win_name)
        minRadius = cv2.getTrackbarPos("minRadius", win_name)
        maxRadius = cv2.getTrackbarPos("maxRadius", win_name)

        # ------------------ 参数合法性保护 ------------------
        # 强制正数参数至少为 1
        if dp <= 0:
            dp = 1
            cv2.setTrackbarPos("dp", win_name, dp)
        if minDist <= 0:
            minDist = 1
            cv2.setTrackbarPos("minDist", win_name, minDist)
        if param1 <= 0:
            param1 = 1
            cv2.setTrackbarPos("param1", win_name, param1)
        if param2 <= 0:
            param2 = 1
            cv2.setTrackbarPos("param2", win_name, param2)

        # 确保 minRadius <= maxRadius
        if minRadius > maxRadius:
            minRadius, maxRadius = maxRadius, minRadius
            cv2.setTrackbarPos("minRadius", win_name, minRadius)
            cv2.setTrackbarPos("maxRadius", win_name, maxRadius)

        # 可选：限制 minDist 不能超过图像短边的一半（避免检测异常）
        # 此处仅作演示，可根据图像大小动态调整
        # if minDist > min(image.shape[:2]) // 2:
        #     minDist = min(image.shape[:2]) // 2
        #     cv2.setTrackbarPos("minDist", win_name, minDist)

        # 执行霍夫圆检测
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=dp,
            minDist=minDist,
            param1=param1,
            param2=param2,
            minRadius=minRadius,
            maxRadius=maxRadius
        )

        # 绘制结果
        result = image.copy()
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(result, (x, y), r, (0, 255, 0), 2)
                cv2.circle(result, (x, y), 2, (0, 0, 255), 3)
            cv2.putText(result, f"Circles: {len(circles)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        else:
            cv2.putText(result, "No circles detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow(win_name, result)

        if (cv2.waitKey(30) & 0xFF) == 27:  # ESC
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
