#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/11 下午6:23
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from socket import socket, AF_INET, SOCK_STREAM
from subprocess import getoutput
from functools import cached_property


class server:
    def __init__(self, host: str = "127.0.0.1", port: int = 9999):
        self._host = host
        self._port = port
        self._client = None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @cached_property
    def socket(self):
        return socket(AF_INET, SOCK_STREAM)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    def __enter__(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()
        if self.client:
            self.client.close()

    def accept(self):
        print("等待客户端连接...")
        self.client, addr = self.socket.accept()
        print(f"连接来自: {addr}")

    def receive(self):
        while (out := self.client.recv(1024).decode().lower()) != "exit":

            if out == 0:
                break

            print(res := getoutput(out))
            self.client.send(res.encode())


if __name__ == '__main__':
    with server() as s:
        s.accept()
        s.receive()
