import cv2
import numpy as np



def brisque_quality_assessment(img_path):
    # 读取图像
    img = cv2.imread(img_path)
    if img is None:
        print("无法读取图像")
        return None
    
    # 创建BRISQUE评估器
    try:
        # 方法1: 使用create方法
        brisque = cv2.quality.QualityBRISQUE.create("brisque_model_live.yml", "brisque_range_live.yml")
        
        # 计算质量分数
        score = brisque.compute(img)
        print(f"BRISQUE Score: {score[0]}")
        return score[0]
        
    except Exception as e:
        print(f"错误: {e}")
        return None

# 使用示例
score = brisque_quality_assessment("p2.jpg")
