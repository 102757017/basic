import cv2
import numpy as np
import os

# --- 配置和常量 ---
MATCHES_DIST_THRESHOLD = 25

# 注意：请确保这两张图片与你的 .py 文件在同一个目录下
IMAGE_PATH1 = "1.png"
IMAGE_PATH2 = "2.bmp"

# --- 主逻辑 ---
def main():
    # 1. 加载图片 (使用 imdecode 支持中文路径)
    img1_orig = cv2.imdecode(np.fromfile(IMAGE_PATH1, dtype=np.uint8), cv2.IMREAD_COLOR)
    img2_orig = cv2.imdecode(np.fromfile(IMAGE_PATH2, dtype=np.uint8), cv2.IMREAD_COLOR)

    if img1_orig is None or img2_orig is None:
        print(f"错误: 无法加载图片。请检查路径:\n{IMAGE_PATH1}\n{IMAGE_PATH2}")
        return

    img1 = img1_orig.copy()
    img2 = img2_orig.copy()

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 2. 创建 BinaryDescriptor 和 Matcher
    bd = cv2.line_descriptor.BinaryDescriptor_createBinaryDescriptor()
    bdm = cv2.line_descriptor.BinaryDescriptorMatcher()
    
    # =========================================================================
    # 方法一: 使用 BinaryDescriptor 进行检测和描述
    # =========================================================================
    print("--- 方法一: BinaryDescriptor 检测与匹配 ---")
    keylines1 = bd.detect(gray1)
    if keylines1 is None: keylines1 = []
    keylines2 = bd.detect(gray2)
    if keylines2 is None: keylines2 = []
    
    keylines1, descr1 = bd.compute(gray1, keylines1)
    keylines2, descr2 = bd.compute(gray2, keylines2)
    
    lbd_octave1, left_lbd_list = [], []
    lbd_octave2, right_lbd_list = [], []

    if descr1 is not None:
        for i, kl in enumerate(keylines1):
            if kl.octave == 0:
                lbd_octave1.append(kl)
                left_lbd_list.append(descr1[i])
    
    if descr2 is not None:
        for i, kl in enumerate(keylines2):
            if kl.octave == 0:
                lbd_octave2.append(kl)
                right_lbd_list.append(descr2[i])
    
    left_lbd = np.array(left_lbd_list, dtype=np.uint8)
    right_lbd = np.array(right_lbd_list, dtype=np.uint8)

    if left_lbd.shape[0] > 0 and right_lbd.shape[0] > 0:
        matches = bdm.match(left_lbd, right_lbd)
        good_matches = [m for m in matches if m.distance < MATCHES_DIST_THRESHOLD]
        print(f"BinaryDescriptor 初始匹配数: {len(matches)}, 筛选后优质匹配数: {len(good_matches)}")

        out_img_bd = draw_line_matches(img1, lbd_octave1, img2, lbd_octave2, good_matches)
        cv2.imshow("BinaryDescriptor Matches", out_img_bd)
        cv2.imwrite("matches_bd.jpg", out_img_bd)
    else:
        print("BinaryDescriptor未能找到足够的线段进行匹配。")


    # =========================================================================
    # 方法二: 使用 LSDDetector 检测, BinaryDescriptor 描述
    # =========================================================================
    print("\n--- 方法二: LSD 检测与匹配 ---")
    
    lsd = cv2.line_descriptor.LSDDetector_createLSDDetector()

    # --- 最终修正点在这里 ---
    # lsd.detect 的 Python 绑定版本是返回 keylines，而不是通过参数修改列表
    mask1 = np.ones_like(gray1)
    mask2 = np.ones_like(gray2)
    klsd1 = lsd.detect(gray1, 2, 2, mask1)
    klsd2 = lsd.detect(gray2, 2, 2, mask2)
    
    # 检测返回的可能是 None，需要处理
    if klsd1 is None: klsd1 = []
    if klsd2 is None: klsd2 = []
    
    if not klsd1 or not klsd2:
        print("LSD方法未能找到足够的线段进行匹配。")
    else:
        klsd1, lsd_descr1 = bd.compute(gray1, klsd1)
        klsd2, lsd_descr2 = bd.compute(gray2, klsd2)
        
        octave1_kl, left_lsd_descr_list = [], []
        octave1_kl_2, right_lsd_descr_list = [], []
        
        if lsd_descr1 is not None:
            for i, kl in enumerate(klsd1):
                if kl.octave == 1:
                    octave1_kl.append(kl)
                    left_lsd_descr_list.append(lsd_descr1[i])
            
        if lsd_descr2 is not None:
            for i, kl in enumerate(klsd2):
                if kl.octave == 1:
                    octave1_kl_2.append(kl)
                    right_lsd_descr_list.append(lsd_descr2[i])

        left_lsd_descr = np.array(left_lsd_descr_list, dtype=np.uint8)
        right_lsd_descr = np.array(right_lsd_descr_list, dtype=np.uint8)

        if left_lsd_descr.shape[0] > 0 and right_lsd_descr.shape[0] > 0:
            lsd_matches = bdm.match(left_lsd_descr, right_lsd_descr)
            good_lsd_matches = [m for m in lsd_matches if m.distance < MATCHES_DIST_THRESHOLD]
            print(f"LSD 初始匹配数: {len(lsd_matches)}, 筛选后优质匹配数: {len(good_lsd_matches)}")

            out_img_lsd = draw_line_matches(img1_orig.copy(), octave1_kl, img2_orig.copy(), octave1_kl_2, good_lsd_matches)
            cv2.imshow("LSD Matches", out_img_lsd)
            cv2.imwrite("matches_lsd.jpg", out_img_lsd)
        else:
            print("LSD方法在筛选octave后未能找到足够的描述符进行匹配。")

    print("\n按任意键关闭所有窗口...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_line_matches(img1, keylines1, img2, keylines2, good_matches, 
                      line_color=(0, 255, 0), pt_color=(0, 0, 255)):
    # 此函数保持不变
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    output_img = np.zeros((max(h1, h2), w1 + w2, 3), dtype=np.uint8)
    output_img[:h1, :w1, :] = img1
    output_img[:h2, w1:w1 + w2, :] = img2
    
    for match in good_matches:
        idx1 = match.queryIdx
        idx2 = match.trainIdx
        
        if idx1 >= len(keylines1) or idx2 >= len(keylines2):
            continue
            
        kl1 = keylines1[idx1]
        kl2 = keylines2[idx2]
        pt1_start = (int(kl1.startPointX), int(kl1.startPointY))
        pt1_end = (int(kl1.endPointX), int(kl1.endPointY))
        pt2_start = (int(kl2.startPointX + w1), int(kl2.startPointY))
        pt2_end = (int(kl2.endPointX + w1), int(kl2.endPointY))
        
        color = tuple(np.random.randint(0, 255, 3).tolist())
        
        cv2.line(output_img, pt1_start, pt1_end, line_color, 2)
        cv2.line(output_img, pt2_start, pt2_end, line_color, 2)
        
        mid_pt1 = (int((pt1_start[0] + pt1_end[0]) / 2), int((pt1_start[1] + pt1_end[1]) / 2))
        mid_pt2 = (int((pt2_start[0] + pt2_end[0]) / 2), int((pt2_start[1] + pt2_end[1]) / 2))
        cv2.line(output_img, mid_pt1, mid_pt2, color, 1)

        cv2.circle(output_img, mid_pt1, 3, pt_color, -1)
        cv2.circle(output_img, mid_pt2, 3, pt_color, -1)

    return output_img

if __name__ == "__main__":
    main()
