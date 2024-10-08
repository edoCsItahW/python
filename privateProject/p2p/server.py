#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/10/3 下午4:36
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from proto import User, debug, Socket, ServerFlag, ClientFlag, Msg, Clients
from time import sleep
from threading import Thread


# TODO: 留出用户接口, 发送心跳包


class Server:
    def __init__(self, port: int):
        self._sock = Socket()
        self._sock.bind(('', port))
        self._clients = Clients()
        self._log = {}
        debug(f"Server start,Monitor the {port} port of all IP addresses", addr=self._sock.getsockname())

    @property
    def self(self) -> User:
        return User('Server', addr=self._sock.getsockname())

    def keepAlive(self):
        while True:
            for client in self._clients:
                if self._log.get(client.name, 0) > 3:
                    debug(f"Client {client} is offline, remove it", addr=client.addr)
                    self._clients.remove(client)
                else:
                    self._sock.sendto(Msg(ClientFlag.HEARTBEAT, sender=self.self, receiver=client), client.addr)
                    self._log[client.name] = self._log.get(client.name, 0) + 1
            sleep(3)

    def listen(self):
        Thread(target=self.keepAlive, daemon=True).start()
        while True:
            data, addr = self._sock.recvFrom()
            data.sender.addr = addr
            if data:
                self.handle(data, addr)

    def handle(self, data: Msg, addr: tuple[str, int]):
        match data.flag:
            # 登录标志
            case ServerFlag.LOGIN:
                debug(f"LOGIN {data.sender}", addr=addr)
                self._clients.append(data.sender)
                self._sock.sendto(Msg(ServerFlag.NONE, self._clients, sender=self.self, receiver=data.sender), addr)
                for client in self._clients:
                    if client != data.sender:
                        self._sock.sendto(Msg(ClientFlag.GETUSER, self._clients, sender=self.self, receiver=client), client.addr)

            # 登出标志
            case ServerFlag.LOGOUT:
                debug(f"LOGOUT {data.sender}", addr=addr)
                for user in self._clients:
                    if user == data.sender:
                        self._clients.remove(user)

            # 点对点通讯构建标志
            case ServerFlag.P2PTRANS:
                # data: C2SMsg
                if user := self._clients[data.info]:
                    debug(f"P2PTRANS {data.sender} -> {user} establish p2p communication request", addr=addr)
                    self._sock.sendto(Msg(ClientFlag.REQUEST, data.sender, sender=self.self, receiver=user), user.addr)
                else:
                    self._sock.sendto(Msg(ClientFlag.ERROR, "User not found", sender=self.self, receiver=data.sender), addr)

            # 获取用户列表标志
            case ServerFlag.GETUSER:
                debug(f"GETUSER {data.sender} get user list", addr=addr)
                self._sock.sendto(Msg(ClientFlag.GETUSER, self._clients, sender=self.self, receiver=data.sender), addr)

            # 心跳包标志
            case ServerFlag.HEARTBEAT:
                self._log[data.sender.name] -= 1

            case ServerFlag.ERROR:
                debug(f"ERROR {data.sender} {data.info}", addr=addr)

            case _:
                print(f"Unknown flag: {data.flag}")


if __name__ == '__main__':
    server = Server(5000)
    server.listen()
