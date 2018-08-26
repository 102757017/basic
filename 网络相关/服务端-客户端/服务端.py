#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket
import os


#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = ""
port = 13000
buf = 1024
addr = (host, port)
# 创建一个socket
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#设置超时时间
UDPSock.settimeout(3)

#服务器端要用 bind() 函数将套接字与特定的IP地址和端口绑定起来，只有这样，流经该IP地址和端口的数据才能交给套接字处理
UDPSock.bind(addr)
print("等待接受消息...")
while True:
  (data, addr) = UDPSock.recvfrom(buf)

  #客户端发送的数据是utf-8编码的，需要转换为Unicode码才能正常显示
  data=data.decode('utf-8')
  print("接收到消息: " , data)
  if data == "exit":
    break
UDPSock.close()
os._exit(0)
