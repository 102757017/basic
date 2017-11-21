# -*- coding: UTF-8 -*-
import os
import time
import pprint
import requests
import urllib
import re
import chardet

from couplelink import makeurl
from allurl import GetAllUrl

a=open(os.path.join(os.path.dirname(__file__),"AllCouple",'couples.html'),'w')
a.write('''<html>
<head><title>Ordering notice</title></head>
<body>
''')
urls=GetAllUrl()
for index,item in enumerate(urls):
    print(index)
    CoupleInfos=makeurl(item)
    if len(CoupleInfos)!=0:
        for CoupleInfo in CoupleInfos:
            describ=CoupleInfo[0][1:-1]+CoupleInfo[1][1:-1]+CoupleInfo[2][1:-1]+"\n"+CoupleInfo[5]
            body="<a href="+CoupleInfo[4]+"><img src="+CoupleInfo[3]+" alt="+describ+"></a>"
            a.write(body)
            a.write("\n")
a.write('''</body>
</html>
''')
a.close()
