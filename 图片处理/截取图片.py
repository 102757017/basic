# -*- coding: UTF-8 -*-
from PIL import Image
import sys

#打开图片
im = Image.open('p.png')
print(dir(im))
print(im.format, im.size, im.mode)

#显示图片
im.show()

#截取图片
part1 = im.crop((570, 181, 738, 218))

#转换图片格式
part1.save('p2.jpg')


