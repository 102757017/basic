# -*- coding: UTF-8 -*-
import pprint


#从fiddler内复制header到此处
headers='''Host: www.yv55.com
Connection: keep-alive
Content-Length: 52
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.yv55.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://www.yv55.com/PersonalCenter
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: safedog-flow-item=; acw_tc=AQAAAEiOGmGTNA4ANsUQG4zEXm/RH0KN; ASP.NET_SessionId=ey5fss5lxdeo1roptysc2kpu; login=117309,2017-10-08 20:15:18; si117309=1; dfw=54awjO1NA5wOthKCv8LDA/ycqv9/p6BiLdLiiVyL0QsPL13pI4bMh/anxSPIxR5Rtg7lU9Y/qJv70RNCULN64CtfREL+Vmp3dQkGeYe68D7ART+6HYIfhPJPNmRUZ1ctBswHBuU5eeEr6AmgPNeigFlJYy3rIwmqoQTi0rtWvzNii/kwFYxoN5NHmzPg3Mbx+f0VLjh23vB28OaenPl3i2N24gPFJeboZ1Zl6J6h4XQDF36jaZVZCxM4tcdgPqnsLKVEhjIjzMhWv3F2Q6OEGaVnT2LHg7ONNie1sKWitiiO8apQeHfh2/e3NnLlL3D+gzsEVxSg33G1yusP1MQyiLxcCxOJVpi9iQtoIY5HqUNETFNkzu6o46WplMqVkQPv1Y4aPV3LnY0TeIdz8BB1E/+TWUsU6GSPE9h/snVF4K2Kfiy/Scwd9PfC5m6QeDpGkKtydArrj6+HO0j+rh0dywQdaa6xSN927MkDzFbUPg2ZXf4mqUiKXjngiKaEDHXLRqUoYnedNPCfIlNME7ZInAn+2f/dr7tBCPtnnOQWPYZDeUJ7QW8JQIRS2TrOXTp5fz0M/D7oabiZvw4HYBLUMO6SaERq3DIot2Kfdw3uSVsUPolHKGvvRGTRBibLM4mAqTlBGt80xT/g9LL1P1L0C+xvEfmnw8E405Vt5virQw2jCbWt1tccnbYATX5WyxuDElsykTNHqsv1RI2KJKEZUTWwak/pTEF7xfhKNJyGTmLDvgubLMmLnKGtf5ff8abcf1926c3b90c39bd0b639f17ae'''



#pprint.pprint(headers)
head={}
a=headers.split("\n")
for x in a:
    b=x.split(": ")
    b1=b[0]
    b2=b[1]
    head[b1]=b2
pprint.pprint(head)

