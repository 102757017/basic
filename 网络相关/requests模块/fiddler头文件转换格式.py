# -*- coding: UTF-8 -*-
import pprint


#从fiddler内复制header到此处
headers='''Connection: keep-alive
Content-Length: 52
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://www.yv55.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://www.yv55.com/PersonalCenter
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie: safedog-flow-item=; acw_tc=AQAAAEfyWC7zTQ4ANsUQGwXbzFT0NfEv; ASP.NET_SessionId=4cilgass5hqoxbqgwvetucty; login=117309,2017-10-07 12:30:56; si117309=1; dfw=54awjO1NA5wOthKCv8LDA/ycqv9/p6BiLdLiiVyL0QsPL13pI4bMh/anxSPIxR5Rtg7lU9Y/qJv70RNCULN64CtfREL+Vmp3dQkGeYe68D7ART+6HYIfhPJPNmRUZ1ctBswHBuU5eeE81isLSiw8rhnr+mv4l9ZJpCog3sVZIcf9bVAvrIefXbb8z0rEYJ5RiTIGlqSDOrCHIk8TXxsJCNSFbzObZM+m+X97mCoT0xu7J+UdcaMoysAycXTLJSr1S1eW1e6lm9dFXW5C7sVRsfkZ+70XLYEEVryTKgKRR7A34JOeeXaRhU+orgc1GcSN6ZH+9sOYjb4JdTwTqmdALQ9MZzTHbgn8a4Ogzv+omKsQ7oL4qQPjVUG75qptpqZbER3egvb3gUCyvbMX1Ew0n4dqC7LdFNf02/b9VAtv0ynW27tXQ0UjozGT7hhDKwzvH8GHWWchdvy/ns+/YLUhEKTi4kn/WhxDv2P5OlOCAbke+gnp97p1NaIdZnfseEGigM6/m7epwzrACcsUX9VAhbpqpcoB3viXAdkxDVOgrHjrHAqlYLCw2p2CHx/biznH9+KU88eSqGC2C7L3e+1sunraO6Mb8Puty41YnjbsqU58GVlLikCQzG5KZslLBI1KAKqY+pI7Ljy4uuIE/JWATgK1/PfxCq/hFsuGUpWGU+aQPSbooSnzh8QOjHCwuMpmx4eAqJXYVohWgbN1FQ3yxYmPJrdG6oLuxfhKNJyGTmLDvgubLMmLnKGtf6a929fdb8eb7e3f775fc9817c79911c7'''

#pprint.pprint(headers)
head={}
a=headers.split("\n")
for x in a:
    b=x.split(": ")
    b1=b[0]
    b2=b[1]
    head[b1]=b2
pprint.pprint(head)

