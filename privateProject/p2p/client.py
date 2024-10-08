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
from proto import User, debug, Socket, Msg, ServerFlag, ClientFlag, Clients
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
        self._clients = Clients()
        self._ack = False

    @property
    def self(self):
        return User(self._name or 'Client', addr=None)

    @property
    def server(self):
        return User('Server', addr=self._addr)

    def send(self, name: str, msg: str):
        if user := self._clients[name]:
            self._ack = False
            self._sock.sendto(Msg(ClientFlag.MSG, msg, sender=self.self, receiver=user), user.addr)
            for _ in range(3):
                if self._ack:
                    break
                else:
                    sleep(0.1)

            self._sock.sendto(Msg(ServerFlag.P2PTRANS, name, sender=self.self, receiver=self.server), self._addr)
        else:
            debug(f"用户'{name}'不在线或不存在", addr=self._addr)

    def login(self):
        self._name = self._name or input("请输入昵称: ")
        self._sock.sendto(Msg(ServerFlag.LOGIN, sender=self.self, receiver=self.server), self._addr)
        data, _ = self._sock.recvFrom()
        self._clients = data.info

    def handle(self, data: Msg, addr: tuple[str, int]):
        match data.flag:
            # 用户间聊天信息
            case ClientFlag.MSG:
                debug(f"MSG {data.sender}'s chat flag", addr=addr)
                print(f"接收到信息: {data.info}")
                self._sock.sendto(Msg(ClientFlag.RESPONSE, sender=self.self, receiver=data.sender), addr)

            # 打洞请求
            case ClientFlag.REQUEST:
                # P2PMsg
                debug(f"REQUEST {data.sender}'s hole punching request", addr=addr)
                self._sock.sendto(Msg(ClientFlag.TRASH, sender=self.self, receiver=data.sender), data.info.addr)

            # 打洞响应
            case ClientFlag.RESPONSE:
                debug(f"RESPONSE {data.sender}'s hole punching response", addr=addr)
                self._ack = True

            #
            case ClientFlag.TRASH:
                debug(f"TRASH {data.sender}'s trash message", addr=addr)

            case ClientFlag.HEARTBEAT:
                self._sock.sendto(Msg(ServerFlag.HEARTBEAT, sender=self.self, receiver=self.server), self._addr)

            # 获取在线用户列表
            case ClientFlag.GETUSER:
                self._clients = data.info

            case ClientFlag.ERROR:
                debug(f"ERROR {data.info}", addr=addr)

            case _:
                debug(f"Unknown flag: {data.flag}", addr=addr)

    def listen(self):
        while True:
            data, addr = self._sock.recvFrom(wait=False)
            if data:
                data.sender.addr = addr
                self.handle(data, addr)
            else:
                continue

    def run(self):
        try:
            self.login()

            Thread(target=self.listen).start()

            print(self.usage)
            while cmds := input(f"请输入命令: ").split():
                match cmds[0]:
                    case 'exit':
                        self._sock.sendto(Msg(ServerFlag.LOGOUT, sender=self.self, receiver=self.server), self._addr)
                        self._sock.close()
                        exit()
                    case 'getuser':
                        self._sock.sendto(Msg(ServerFlag.GETUSER, sender=self.self, receiver=self.server), self._addr)
                    case _:
                        if cmds[0] == 'send':
                            self.send(cmds[1], ' '.join(cmds[2:]))
        except KeyboardInterrupt:
            self._sock.sendto(Msg(ServerFlag.LOGOUT, sender=self.self, receiver=self.server), self._addr)
            self._sock.close()
            exit()
        except Exception as e:
            debug(f"Error: {e}", addr=self._addr)
            self._sock.sendto(Msg(ServerFlag.ERROR, sender=self.self, receiver=self.server, info=str(e)), self._addr)


if __name__ == '__main__':
    # Client(args.ip, args.port, name=args.name).run()
    Client('129.204.24.232', 5000, name='pc').run()
