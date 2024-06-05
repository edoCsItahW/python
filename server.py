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
from threading import Thread
from queue import Queue
from privateProject.minecraftExtent.temp import RCON
from re import sub, match


def commendFormat(cmd: str, sender: str) -> str:
    cmd = cmd.replace("\\", "")

    if "@s" in cmd and cmd[cmd.index("@s") + 1] != "[":
        cmd = cmd.replace("@s", sender)

    if "@a" in cmd and cmd[cmd.index("@a") + 1] != "[":
        cmd = cmd.replace("@a", "@a[name=!baseBot]")

    return cmd


class server:
    def __init__(self, host: str = "127.0.0.1", port: int = 9999):
        self._host = host
        self._port = port
        self._client = None
        self._queue = Queue()

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
    def queue(self): return self._queue

    @property
    def client(self):
        return self._client

    @property
    def rcon(self):
        return self._rcon

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
    #
    # def inputLoop(self):
    #     while cmd := input(">>"):
    #         print(cmd)

    def receive(self):
        # thread = Thread(target=self.inputLoop)
        # thread.start()
        with RCON() as rcon:
            rcon.send("title @a 2s 100 4s")

            while (out := self.client.recv(1024).decode()).lower() != "exit":

                if out == 0:
                    break

                # print(res := getoutput(out))
                if '\\' in out:

                    sender = match(r'<[^>]+> ', out)

                    if sender:
                        sender = sender.group(0)
                    else:
                        sender = out[out.index('>')+1:]

                    print(f"COMMAND: {(cmd := out.replace(sender, ''))}")

                    sender = sender.replace('<', '').replace('>', '')

                    if cmd.startswith(r"\op"):
                        rcon.send(f"tell {sender} You haven't permission to execute this command!")
                    else:
                        res = rcon.send(commendFormat(cmd, sender))

                        rcon.send(rf"tell {sender} {res}")

                        self.client.send((f"SERVER: {res}" if res else "失败或无返回").encode("gbk"))
                else:
                    print(f"MESSAGE: {out}")

                    if "joined the game" in out:
                        rcon.send(f'title @a title {{"text": "欢迎{out.split()[0]}!", "color": "gold", "bold": true}}')


if __name__ == '__main__':
    with server() as s:
        s.accept()
        s.receive()
