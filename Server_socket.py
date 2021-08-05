# -*- coding: utf-8 -*-
# @Time : 2021/8/3 16:00
# @Author : 谢泽辉
# @Software : PyCharm

import socketserver
import Log_system
from dataBase_mysql import UsingMysql


#基础语句参考
# search_sql_phoneCount = "SELECT count(phone) as total FROM user_phone  WHERE phone='{}';"
# search_sql_activeCount = "SELECT count(active) as total FROM user_active  WHERE active='{}';"
# search_sql_allCount = "SELECT count(phone) as total FROM user_phone"
# add_sql = "insert into user_phone VALUES ('{}');"
# delete_sql = "delete from user_active where active='{}';"

ls = Log_system

class MyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):  # 处理通信
        while True:
            try:
                conn = self.request     # self.request相当于之前写的conn
                #print("conn")
                addr = self.client_address  #可打印用户ip和端口('127.0.0.1', 50565)
                #print("addr")
                print("用户：",addr)
                #ls.writeLog("用户：{}".format(addr))
                recv_data = conn.recv(1024)     #recv会一直循环直到接收到数据或者连接断开
                #print(recv_data)
                if len(recv_data) == 0:
                    print("break,用户强制断开了连接",addr)      #一般为客户端强制退出的情况
                    ls.writeLog("break,用户强制断开了连接{}".format(addr))
                    break
                recv_data = recv_data.decode('utf8')     #bytes to str
                # *****登录模块*****
                if recv_data[0:4] == "Log-":
                    print("登录开始")
                    #ls.writeLog("登录开始")
                    #这里加入判断  并且插入数据库
                    search_sql_phoneCount = "SELECT count(phone) as total FROM user_phone  WHERE phone='{}';".format(recv_data[4:15])      #format() 里面的内容来替换 {} 和 :
                    with UsingMysql(log_time=True) as um:
                        count = um.get_count(search_sql_phoneCount, None, 'total')
                    if count != 0:      #数据库存在用户手机号
                        conn.send(bytes("true", encoding='utf8'))  # str to bytes
                        print("登录成功",addr)
                        ls.writeLog("登录成功{}".format(addr))
                    else:
                        conn.send(bytes("false", encoding='utf8'))  # str to bytes
                        print("登录失败，数据库不存在手机号", addr)
                        ls.writeLog("登录失败，数据库不存在手机号{}".format(addr))
                # *****注册模块*****
                if recv_data[0:4] == "Reg-":
                    print("注册开始")
                    #ls.writeLog("注册开始")
                    # 这里加入判断  并且插入数据库
                    search_sql_activeCount = "SELECT count(active) as total FROM user_active  WHERE active='{}';".format(recv_data[4:20])  # format() 里面的内容来替换 {} 和 :
                    delete_sql = "delete from user_active where active='{}';".format(recv_data[4:20])
                    add_sql = "insert into user_phone VALUES ('{}');".format(recv_data[21:32])  # 激活码和手机号用-隔开了  所以从21开始
                    with UsingMysql(log_time=True) as um:
                        count = um.get_count(search_sql_activeCount, None, 'total')
                    if count != 0:      #数据库存在该激活码
                        with UsingMysql(log_time=True) as um:
                            um.executeSql(add_sql)
                            um.executeSql(delete_sql)
                        conn.send(bytes("true", encoding='utf8'))  # str to bytes
                        print("注册成功", addr)
                        ls.writeLog("注册成功{}".format(addr))
                    else:
                        conn.send(bytes("false", encoding='utf8'))  # str to bytes
                        print("注册失败，数据库不存该激活码", addr)
                        ls.writeLog("注册失败，数据库不存该激活码{}".format(addr))

            except Exception:
                print("Unknown Error")
                ls.writeLog("Unknown Error")
                break
        conn.close()


if __name__ == '__main__':
    s = socketserver.ThreadingTCPServer(('192.168.0.4', 8080), MyRequestHandler, bind_and_activate=True)
    s.serve_forever()  # 一直处于服务状态
