# -*- coding:utf-8 -*-
#import browsercookie
import browser_cookie3
import tldextract
import pprint
import requests

"""
支持chrome和firefox浏览器的cookies导出，如果同时安装了两个浏览器，会将两者的cookies合并
统一cookie数据格式:[{},{}]
"""
def get_cookie(websize):
    """
    需要将直接获取浏览器的cookie
    :return:dict
    """
    domain = '.{}.{}'.format(tldextract.extract(websize).domain, tldextract.extract(websize).suffix)
    cookies = browser_cookie3.load()
    items = dict()
    for cookie in cookies:
        item = items.get(cookie.domain, [])
        item.append({'domain': cookie.domain, 'expiry': cookie.expires,
                     'path': cookie.path, 'name': cookie.name,
                     'secure': cookie.secure, 'value': cookie.value})
        items[cookie.domain] = item
    data = items.get(domain, [])
    if not data:
        return False
    return data



if __name__ == '__main__':
    url = "https://buy.taobao.com"
    cookies=get_cookie(url)
    CookieJar = requests.utils.cookiejar_from_dict({c['name']: c['value'] for c in cookies})
    print(type(CookieJar))
    #CookieJar可以直接传入requests中使用，requests.get(url,headers,cookies=CookieJar)
    for item in CookieJar:
        print(item.name + "=" +item.value + ";")
    tb_token=CookieJar.get("_tb_token_")
    print(tb_token)


