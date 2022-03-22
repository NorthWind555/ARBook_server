#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket  # 客户端 发送一个数据，再接收一个数据
import time
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
client.connect(('192.168.0.3', 8081))  # 建立一个链接，连接到本地的6969端口
while True:
    Phone = input()

    send_data = {"Event": "login", "Phone": str(Phone)}

    client.send(bytes(json.dumps(send_data), encoding="utf-8"))  # 发送一条信息 python3 只接收btye流
    data = client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
    # dataJson = json.loads(data.decode())
    # 如果返回的只是一个字符串，不是json数据，则替换成下面代码：
    reciveStr = data.decode("utf-8")
    print(reciveStr)
    time.sleep(1)

client.close()  # 关闭这个链接
