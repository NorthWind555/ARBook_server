# from dataBase_mysql import UsingMysql
import Log_system as ls
from event_mysql import UsingMysql

sql_get_phoneCount = "SELECT count(phone) as total FROM user_phone  WHERE phone='{}';"

sql_get_activeCount = "SELECT count(active) as total FROM user_active  WHERE active='{}';"

sql_get_isuseValue = "SELECT is_use FROM user_active  WHERE active='{}';"

sql_update_isuseValue = "UPDATE user_active SET is_use='1' WHERE active='{}';"

sql_add_phone = "insert into user_phone VALUES ('{}');"

# 发送给客户端的语句合集
msg_success = "true"
msg_false_uselessPhone = "false_1"  # 手机号未注册
msg_false_duplicatePhone = "false_2"  # 手机号已注册
msg_false_incorrectActivationCode = "false_3"  # 激活码错误（已激活或者不存在）


# *****登录事件***** #
def login_event(recv_data, conn, addr, online_list, conn_list):
    user_phone = recv_data["Phone"]

    if user_phone in online_list:
        out_index = online_list.index(user_phone)
        out_conn = conn_list[out_index]
        online_list, conn_list = logout_client_event(out_conn, online_list, conn_list, out_index)

        conn.send(bytes(msg_success, encoding='utf8'))  # str to bytes
        content = "用户:" + user_phone + "登录成功"
        print(content)
        ls.writeLog(content)
        online_list.append(user_phone)
        conn_list.append(conn)
    else:
        # 账号处于未登录状态
        print("登录开始")
        with UsingMysql(log_time=True) as um:
            count = um.get_count(sql_get_phoneCount.format(user_phone), None, 'total')

        if count != 0:  # 数据库存在用户手机号
            conn.send(bytes(msg_success, encoding='utf8'))  # str to bytes
            content = "用户:" + user_phone + "登录成功"
            print(content)
            ls.writeLog(content)
            online_list.append(user_phone)
            conn_list.append(conn)

        else:
            conn.send(bytes(msg_false_uselessPhone, encoding='utf8'))  # str to bytes
            content = "登录失败，不存在该手机号：" + user_phone
            print(content)
            ls.writeLog(content)
    return online_list, conn_list


# *****注册模块***** #
def registration_event(recv_data, conn, addr, online_list, conn_list):
    user_phone = recv_data["Phone"]
    user_activationCode = recv_data["Active"]

    print("注册开始")
    with UsingMysql(log_time=True) as um:
        count = um.get_count(sql_get_activeCount.format(user_activationCode), None, 'total')
    if count != 0:  # 数据库存在该激活码
        with UsingMysql(log_time=True) as um:
            result_value = um.get_value(sql_get_isuseValue.format(user_activationCode))
        if result_value['is_use'] == '0':  # 激活码未被使用
            with UsingMysql(log_time=True) as um:
                counts = um.get_count(sql_get_phoneCount.format(user_phone), None, 'total')
            # # 测试用
            # counts = 0
            if counts == 0:  # 数据库存没有该手机号
                with UsingMysql(log_time=True) as um:
                    um.executeSql(sql_update_isuseValue.format(user_activationCode))
                    um.executeSql(sql_add_phone.format(user_phone))
                conn.send(bytes(msg_success, encoding='utf8'))  # str to bytes
                content = "用户:" + user_phone + "注册成功"
                print(content)
                ls.writeLog(content)
            else:
                conn.send(bytes(msg_false_duplicatePhone, encoding='utf8'))  # str to bytes
                content = "用户:" + user_phone + "注册失败，该手机号已注册"
                print(content)
                ls.writeLog(content)
        else:
            conn.send(bytes(msg_false_incorrectActivationCode, encoding='utf8'))  # str to bytes
            content = "用户:" + user_phone + "注册失败，激活码已被使用"
            print(content)
            ls.writeLog(content)
    else:
        conn.send(bytes(msg_false_incorrectActivationCode, encoding='utf8'))  # str to bytes
        content = "用户:" + user_phone + "注册失败，不存该激活码"
        print(content)
        ls.writeLog(content)


# *****强制退出客户端连接***** #
def logout_client_event(out_conn, online_list, conn_list, out_index):
    out_conn.send(bytes("quit", encoding='utf8'))
    out_conn.close()
    online_list.pop(out_index)
    conn_list.pop(out_index)
    return online_list, conn_list
