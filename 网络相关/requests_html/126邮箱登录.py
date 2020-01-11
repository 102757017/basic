# -*- coding: UTF-8 -*-
# 必须先设置环境变量，指定pyppteer的路径
import os
os.environ['PYPPETEER_HOME'] = 'D:\Program Files'
import requests
from requests_html import HTMLSession
import pprint
import asyncio
import win32api,win32con
import random

# 无头模式下navigator.webdriver为true，将webdriver的状态值改为false
js1='() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }'

# chrome属性检测，在无头模式下window.chrome属性是undefined
js2='''() =>{ window.navigator.chrome = { runtime: {},  }; }'''

# 无头模式下Notification.permission与navigator.permissions.query会返回相反的值
js3='''() => {
                  const originalQuery = window.navigator.permissions.query;
                  return window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                      Promise.resolve({ state: Notification.permission }) :
                      originalQuery(parameters)
                  );
                }
            '''

# navigator.languages可以获取一个数组，里面存储的是浏览器用户所有的次选语言。而无头浏览器的navigator.languages返回的是空字符串
js4='''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }'''

# navigator.plugins会返回一个数组，里面的元素代表浏览器已安装的插件，无头浏览器通常是没有插件的
js5='''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }'''

js6 = """
                () => {
                    return {
                        webdriver: navigator.webdriver,
                        chrome: navigator.chrome,
                        permission: Notification.permission,
                        query:navigator.permissions.query,
                        languages: navigator.languages,
                        plugins: navigator.plugins,
                    }
                }
               """


width=win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
heigth=win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴

# 需要修改源码，在BaseSession的__init__方法添加一个关键字参数headless=True
r = HTMLSession(browser_args=['--window-size={},{}'.format(width,heigth),#只有headless=False时才需要设置该参数
                              '--disable-extensions',
                              '--hide-scrollbars',
                              '--disable-bundled-ppapi-flash',
                              '--mute-audio',  # 页面静音
                              '--no-sandbox',  # 以最高权限运行
                              '--disable-setuid-sandbox',
                              '--disable-gpu',
                              '--disable-infobars'
                              ],
                headless=False,
                autoClose=False #脚本完成时自动关闭浏览器进程。默认为True
                )

url = 'https://mail.126.com/'

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'mail.126.com',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'cross-site',
           'Sec-Fetch-User': '?1',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

rs = r.get(url,
           headers=headers,
           # cookies=CookieJar,
           verify=False,
           allow_redirects=False,
           timeout=(3, 7),
           # proxies=proxies
           )

# 获取页面上的所有链接,以绝对路径的方式。
#pprint.pprint(rs.html.absolute_links)

try:
    # 调用pyppeteer执行js渲染html页面,默认重新发起一次请求
    # keep_page,默认为False,需要设置为True，否则后面无法使用r.html.page,这个是与浏览器交互的关键,最好关闭已经使用过的页面，如果打开过多页面会造成浏览器崩溃
    # reload 默认为True,如果为False,如果为False,就会从内存中加载内容
    # script，JS 脚本，可选参数，默认为None,str类型，如果有值，返回JS执行脚本的返回值
    result=rs.html.render(keep_page=True,reload=True,script=js6)
    print(result)

    # async关键字：定义一个协程函数
    # await关键字只能放在协程函数里，await语法来挂起自身的协程，并等待另一个协程完成直到返回结果
    async def main():
        # 设置浏览器头部
        await rs.html.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36')
        
        # 浏览器窗口很大，内容显示很小，需要设定page.setViewport
        await rs.html.page.setViewport({'width': width, 'height': heigth})
        
        # page.evaluateOnNewDocument在页面载入前注入js代码
        # js无法跨域，如果检测代码在iframe内部，就在iframe内部再执行了一次注入js
        # 可以在开发者工具中按ctrl+f，先搜一下frame，也可以在console的选择框中确认选中元素所属的iframe
        await rs.html.page.evaluateOnNewDocument(js1)
        await rs.html.page.evaluateOnNewDocument(js2)
        await rs.html.page.evaluateOnNewDocument(js3)
        await rs.html.page.evaluateOnNewDocument(js4)
        await rs.html.page.evaluateOnNewDocument(js5)

        # 重新加载页面，使注入的js生效后进行再渲染
        await rs.html.page.goto('https://mail.126.com/')
        # 点击使用密码登录
        await rs.html.page.click("#lbNormal")

        # 获取当前页面所有的iframe
        frames= rs.html.page.frames
        # 遍历iframe,获取目标的序号
        for i, x in enumerate(frames):
            title = await x.title()
            name = x.name
            print("No:{} ,iframe_title:{}   ,   iframe_name:{}".format(i,title,name))

        # 输入用户名
        # 用CSS选择器选择元素，#表示选择id，.表示选择class，详见css选择器手册，class="j-inputtext dlemail j-nameforslide"，class中的空格是为了给html标签同时赋予多个class类名
        # CSS选择器中不能出现空格，.class1 .class2中间的空格表示.class2是.class1的子节点，选中子节点
        await frames[4].type(".j-inputtext.dlemail", "username", {'delay': random.randint(100, 151) - 50})
        await frames[4].type(".j-inputtext.dlpwd", "password", {'delay': random.randint(100, 151) - 50})
        #点击登录按钮
        await frames[4].click("#dologin")

        # 异步延时
        await asyncio.sleep(5)
        # 鼠标悬停在验证码上
        await frames[4].hover('.yidun_tips')



        #await rs.html.page.screenshot({r'H:\学习资料\编程学习\pathon\基础操作\basic\网络相关\requests_html':'1.png'}) # 传入参数用字典path 代表路径 值为你要存放的路径

    asyncio.get_event_loop().run_until_complete(main())

    # 打印渲染后的html
    #print(rs.html.html)

finally:
    pass
    # 关闭浏览器
    #r.close()