#!/usr/bin/python
# -*- coding: UTF-8 -*-
import telnetlib

def telnet():
    debugging = 0
    rcfile = None

    '''初始化telnet信息'''
    telnet_host='192.168.2.1'
    telnet_userid = 'admin'
    telnet_passwd = 'admin'
    telnet_port = '23'


    tn = telnetlib.Telnet()
    tn.set_debuglevel(debugging)
    tn.open(telnet_host, telnet_port)

    '''登陆主机后，提示输入用户名后会换行'''
    tn.read_until(str.encode("\n"))

    a=telnet_userid + "\n\r"
    b=str.encode(a)
    tn.write(b)

    '''登陆主机后，提示输入密码后会换行'''
    tn.read_until(str.encode("\n"))

    a=telnet_passwd + "\r"
    b=str.encode(a)
    tn.write(b)

    
    command="/etc/init.d/parentctl stop"
    a=command + "\r"
    b=str.encode(a)
    tn.write(b)

    tn.interact()


    tn.close()
telnet()
