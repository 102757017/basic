# -*- coding: UTF-8 -*-
import cv2
import os
import numpy as np



 
def motion_blur(image, degree=12, angle=45):
    image = np.array(image)
 
    # 这里生成任意角度的运动模糊kernel的矩阵， degree越大，模糊程度越高
    M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
    motion_blur_kernel = np.diag(np.ones(degree))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))
 
    motion_blur_kernel = motion_blur_kernel / degree
    blurred = cv2.filter2D(image, -1, motion_blur_kernel)
 
    # convert to uint8
    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred



img = cv2.imread('text.png')
#由于opencv不支持读取中文路径，用以下方法代替cv2.imread
img = cv2.imdecode(np.fromfile('text.png', dtype=np.uint8), 1)

img_ = motion_blur(img,degree=15,angle=90)
 
cv2.imshow('Source image',img)
cv2.imshow('blur image',img_)
cv2.waitKey()
