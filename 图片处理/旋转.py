# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np

os.chdir(os.path.dirname(__file__))
def rotate(binary):
        # 第一个参数旋转中心，第二个参数旋转角度，第三个参数：缩放比例
        M = cv2.getRotationMatrix2D((120, 55), 45, 1)
        # 第三个参数：变换后的图像大小,以左上角为起点进行裁剪
        res = cv2.warpAffine(img, M, (240, 110))
        cv2.imshow("img2", res)
        cv2.waitKey(0)


if __name__=="__main__":
    img = cv2.imdecode(np.fromfile('binary2.png', dtype=np.uint8), 1)
    rotate(img)
