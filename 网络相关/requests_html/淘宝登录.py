# -*- coding: utf-8 -*-
import os
import time
import random
import asyncio #协程库
import pyppeteer
import win32api,win32con

'''
由于pyppeteer久未更新有bug，需要修改源码，找到pyppeteer包下的connection.py模块，在其43行和44行改为下面这样： 
self._ws = websockets.client.connect( 
#self._url, max_size=None, loop=self._loop) 
self._url, max_size=None, loop=self._loop, ping_interval=None, ping_timeout=None)
websockets 这个库的版本，因为必须保证这个库是 7.0 的版本。8.0 和 6.0 虽然可以使用，但是在访问多个网页会出现一些无法解决的异常
'''
import pyppeteer.chromium_downloader
print('默认版本是：{}'.format(pyppeteer.__chromium_revision__))
print('可执行文件默认路径：{}'.format(pyppeteer.chromium_downloader.chromiumExecutable.get('win64')))
print('win64平台下载链接为：{}'.format(pyppeteer.chromium_downloader.downloadURLs.get('win64')))
class LoginTaoBao:
    """
    类异步
    """
    pyppeteer.DEBUG = True
    page = None

    # async关键字：定义一个协程函数
    # await关键字只能放在协程函数里，await语法来挂起自身的协程，并等待另一个协程完成直到返回结果
    # page.evaluateOnNewDocument在页面载入前注入js代码
    # js无法跨域，如果检测代码在iframe内部，就在iframe内部再执行了一次注入js
    async def _injection_js(self):       
        # 无头模式下navigator.webdriver为true，将webdriver的状态值改为false
        await self.page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }')  # 本页刷新后值不变

        # chrome属性检测，在无头模式下window.chrome属性是undefined
        await self.page.evaluateOnNewDocument('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')

        # 无头模式下Notification.permission与navigator.permissions.query会返回相反的值
        await self.page.evaluateOnNewDocument('''() => {
                  const originalQuery = window.navigator.permissions.query;
                  return window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                      Promise.resolve({ state: Notification.permission }) :
                      originalQuery(parameters)
                  );
                }
            ''')

        # navigator.languages可以获取一个数组，里面存储的是浏览器用户所有的次选语言。而无头浏览器的navigator.languages返回的是空字符串
        await self.page.evaluateOnNewDocument('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')

        # navigator.plugins会返回一个数组，里面的元素代表浏览器已安装的插件，无头浏览器通常是没有插件的
        await self.page.evaluateOnNewDocument('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    async def _init(self):
        """初始化浏览器
        """
        width=win32api.GetSystemMetrics(win32con.SM_CXSCREEN)   #获得屏幕分辨率X轴
        heigth=win32api.GetSystemMetrics(win32con.SM_CYSCREEN)   #获得屏幕分辨率Y轴
        browser = await pyppeteer.launch({'headless': False,
                                          # 'userDataDir': './userdata',
                                          'args': [
                                              '--window-size={},{}'.format(width,heigth),#只有headless=False时才需要设置该参数
                                              '--disable-extensions',
                                              '--hide-scrollbars',
                                              '--disable-bundled-ppapi-flash',
                                              '--mute-audio',#页面静音
                                              '--no-sandbox',#以最高权限运行
                                              '--disable-setuid-sandbox',
                                              '--disable-gpu',
                                              '--disable-infobars'
                                          ],
                                          'dumpio': True, #chromium浏览器多开页面卡死问题，解决这个问题的方法就是浏览器初始化的时候添加'dumpio':True。
                                          "executablePath":r"D:\Program Files\local-chromium\575458\chrome-win32\chrome.exe", # Chromium的路径
                                          "userDataDir":'./userdata' #设置用户目录,进行cookies的保存，下次打开可以免登录。如果没有设置，每次打开就是一个全新的浏览器
                                          })
        self.page = await browser.newPage()
        # 设置浏览器头部
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
        # 浏览器窗口很大，内容显示很小，需要设定page.setViewport
        await self.page.setViewport({'width': width, 'height': heigth})

    async def get_cookie(self):
        cookies_list = await self.page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        print(cookies)
        return cookies

    async def mouse_slider(self):
        """滑动滑块
        """
        await asyncio.sleep(3)
        try:
            # 鼠标悬停在匹配元素上
            await self.page.hover('#nc_1_n1z')
            # 鼠标按下按钮
            await self.page.mouse.down()
            # 移动鼠标，steps是将我们传入的距离分成 ‘steps’ 段来执行，steps越大 则 越耗时，滑动越慢
            await self.page.mouse.move(2000, 0, {'steps': 30})
            # 松开鼠标
            await self.page.mouse.up()
            await asyncio.sleep(2)
        except Exception as e:
            print(e, '      :错误')
            return None
        else:
            await asyncio.sleep(3)
            # 获取元素内容
            slider_again = await self.page.querySelectorEval('#nc_1__scale_text', 'node => node.textContent')
            if slider_again != '验证通过':
                return None
            else:
                print('验证通过')
                return True

    async def main(self, username_, pwd_):
        """登陆
        """
        # 初始化浏览器
        await self._init()
        # 注入js
        await self._injection_js()
        # 打开淘宝登陆页面
        await self.page.goto('https://login.taobao.com')

        # await self.page.goto('https://www.taobao.com')
        # time.sleep(1000000)
        # 点击密码登陆按钮
        await self.page.click('div.login-switch')
        time.sleep(random.random() * 2)
        # 输入用户名
        await self.page.type('#TPL_username_1', username_, {'delay': random.randint(100, 151) - 50})
        # 输入密码
        await self.page.type('#TPL_password_1', pwd_, {'delay': random.randint(100, 151)})
        time.sleep(random.random() * 2)
        # 参数1为css选择器
        # 参数2为js的箭头函数，函数内容是获取节点的style属性
        slider = await self.page.Jeval('#nocaptcha', 'node => node.style')
        # 如果滑块属性非空
        if slider:
            print('有滑块')
            # 移动滑块
            flag = await self.mouse_slider()
            if not flag:
                print('滑动滑块失败')
                return None
            time.sleep(random.random() + 1.5)
            # 点击登陆
            print('点击登陆')
            await self.page.click('#J_SubmitStatic')
            await asyncio.sleep(1000)

        print('点击登陆')
        await self.page.keyboard.press('Enter')

        cookies = await self.get_cookie()
        time.sleep(10000)


if __name__ == '__main__':
    username = input('请输入淘宝用户名')
    password = input('密码')
    login = LoginTaoBao()
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(login.main(username, password))
    loop.run_until_complete(task)
