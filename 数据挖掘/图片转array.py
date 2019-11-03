# -*- coding: UTF-8 -*-
from PIL import Image
import sys
from numpy import array


def Img2Array(path):
    #打开图片
    im = Image.open(path)
    
    #截取图片
    #im = im.crop((570, 181, 738, 218))
    
    print(im.format, im.size, im.mode)
    obj=array(im)
    return obj

if __name__=="__main__":
    a=Img2Array(r"H:\学习资料\编程学习\pathon\基础操作\basic\图片处理\p.png")
    print(a.shape,a.size)
    print(a)
    


#转换图片格式
#part1.save('p2.jpg')


