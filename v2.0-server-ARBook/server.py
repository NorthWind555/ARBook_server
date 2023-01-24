import json
import socketserver
import Log_system as ls
import eventProcessing as ep
import threading



online_list = []
conn_list = []




class MyRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):  # 处理通信
        event = ''
        recv_data = ''

        conn = self.request

        addr = self.client_address  # 可打印用户ip和端口('127.0.0.1', 50565)

        while True:
            try:
                print("当前在线列表：", online_list)
                returned_data = conn.recv(1024)  # recv会一直循环直到接收到数据或者连接断开

                # *****用户断开连接***** #
                if len(returned_data) == 0:
                    content = "用户：" + recv_data["Phone"] + "强制断开了连接"
                    out_index = online_list.index(recv_data["Phone"])
                    online_list.pop(out_index)
                    conn_list.pop(out_index)
                    print(content)  # 一般为客户端强制退出的情况
                    ls.writeLog(content)
                    break
                event, recv_data = self.getData(returned_data)  # 数据解析处理

                if event == "login":
                    # *****登录模块***** #
                    ep.login_event(recv_data, conn, addr, online_list, conn_list)
                elif event == "register":
                    # *****注册模块***** #
                    ep.registration_event(recv_data, conn, addr, online_list, conn_list)


            except Exception:
                print("Unknown Error 或者用户未操作直接退出")
                # ls.writeLog("Unknown Error 或者用户未操作直接退出")
                break


        conn.close()

    def getData(self, returned_data):
        # 数据为json格式,{"Event":"res","Phone":"15319405520","RegCode":"qqq"}

        recv_data = json.loads(returned_data.decode('utf8'))

        event = recv_data["Event"]
        data = recv_data
        return event, data




# # 自定义指令  有BUG
# def customCommand():
#     commandList = ["list"]
#     while True:
#         word = input()
#         for comm in commandList:
#             if (word == comm and comm == "list"):
#                 print("当前在线列表：", online_list)
#                 print("对应地址列表：", conn_list)

if __name__ == '__main__':
    # 0为正式版配置  1为测试版本配置(xzh专用)
    mode = 1
    if mode == 0:
        s = socketserver.ThreadingTCPServer(('172.17.4.84', 8081), MyRequestHandler, bind_and_activate=True)
        # 客户端:39.99.37.97   服务器端：172.17.4.84
        print("IP：172.17.4.84   端口：8081")
        s.serve_forever()  # 一直处于服务状态
    elif mode == 1:
        s = socketserver.ThreadingTCPServer(('192.168.173.10', 8081), MyRequestHandler, bind_and_activate=True)
        s.serve_forever()  # 一直处于服务状态
