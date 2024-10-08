#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/10/2 下午10:16
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from pickle import dumps, loads
from typing import overload, Optional, Any
from datetime import datetime
from socket import socket, AF_INET, SOCK_DGRAM


@overload
def debug(msg: str, *, addr: tuple[str, int]): ...


@overload
def debug(msg: str, *, ip: str, port: int): ...


def debug(*args, **kwargs):
    if len(args) < 1:
        raise TypeError(f"{debug.__name__} missing 1 required positional argument: 'msg'")
    elif len(args) > 1:
        raise TypeError(f"{debug.__name__} takes 1 positional arguments but {len(args)} were given")

    if len(kwargs) < 1:
        raise TypeError(f"TypeError: {debug.__name__} missing 1 required keyword-only argument: 'addr'")
    elif len(kwargs) > 2:
        raise TypeError(f"TypeError: {debug.__name__} got an unexpected keyword argument '{list(kwargs.keys())[2]}'")

    addr = f"{k[0]}:{k[1]}" if (k := kwargs.get('addr')) else f"{kwargs.get('ip')}:{kwargs.get('port')}"
    print(f"{addr} - - [{datetime.now():%d/%b/%Y %H:%M:%S}] '{args[0]}' -")


class ServerFlag:
    LOGIN = 1
    LOGOUT = 2
    P2PTRANS = 3
    GETUSER = 4
    NONE = 5
    REDIRECT = 6
    HEARTBEAT = 7
    ERROR = 8


class ClientFlag:
    MSG = 101
    REQUEST = 102
    RESPONSE = 103
    TRASH = 104
    GETUSER = 105
    HEARTBEAT = 106
    ERROR = 107


class User:
    def __init__(self, name: str, *, addr: Optional[tuple[str, int]]):
        self.name = name
        self._addr = addr

    def __repr__(self):
        return f"[{self.name}: <{self.ip}:{self.port}>]"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, User):
            return self.name == other.name and self.addr == other.addr
        return False

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value: tuple[str, int]):
        self._addr = value

    @property
    def ip(self):
        return self._addr[0]

    @property
    def port(self):
        return self._addr[1]


class Clients(list):
    def __getitem__(self, item: int | str) -> User | None:
        if isinstance(item, int):
            return super().__getitem__(item)
        elif isinstance(item, str):
            for user in self:
                if user.name == item:
                    return user
            return None
        raise TypeError(f"list indices must be integers or strings, not {type(item).__name__}")

    def append(self, __object):
        if not isinstance(__object, User):
            raise TypeError(f"append() argument must be User, not {type(__object).__name__}")
        if any(user.name == __object.name for user in self):
            raise ValueError(f"User {__object.name} already exists in the list")
        super().append(__object)


class Msg:
    def __init__(self, flag: ServerFlag = ServerFlag.NONE, info: Any = None, *, sender: User, receiver: User):
        self.flag = flag
        self.info = info
        self.sender = sender
        self.receiver = receiver


class Socket(socket):
    def __init__(self, __family: int = AF_INET, __type: int = SOCK_DGRAM):
        super().__init__(__family, __type)
        self.setblocking(False)

    def sendto(self, __data, __address):
        super().sendto(dumps(__data), __address)

    def recvFrom(self, __bufsize: int = 1024, *, wait: bool = True):
        while True:
            try:
                data, address = super().recvfrom(__bufsize)
                return loads(data), address
            except BlockingIOError:
                if not wait:
                    return None, None
                continue
