# -*- coding: UTF-8 -*-
import requests
import browser_cookie3

url="https://opencredit.jd.com/act/get/coupon?couponBusinessId=071d6089cca2022c87dd6089ebd685ad&actId=004&agreementSource=77&platform=3&pageClickKey=jr%7Ckeycount%7Cxbxy_ktyh%7Ccoupon199&eid=5OFMAQPGUPZFKIG24NSZIMB5RQ2XUIRUMZB7U4QWQHGFZJXJ57JJ6MBPDIWN6YEISC4EKO4O2PWSILDZWXJGVX6YRQ&fp=f5360b1889ad0f30246632c59bc00e74&referUrl=https%3A%2F%2Fplogin.m.jd.com%2Flogin%2Flogin%3Fappid%3D119%26returnurl%3Dhttps%253A%252F%252Fcredit.jd.com%252Fchannel%252Fktyh.html"
#用这种方式提取不出cookies内的值
cj = browser_cookie3.chrome()
r=requests.get(url,cookies=cj,verify=False)
print(r.text)
           
