#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from socket import *
import socket


#设置服务器ip地址
host = "127.0.0.1" 
port = 13000
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
  data = input("请输入要发送的消息，或输入'exit'退出: ")
  #将数据转换为utf-8再进行传输
  data=data.encode('utf-8')
  UDPSock.sendto(data, addr)
  if data == "exit":
    break
UDPSock.close()
os._exit(0)
