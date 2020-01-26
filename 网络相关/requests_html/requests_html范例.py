# -*- coding: utf-8 -*-
import os
from requests_html import HTMLSession


url = "https://www.baidu.com/"
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
 'Accept-Encoding': 'gzip, deflate, br',
 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
 'Cache-Control': 'max-age=0',
 'Connection': 'keep-alive',
 'Cookie': 'BAIDUID=48132C6A1BF3B9897FFE15275F5736DA:FG=1; PSTM=1553393591; '
           'BIDUPSID=17F5620CE45F28D3028333618A1BCEF8; '
           'BDUSS=16NEE1VW9zWmctQ3lZcjBQQ3g3cXJhNnhRUjR6Y2ZrNzZFMmhBQ3h-Y2RBZzVlRVFBQUFBJCQAAAAAAAAAAAEAAABBlV0KMTAyNzU3MDE2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB115l0ddeZdNW; '
           'BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; '
           'BD_HOME=1; sugstore=1; BD_CK_SAM=1; PSINO=6; '
           'H_PS_PSSID=1444_21097_26350_28703; '
           'H_PS_645EC=732a0FqhcHVnia81I5PC9Xugh1m8Ry4%2FFbHmAfLS8ajToe65mb%2BigEDvizlZmaHBcun0; '
           'BDSVRTM=0',
 'Host': 'www.baidu.com',
 'Sec-Fetch-Mode': 'navigate',
 'Sec-Fetch-Site': 'none',
 'Sec-Fetch-User': '?1',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

session = HTMLSession()

r = session.get(url,
                headers=headers,
                # cookies=CookieJar,
                verify=False,
                allow_redirects=False,
                timeout=(3, 7),
                # proxies=proxies
                )

link_list = r.html.find('.s-title-yahei', first=False)

# 获取Element对象的所有attributes
attributes=link_list[0].attrs
print(type(attributes),attributes)

for i in link_list:
    print(i.text)


for i in link_list:
    # 获取绝对路径的链接
    print(i.absolute_links)

for i in link_list:
    # 获取对象的属性
    print(i.attrs['data-title'])


# 在子节点中查找对象
link_list[0].find('.xst', first=False)

# 这个大括号里面是相当于替代的词类似于正则里的.也就是所有匹配可以设定开头和结尾中间的大括号里的内容也就是我们想要取出来的文字,返回一个dict
# 该函数也可以用于子节点
# 只获取第一个匹配的对象
d=r.html.search('<input type="submit" value="{obj1}" id="{obj2}" class="btn self-btn bg s_btn"')
print(d["obj1"],d["obj2"])

# 获取所有匹配的对象
d=r.html.search_all('<input type="submit" value="{obj1}" id="{obj2}" class="btn self-btn bg s_btn"')
print(d[0]["obj1"],d[0]["obj2"])