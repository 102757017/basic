# -*- coding: UTF-8 -*-
import os
import sys
import urllib.parse
import pprint
import json

os.chdir(sys.path[0])


x_itemid="XXXX"
x_uid="XXXX"
submitref="XXXX"
sparam1="XXXX"
sparam2="XXXX"

confirm_url="https://buy.taobao.com/auction/confirm_order.htm?x-itemid=%s&x-uid=%s&submitref=%s&sparam1=%s&sparam2=%s"%(x_itemid,x_uid,submitref,sparam1,sparam2)
