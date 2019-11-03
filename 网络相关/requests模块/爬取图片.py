# -*- coding: UTF-8 -*-
import requests
import io
from PIL import Image
import cv2
import numpy as np

url = "https://user.lu.com/user/captcha/captcha.jpg?source=login&_=1550756412573"
headers={'Accept': 'image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5',
 'Accept-Encoding': 'gzip, deflate, br',
 'Accept-Language': 'zh-CN',
 'Connection': 'Keep-Alive',
 'Cookie': '_g=n_430765_3bebd7ed-fd77-4f9a-873a-c416fb5c20c9; '
           '_g2=n_430765_4ada9ed7-3844-432e-aeff-64ad881341f3; '
           'IMVC=542273a092234c57a453814bdabc8ce3; '
           '_fp="x9hEVzIwMTkwMTA4MDQ1NTI3MjUxNTgx_fEqK0kpx4KtOKGrLmNfm8S703o0U0MI9TQsme6CdNzAhay9Z3QOBYoRVktuw1M/nPPs=:Q86W07C5WE3ciQPUTFy6WO8Qk5QYuUFrDD509Md4JpM="; '
           'WT-FPC=id=4.0.4.13-3612462752.30722538:lv=1550756344903:ss=1550756344903:fs=1550756344903:pn=1:vn=1; '
           'Hm_lvt_9842c7dcbbff3109ea37b7407dd0e95c=1550756345; '
           'Hm_lpvt_9842c7dcbbff3109ea37b7407dd0e95c=1550756345',
 'Host': 'user.lu.com',
 'Referer': 'https://user.lu.com/user/login',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 '
               'Edge/17.17134'}


#访问https页面时，将verify设置为false将不会验证网站的CA证书，隐患是可能访问到假网站，钓鱼网站
#allow_redirects是否允许重定向（页面跳转）
#timeout 3s钟没有响应就不重新尝试了
r=requests.get(url,headers=headers,verify=False,allow_redirects=False,timeout=3)
stream = io.BytesIO(r.content)
img = Image.open(stream)
img.show()

img=cv2.imdecode(np.fromstring(r.content,np.uint8), 1)
cv2.imshow("img", img)
