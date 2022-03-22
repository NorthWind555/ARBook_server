import socketserver
import Log_system
from dataBase_mysql import UsingMysql

# 基础语句参考
# search_sql_phoneCount = "SELECT count(phone) as total FROM user_phone  WHERE phone='{}';"
# search_sql_activeCount = "SELECT count(active) as total FROM user_active  WHERE active='{}';"
# search_sql_allCount = "SELECT count(phone) as total FROM user_phone"
# add_sql = "insert into user_phone VALUES ('{}');"
# delete_sql = "delete from user_active where active='{}';"
# search_sql_value = "SELECT is_login FROM user_phone  WHERE phone='{}';"
# update_sql = "UPDATE user_phone SET is_login=‘1’ WHERE phone='{}';"　　　

ls = Log_system
log_succ_flag = 0  # 用户是否登录成功的标志  0 登录失败 1登录成功
g_conn_pool = []  # 连接池


class MyRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):  # 处理通信
        global log_succ_flag
        global User_phone
        while True:
            try:
                conn = self.request  # self.request相当于之前写的conn
                # print("conn")
                addr = self.client_address  # 可打印用户ip和端口('127.0.0.1', 50565)
                # print("addr")
                g_conn_pool.append(addr)
                print("用户列表", g_conn_pool)
                # ls.writeLog("用户：{}".format(addr))
                while True:
                    recv_data = conn.recv(1024)  # recv会一直循环直到接收到数据或者连接断开
                    # print(recv_data)
                    # *****强制断开***** #
                    if len(recv_data) == 0:
                        if log_succ_flag == 1:
                            update_sql2 = "UPDATE user_phone SET is_login='0' WHERE phone='{}';".format(User_phone)
                            with UsingMysql(log_time=True) as um:
                                um.executeSql(update_sql2)
                        print("break,用户", User_phone, "强制断开了连接", addr)  # 一般为客户端强制退出的情况
                        ls.writeLog("break,用户强制断开了连接{}".format(addr))
                        break
                    recv_data = recv_data.decode('utf8')  # bytes to str

                    if recv_data[0:4] == "Esc-":
                        # *****退出模块***** #
                        self.ExitModule(recv_data)
                    elif recv_data[0:4] == "Log-":
                        # *****登录模块***** #
                        self.LoginModule(recv_data, conn, addr)
                    elif recv_data[0:4] == "Reg-":
                        # *****注册模块***** #
                        self.RegistrationModule(recv_data, conn, addr)
            except Exception:
                print("Unknown Error 或者用户未操作直接退出")
                ls.writeLog("Unknown Error 或者用户未操作直接退出")
                break
        conn.close()

    # *****登录模块***** #
    def LoginModule(self, recv_data, conn, addr):
        global log_succ_flag
        print("登录开始")
        # ls.writeLog("登录开始")
        # 这里加入判断  并且插入数据库
        search_sql_phoneCount = "SELECT count(phone) as total FROM user_phone  WHERE phone='{}';".format(
            recv_data[4:15])  # format() 里面的内容来替换 {} 和 :
        search_sql_value = "SELECT is_login FROM user_phone  WHERE phone='{}';".format(recv_data[4:15])
        update_sql = "UPDATE user_phone SET is_login='1' WHERE phone='{}';".format(recv_data[4:15])
        User_phone = recv_data[4:15]
        with UsingMysql(log_time=True) as um:
            count = um.get_count(search_sql_phoneCount, None, 'total')
        if count != 0:  # 数据库存在用户手机号
            # 开始判断该手机号是否已经登录
            with UsingMysql(log_time=True) as um:
                result_value = um.get_value(search_sql_value)
            if result_value['is_login'] == '0':
                # 用户未登录
                with UsingMysql(log_time=True) as um:
                    um.executeSql(update_sql)
                conn.send(bytes("true", encoding='utf8'))  # str to bytes
                log_succ_flag = 1
                print("用户:", User_phone, "登录成功", addr)
                ls.writeLog("登录成功{}".format(addr))

            else:
                conn.send(bytes("false", encoding='utf8'))  # str to bytes
                log_succ_flag = 0
                print("用户:", User_phone, "登录失败,该手机号已登录", addr)
                ls.writeLog("登录失败,该手机号已登录{}".format(addr))
        else:
            conn.send(bytes("false", encoding='utf8'))  # str to bytes
            log_succ_flag = 0
            print("登录失败，不存在该手机号", addr)
            ls.writeLog("登录失败，不存在手机号{}".format(addr))

    # *****注册模块***** #
    def RegistrationModule(self, recv_data, conn, addr):

        print("注册开始")
        # ls.writeLog("注册开始")
        # 这里加入判断  并且插入数据库
        search_sql_phoneCount = "SELECT count(phone) as total FROM user_phone  WHERE phone='{}';".format(
            recv_data[21:32])
        search_sql_activeCount = "SELECT count(active) as total FROM user_active  WHERE active='{}';".format(
            recv_data[4:20])  # format() 里面的内容来替换 {} 和 :

        search_sql_values = "SELECT is_res FROM user_active  WHERE active='{}';".format(recv_data[4:20])
        update_sql2 = "UPDATE user_active SET is_res='1' WHERE active='{}';".format(recv_data[4:20])
        # delete_sql = "delete from user_active where active='{}';".format(recv_data[4:20])
        add_sql = "insert into user_phone VALUES ('{}','0');".format(recv_data[21:32])  # 激活码和手机号用-隔开了  所以从21开始
        with UsingMysql(log_time=True) as um:
            counts = um.get_count(search_sql_phoneCount, None, 'total')
        if counts == 0:  # 数据库存没有该手机号
            with UsingMysql(log_time=True) as um:
                count = um.get_count(search_sql_activeCount, None, 'total')
            if count != 0:  # 数据库存在该激活码
                with UsingMysql(log_time=True) as um:
                    result_value = um.get_value(search_sql_values)
                if result_value['is_res'] == '0':
                    with UsingMysql(log_time=True) as um:
                        um.executeSql(update_sql2)
                        um.executeSql(add_sql)
                    conn.send(bytes("true", encoding='utf8'))  # str to bytes
                    print("注册成功", addr)
                    ls.writeLog("注册成功{}".format(addr))

                else:
                    conn.send(bytes("false", encoding='utf8'))  # str to bytes
                    print("注册失败，激活码已被使用", addr)
                    ls.writeLog("注册失败，激活码已被使用{}".format(addr))
            else:
                conn.send(bytes("false", encoding='utf8'))  # str to bytes
                print("注册失败，不存该激活码", addr)
                ls.writeLog("注册失败，不存该激活码{}".format(addr))
        else:
            conn.send(bytes("false", encoding='utf8'))  # str to bytes
            print("注册失败，该手机号已注册", addr)
            ls.writeLog("注册失败，该手机号已注册{}".format(addr))

    # *****退出模块***** #
    def ExitModule(self, recv_data):

        update_sql3 = "UPDATE user_phone SET is_login='0' WHERE phone='{}';".format(User_phone)
        with UsingMysql(log_time=True) as um:
            um.executeSql(update_sql3)
        print("用户：", User_phone, "已退出")


if __name__ == '__main__':
    # 0为正式版配置  1为测试版本配置(xzh专用)
    mode = 1
    if mode == 0:
        s = socketserver.ThreadingTCPServer(('192.168.0.5', 8081), MyRequestHandler, bind_and_activate=True)
        # 客户端:39.99.37.97   服务器端：172.17.4.84
        print("IP：172.17.4.84   端口：8081")
        s.serve_forever()  # 一直处于服务状态
    elif mode == 1:
        s = socketserver.ThreadingTCPServer(('192.168.120.10', 8081), MyRequestHandler, bind_and_activate=True)
        s.serve_forever()  # 一直处于服务状态
