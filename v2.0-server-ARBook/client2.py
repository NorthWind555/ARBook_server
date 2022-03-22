#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket  # 客户端 发送一个数据，再接收一个数据
import time
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
client.connect(('192.168.20.1', 8081))  # 建立一个链接，连接到本地的6969端口

send_data_1 = {"Event": "login", "Phone": "15319405521"}
send_data_2 = {"Event": "register", "Phone": "15319405520", "Active": "A2002ytuP594JpL9"}

client.send(bytes(json.dumps(send_data_2), encoding="utf-8"))  # 发送一条信息 python3 只接收btye流
data = client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
# dataJson = json.loads(data.decode())
# 如果返回的只是一个字符串，不是json数据，则替换成下面代码：
reciveStr = data.decode()
print(reciveStr)
time.sleep(1)
data = client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
print("2次接收", data.decode())

client.close()  # 关闭这个链接
