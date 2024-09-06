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
from functools import cached_property
from threading import Thread
from datetime import datetime
from warnings import warn
from socket import socket, AF_INET, SOCK_STREAM
from typing import Literal
from mcrcon import MCRcon
from queue import Queue
from time import sleep
from re import match


def formatMsg(msg: str | bytes, *, dst: Literal['in', 'out', 'no'], Type: str = None) -> str:
    return f"[{datetime.now().strftime('%d/%b/%Y %H:%M:%S')}]{f' <{Type}>' if Type else ''} {'<-' if dst == 'in' else '->' if dst == 'out' else '--'} {msg}"


def commendFormat(cmd: str, sender: str) -> str:
    """
    预处理指令,以便服务器执行

    :param cmd: 原始指令
    :param sender: 发送者
    :return: 格式化后的指令
    """
    cmd = cmd.replace("\\", "")

    if "@s" in cmd and cmd[cmd.index("@s") + 1] != "[":
        cmd = cmd.replace("@s", sender.replace(" ", ""))

    if "@a" in cmd and cmd[cmd.index("@a") + 1] != "[":
        cmd = cmd.replace("@a", "@a[name=!baseBot]")  # TODO: 替换写死的玩家名

    return cmd


class RCON:
    def __init__(self, *, address: str = "127.0.0.1", port: int = 25575):
        self._address = address
        self._port = port
        self._rcon = MCRcon(self._address, 'password', self._port)
        self._conFlag = False

    @cached_property
    def rcon(self):
        if not self._conFlag:
            self._rcon.connect()
            self._conFlag = True
        return self._rcon

    def __enter__(self):
        self._rcon.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rcon.disconnect()

    def send(self, instruction: str):
        return self.rcon.command(instruction)

    def continuousInput(self):
        closeFlag = True
        while closeFlag:
            if (ins := input('Minecraft RCON> /')).lower() != 'exit':

                if ins.split(" ")[0].lower() == "op":
                    warn("You can't use 'op' command!")

                print(self.send(ins))
            else:
                print('退出程序')
                closeFlag = False


class server:
    def __init__(self, host: str = "127.0.0.1", port: int = 9999):
        self._host = host
        self._port = port
        self._client = None
        self._queue = Queue()
        self._rcon = RCON()

    @cached_property
    def socket(self):
        return socket(AF_INET, SOCK_STREAM)

    def __enter__(self):
        self.socket.bind((self._host, self._port))
        self.socket.listen(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()
        if self._client:
            self._client.close()

    def accept(self):
        print(formatMsg("Waiting for connection...", dst='no'))
        self._client, addr = self.socket.accept()
        print(formatMsg(f"Accepted connection from {addr}", dst='no'))

    def sendReturn(self, res: str):
        self._client.send((res or 'Execution failed').encode("gbk"))

        print(formatMsg(res or 'Execution failed', dst='out', Type='MESSAGE'))

    def _executor(self):
        while True:
            cmd = self._queue.get()

            res = self._rcon.send(cmd)

            self.sendReturn(res)

            sleep(0.1)

    @staticmethod
    def _procCmd(cmd: str):
        try:
            # 获取发送者
            sender = s.group(0) if (s := match(r'<[^>]+> ', cmd)) else cmd[cmd.index('>') + 1:]
        except ValueError as e:
            warn(f"对于指令{cmd}的发送者解析失败: {e}!")
            sender = "<Unknown>"

        print(formatMsg(cmd := cmd.replace(sender, ''), dst='in', Type='COMMAND'))

        # 去除包裹发送者的尖括号
        sender = sender.replace('<', '').replace('>', '')

        return cmd, sender

    def send(self):
        Thread(target=self._executor, daemon=True).start()

    def receive(self):
        while (out := self._client.recv(1024).decode()).lower() != "exit":
            if '\\' in out:
                for rawCmd in out.split('|'):
                    if rawCmd:
                        cmd, sender = self._procCmd(rawCmd)

                        # 发送指令并获取返回值
                        self._queue.put(commendFormat(cmd, sender))

            else:
                print(formatMsg(out, dst='in', Type='MESSAGE'))

                if "joined the game" in out:  # 欢迎新玩家
                    self._rcon.send(f'title @a title {{"text": "欢迎{out.split()[0]}!", "color": "gold", "bold": true}}')

    def run(self):
        self.accept()
        self._rcon.send("title @a 2s 100 4s")
        self.send()
        self.receive()


if __name__ == '__main__':
    # pyinstaller -F server.py --exclude-module PyQt6 --exclude-module PyQt5
    with server() as s:
        s.run()
