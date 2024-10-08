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
from proto import User, debug, Socket
from time import sleep
from threading import Thread
from atexit import register


# @register
# def closeSocket():
#     sock, addr, name = globals()['sock'].values()
#     sock.sendto(C2SMsg(MsgType.LOGOUT, Logout(name)), addr)
#     sock.close()


class Client:
    usage = """你可以输入以下命令:
    命令: send [name] [msg]  向指定用户发送消息
    命令: getuser  获取在线用户列表
    命令: exit  退出程序
    """

    def __init__(self, ip: str, port: int, *, name: str = None):
        self._sock = Socket()
        self._name = name
        self._addr = (ip, port)  # 服务器地址
        self._clients: list[User] = []
        self._ack = False

    def send(self, name: str, msg: str):
        user = [i for i in self._clients if i.name == name][0]
        for _ in range(3):
            self._ack = False
            self._sock.sendto(P2PMsg(TransType.MSG, *self._addr), (user.ip, user.port))
            self._sock.sendto(msg, (user.ip, user.port))
            for _ in range(3):
                if self._ack:
                    break
                else:
                    sleep(0.1)

        self._sock.sendto(C2SMsg(MsgType.P2PTRANS, P2PTrans(self._name)), self._addr)

    def login(self):
        self._name = self._name or input("请输入昵称: ")
        self._sock.sendto(C2SMsg(MsgType.LOGIN, Login(self._name, '')), self._addr)
        count, _ = self._sock.recvFrom()
        print(f"当前在线用户: {count}")
        for _ in range(count):
            data, _ = self._sock.recvFrom()
            print(f"用户: {data}")
            self._clients.append(data)

    def handle(self, data: S2CMsg | int, addr: tuple[str, int]):
        match data.type if hasattr(data, 'type') else data:
            # 用户间聊天信息
            case TransType.MSG:
                # P2PMsg
                debug(f"收到用户<{data.ip}:{data.port}>聊天标志位", ip=addr[0], port=addr[1])
                msg, _ = self._sock.recvFrom()

                print(f"接收到信息: {msg}")

                self._sock.sendto(P2PMsg(TransType.RESPONSE, *self._addr), addr)

            # 打洞请求
            case TransType.REQUEST:
                debug(f"收到用户<{data.msg.name}>打洞请求", ip=addr[0], port=addr[1])
                self._sock.sendto(P2PMsg(TransType.TRASH, *self._addr), addr)

            # 打洞响应
            case TransType.RESPONSE:
                debug(f"收到用户<{data.msg.name}>打洞响应", ip=addr[0], port=addr[1])
                print("打洞成功")
                self._ack = True

            #
            case TransType.TRASH:
                debug(f"收到用户<{data.msg.name}>打洞垃圾", ip=addr[0], port=addr[1])
                print("收到TRASH")
                pass

            # 获取在线用户列表
            case TransType.GETUSER:
                debug(f"向服务器请求在线用户列表", ip=addr[0], port=addr[1])
                count, _ = self._sock.recvFrom()
                self._clients.clear()
                for _ in range(count):
                    user, _ = self._sock.recvFrom()
                    self._clients.append(user)

    def listen(self):
        while True:
            data, addr = self._sock.recvFrom(wait=False)
            if data:
                self.handle(data, addr)
            else:
                continue

    def run(self):
        self.login()

        Thread(target=self.listen).start()

        print(self.usage)
        while cmds := input(f"请输入命令: ").split():
            match cmds[0]:
                case 'exit':
                    self._sock.sendto(C2SMsg(MsgType.LOGOUT, Logout(self._name)), self._addr)
                    self._sock.close()
                    exit()
                case 'getuser':
                    self._sock.sendto(MsgType.GETUSER, self._addr)
                case _:
                    self.send(cmds[1], ' '.join(cmds[2:]))


if __name__ == '__main__':
    Client('127.0.0.1', 5000, name='mobile').run()
