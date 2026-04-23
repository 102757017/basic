# -*- coding: UTF-8 -*-
import os
import urllib.request
import requests

# 1. 设置全局代理环境变量
os.environ["http_proxy"] = "http://username:password@proxyserver:port"
os.environ["https_proxy"] = "http://username:password@proxyserver:port"


# === 2. 核心补丁：拦截 urlretrieve，让其走 requests ===
'''
底层的 urllib 库不支持自动解析代理密码：anomalib 内部下载权重文件时，使用的是 Python 自带的 urllib.request.urlretrieve 方法。
虽然 urllib 会自动读取系统环境变量 http_proxy 和 https_proxy，但是它默认的代理处理器（ProxyHandler）并不会自动解析代理 URL 中的账号和密码。
这就导致了下载请求直接发往代理服务器时，因为**缺少鉴权（407 Proxy Authentication Required）**而被代理服务器拒绝。

'''
_original_urlretrieve = urllib.request.urlretrieve

def patched_urlretrieve(url, filename=None, reporthook=None, data=None):
    # 非 HTTP 协议退回到自带方法
    if not url.startswith('http'):
        return _original_urlretrieve(url, filename, reporthook, data)
        
    proxies = {
        "http": os.environ.get("http_proxy"),
        "https": os.environ.get("https_proxy")
    }
    
    print(f"\n[Proxy Patch] 正在通过代理下载: {url}")
    # requests 能完美识别并处理 URL 中的 heei:wico3 鉴权信息
    response = requests.get(url, proxies=proxies, stream=True)
    response.raise_for_status()
    
    content_length = response.headers.get('content-length')
    total_size = int(content_length) if content_length is not None else None
    block_size = 8192
    count = 0
    
    with open(filename, 'wb') as f:
        # 激活 tqdm 进度条 (0 bytes)
        if reporthook:
            reporthook(0, block_size, total_size)
            
        # 分块写入文件并同步更新进度条
        for chunk in response.iter_content(chunk_size=block_size):
            if chunk:
                f.write(chunk)
                count += 1
                if reporthook:
                    reporthook(count, block_size, total_size)
                    
    return (filename, response.headers)

# 在导入 anomalib 之前执行全局替换
urllib.request.urlretrieve = patched_urlretrieve
# =========================================================


import anomalib
