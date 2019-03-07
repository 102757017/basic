# coding: utf-8
#!/usr/bin/python
from PIL import Image,ImageDraw,ImageFont

ttfont = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf",20)
im=Image.new('RGB', (100, 100), (255,255,200))
draw = ImageDraw.Draw(im)
draw.text((10,10),'hello', fill=(0,0,0),font=ttfont)
im.show()
