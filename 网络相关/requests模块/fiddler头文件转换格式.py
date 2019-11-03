# -*- coding: UTF-8 -*-
import pprint



#从fiddler内复制header到此处
headers='''Host: www.zuanke8.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: _uab_collina=155945535796459180308477; ki1e_2132_connect_is_bind=1; ki1e_2132_connect_uin=9EBD874937AC331EDB91B98AC20A9554; Hm_lvt_da6569f688ba2c32429af00afd9eb8a1=1559455359,1559458251,1559458990,1559459041; ki1e_2132_smile=1D1; ki1e_2132_nofavfid=1; ki1e_2132_saltkey=BnaNsRAN; ki1e_2132_lastvisit=1572775471; ki1e_2132_pc_size_c=0; ki1e_2132_con_request_uri=http%3A%2F%2Fwww.zuanke8.com%2Fconnect.php%3Fmod%3Dlogin%26op%3Dcallback%26referer%3Dhttp%253A%252F%252Fwww.zuanke8.com%252Farchiver%252F%253Ffid-15.html; ki1e_2132_client_created=1572779275; ki1e_2132_client_token=9EBD874937AC331EDB91B98AC20A9554; ki1e_2132_connect_secques_uid=442162; ki1e_2132_connect_secques_conopenid=9EBD874937AC331EDB91B98AC20A9554; ki1e_2132_ulastactivity=1572779285%7C0; ki1e_2132_auth=c8eaBPVNztB1p97to0h%2FqE7zB6YFMDTVDjsBq2tkU%2BVV9cC3r4S0dmDu%2Fb2QNLP%2FtTzEUrcwGOBQekeEpFMg55oAqZI; ki1e_2132_connect_login=1; ki1e_2132_stats_qc_login=3; ki1e_2132_atarget=1; ki1e_2132_connect_last_report_time=2019-11-03; ki1e_2132_noticeTitle=1; ki1e_2132_forum_lastvisit=D_15_1572779438; ki1e_2132_lastcheckfeed=442162%7C1572779439; ki1e_2132_checkfollow=1; ki1e_2132_sendmail=1; ki1e_2132_lastact=1572779439%09home.php%09spacecp; ki1e_2132_checkpm=1'''


#pprint.pprint(headers)
head={}
a=headers.split("\n")
for x in a:
    b=x.split(": ")
    b1=b[0]
    b2=b[1]
    head[b1]=b2
pprint.pprint(head)




postdata="params=%7B%22listType%22%3A%22trans_lujinfu%22%2C%22pageIndex%22%3A%221%22%2C%22pageSize%22%3A%2215%22%2C%22width%22%3A1080%2C%22cookieUserName%22%3A%22QzA4NEZCRDYzOTVCQzYzNTE5QjNCNzk2MTUyM0ZCNzY%3D%22%2C%22hasManualFilterKey%22%3Afalse%7D&version=6.1.3"
print("\n\n\n\n\n\n\npost参数")
p={}
c=postdata.split("&")
#pprint.pprint(c)
for x in c:
    d=x.split("=")
    d1=d[0]
    try:
        d2=d[1]
        d2=d2.replace("%2B","+")
        d2=d2.replace("%20"," ")
        d2=d2.replace("%2F","/")
        d2=d2.replace("%3F","?")
        d2=d2.replace("%25","%")
        d2=d2.replace("%26","&")
        d2=d2.replace("%3D","=")
        d2=d2.replace("%23","#")
        d2=d2.replace("%3B",";")
    except:
        d2=""
    p[d1]=d2

pprint.pprint(p)
