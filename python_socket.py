# _*_ coding: utf-8 _*_

"""
Socket编程
"""

import sys
import socket


def server_func(port):
    """
    服务端
    """
    # 1. 创建socket对象
    server = socket.socket()

    # 2. 绑定ip和端口
    server.bind(("127.0.0.1", port))

    # 3. 监听是否有客户端连接
    server.listen(10)
    print(f"服务端已经启动{port}端口......")

    # 4. 接收客户端连接
    sock_obj, address = server.accept()
    sock_obj.settimeout(3)
    print(f"客户端：{address}，超时时间：{sock_obj.gettimeout()}")

    while True:
        try:
            # 5. 接收客户端发送的消息
            recv_data = sock_obj.recv(1024).decode("utf-8")
            print(f"客户端端 -> 服务端: {recv_data}")
            if recv_data == "quit":
                break

            # 6. 给客户端回复消息
            send_data = f"received[{recv_data}]"
            sock_obj.send(send_data.encode("utf-8"))
            print(f"服务端 -> 客户端: {send_data}")
        except Exception as excep:
            print("error: ", excep)

    # 7. 关闭socket对象
    sock_obj.close()
    server.close()


def client_func(port):
    """
    客户端
    """
    # 1. 创建客户端的socket对象
    client = socket.socket()

    # 2. 连接服务端， 需要指定端口和IP
    client.connect(("127.0.0.1", port))

    while True:
        # 3. 给服务端发送数据
        send_data = input("客户端>").strip()
        client.send(send_data.encode("utf-8"))
        if send_data == "quit":
            break

        # 4. 获取服务端返回的消息
        recv_data = client.recv(1024).decode("utf-8")
        print(f"服务端 -> 客户端: {recv_data}")

    # 5. 关闭socket连接
    client.close()


if __name__ == '__main__':
    flag = sys.argv[1]
    if flag == "server":
        server_func(9901)
    else:
        client_func(9901)
