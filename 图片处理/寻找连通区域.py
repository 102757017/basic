# -*- coding: UTF-8 -*-
import cv2
import numpy as np

img = np.array([[0, 255, 0, 0],[0, 0, 0, 255],[0, 0, 0, 255],[255, 0, 0, 0]], np.uint8)
_, labels = cv2.connectedComponents(img)
print(labels)

#stats 是bounding box的信息，N*5的矩阵，行对应每个label，五列分别为[x0, y0, width, height, 面积]
# centroids 是每个域的质心坐标
_, labels, stats, centroids = cv2.connectedComponentsWithStats(img)
print(labels)
print(stats)
print(centroids)
