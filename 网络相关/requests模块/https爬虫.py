# -*- coding: UTF-8 -*-
import requests


url = "https://github.com/"
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.8',
 'Cache-Control': 'max-age=0',
 'Connection': 'keep-alive',
 'Host': 'github.com',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, '
               'like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 '
               'Safari/537.36'}


#访问https页面时，将verify设置为false将不会验证网站的CA证书，隐患是可能访问到假网站，钓鱼网站
#allow_redirects是否允许重定向（页面跳转）
#timeout 3s钟没有响应就不重新尝试了
r=requests.get(url,headers=headers,verify=False,allow_redirects=False,timeout=3)
a=r.text
print(a)
