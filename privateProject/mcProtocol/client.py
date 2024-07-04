#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/6/12 上午9:28
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from socket import socket, AF_INET, SOCK_STREAM
from types import TracebackType
from queue import Queue
from threading import Thread, Lock
from time import sleep
from typing import Callable
from package import Package
from warnings import warn
from datetime import datetime
from zlib import compress, decompress, error


def uncompress(data: bytes):
    i = 0
    err = None

    while i >= 0 or i > 6:
        try:
            undata = decompress(data[i:])

        except error as e:
            err = e
            i += 1

        else:
            i = -1

            return data[i:] + undata

    warn(
        f"'{data[:5]}...'解压失败: {err}")


def toOrigin(data: bytes):
    return "b'" + (s := r'\x') + s.join(format(byte, '02x') for byte in data) + "'"


class Client:
    def __init__(self, ip: str = 'localhost', port: int = 25565, *, autoEncode: bool = True, handleRecvFunc: Callable = None, processSendFunc: Callable = None):
        self._ip = ip
        self._port = port
        self._socket = socket(2, 1, 0)  # AF_INET, SOCK_STREAM)
        self._sendQueue = Queue()
        self._threadDict = {}
        self._handleRecvFunc = handleRecvFunc or self.defaulRecvFunc
        self._processSendFunc = processSendFunc or self.defaulSendFunc
        self._resList = []
        self._autoEncode = autoEncode
        self._longData = b''

    @property
    def socket(self) -> socket:
        return self._socket

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def port(self) -> int:
        return self._port

    def _sendLoop(self):
        while True:
            if not self._sendQueue.empty():
                data = self._sendQueue.get()

                self._socket.sendall(data)

                self._processSendFunc(data)

            sleep(0.01)

    def _recvLoop(self):
        while True:
            try:
                data = self._socket.recv(4096)

            except ConnectionAbortedError as e:
                warn(
                    f"connection aborted: '{e.args[1]}'!")

            else:

                if data:
                    self._resList.append(data)

                    self._handleRecvFunc(data)

                else:
                    sleep(0.1)

    def startLoop(self):
        self._threadDict["send"] = Thread(target=self._sendLoop, daemon=True)
        self._threadDict["recv"] = Thread(target=self._recvLoop, daemon=True)

        for thread in self._threadDict.values():
            thread.start()

    def defaulRecvFunc(self, data: bytes):
        now = datetime.now().time().strftime("%H:%M:%S")

        if not self._autoEncode:
            data = "b'" + (s := r'\x') + s.join(format(byte, '02x') for byte in data) + "'"

        if len(data) >= 4096:
            self._longData += data

        else:
            data = self._longData + data

            if data[1] != 0 and len(data) > 256:  # 压缩数据
                print(f"\033[36m[{now}] server <- [{len(data)}] {uncompress(data)}\033[0m")

            else:
                if b'\x04' in data[:4]:
                    print(f"\033[31m[{now}] server <- [{len(data)}] {data}\033[0m")

                else:
                    print(f"\033[34m[{now}] server <- [{len(data)}] {toOrigin(data)}\033[0m")

            self._longData = b''

        # if isinstance(data, bytes) and b'\x24' in data[:5]:
        #     print("this is a keepalive packet")
        #     self.register(Package(4, True, data=("Byte", data[3:])))

    @staticmethod
    def defaulSendFunc(data: bytes):
        now = datetime.now().time().strftime("%H:%M:%S")

        print(f"\033[32m[{now}] client -> {data}\033[0m")

    def __enter__(self):
        self._socket.connect((self._ip, self._port))

        self.startLoop()

        return self

    def __exit__(self, exc_type: type[Exception], exc_val: str, exc_tb: TracebackType):

        for thread in self._threadDict.values():
            thread.join()

        self._socket.close()

        if exc_val:
            raise exc_type(
                exc_val) from RuntimeError(
                f"{exc_tb.tb_lineno} {exc_tb.tb_frame.f_code}")

    def register(self, data: Package | bytes, *, wait: bool = True):
        if isinstance(data, Package):
            self._sendQueue.put(data.data)

        elif isinstance(data, bytes):
            self._sendQueue.put(data)

        else:
            raise TypeError(
                "data must be Basetype or bytes")

    def waitRecv(self, times: int = 1) -> bytes:
        self._resList = []

        while len(self._resList) < times:
            sleep(0.01)

        result = self._resList[-1]

        self._resList = []

        return result


if __name__ == '__main__':
    with Client() as client:
        # client.register(Package(
        #     protocolVersion=("VarInt", 765),
        #     ip=("String", client.ip),
        #     port=("UShort", client.port),
        #     nextState=("VarInt", 1)), wait=False)
        #
        # client.register(Package())
        #
        # # client.waitRecv()
        #
        # client.register(Package(1,
        #                         payload=("Long", 0)))

        client.register(Package(
            protocolVersion=("VarInt", 765),
            ip=("String", client.ip),
            port=("UShort", client.port),
            nextState=("VarInt", 2)))

        client.register(Package(
            name=("String", "Player"),
            uuid=("Uuid", ("Player", {"offline": True}))))

        client.waitRecv()

        client.register(Package(3, True))

        client.waitRecv()

        client.waitRecv()

        client.register(Package(2, True))
