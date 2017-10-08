# -*- coding: UTF-8 -*-
import pprint


#从fiddler内复制header到此处
headers='''Host: www.yv55.com
Connection: keep-alive
Content-Length: 0
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.yv55.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Referer: http://www.yv55.com/PersonalCenter
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: safedog-flow-item=; acw_tc=AQAAAGgmjiZEagEANsUQG7ADO+hDMTt4; ASP.NET_SessionId=0drlfv54gcfu5m5fimroviin; login=117309,2017-10-08 14:41:10; dfw=54awjO1NA5wOthKCv8LDA/ycqv9/p6BiLdLiiVyL0QsPL13pI4bMh/anxSPIxR5Rtg7lU9Y/qJv70RNCULN64CtfREL+Vmp3dQkGeYe68D7ART+6HYIfhPJPNmRUZ1ctBswHBuU5eeEr6AmgPNeigFlJYy3rIwmqoQTi0rtWvzNii/kwFYxoN5NHmzPg3Mbx+f0VLjh23vB28OaenPl3i2N24gPFJeboZ1Zl6J6h4XQDF36jaZVZCxM4tcdgPqnsLKVEhjIjzMhWv3F2Q6OEGaVnT2LHg7ONNie1sKWitiiO8apQeHfh2/e3NnLlL3D+zFwpIOw15dberIYrzNuMUZTSP12AxCKSFOb3+OKwe4s4MWvkW3iBL2Av+iJk98iKeqSnOq83QWPv3NcJVBAnRHnvLTBTfrYm3+RlWbuYzV87vhgrqM8ovcd0iOCbY/PAE/horQvBrL05hHHkTva/RbAqTZ4GpX0c+C23xJg7cBHlR05Q7AOwCFKR6pY7cDUx955wZqIJWYwjkYzJjTGSXSLaIkd3CcPddJzrJXSNrw9Jp//odnmCYYo001inya/emyEwPZyC2snBfw4YQDiv9P5YPKHN8w5376wBsNRyuM5j/n9DdxHI/TuXnKfOqywIG2T2nJwCP1lwmZTIVCynt2Y7TaUS4TImK8wStHvWLXjH+3STZ4xZz1nYy0IafP4TtvVBrhe7rn7kz5Crv3mUBtESwuNzxo03xfhKNJyGTmLDvgubLMmLnKGtf4060767a451bc2b391b7568640b83dc0; si117309=1'''


#pprint.pprint(headers)
head={}
a=headers.split("\n")
for x in a:
    b=x.split(": ")
    b1=b[0]
    b2=b[1]
    head[b1]=b2
pprint.pprint(head)

