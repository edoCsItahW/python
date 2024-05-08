#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/5/8 上午11:08
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
__all__ = [
    'command',
    'interpreter'
]


from abc import ABC, abstractmethod
from typing import final, overload
from types import FunctionType
from functools import singledispatchmethod, partial
from warnings import warn
from inspect import isfunction


class command(ABC):
    @abstractmethod
    def interpret(self, *_command: str):
        pass


class interpreter:
    @final
    def __init__(self):
        self._commands = {}

    @final
    @property
    def commands(self): return self._commands

    @final
    @commands.setter
    def commands(self, value):
        self._commands = value

    @overload
    def register(self, _command: command, commandObj: None):
        ...

    @overload
    def register(self, _command: str, commandObj: command):
        ...

    @final
    @singledispatchmethod
    def register(self, _command: str | FunctionType | type[command], commandObj: command | None = None):
        """
        将命令执行类或函数注册至解释器.

        :param _command:
        :param commandObj:
        :return:
        """
        if isfunction(_command):
            self.commands[_command.__name__] = _command

        elif isinstance(_command, partial):
            self.commands[_command.func.__name__] = _command

        elif issubclass(_command, command):
            self.commands[_command.__class__.__name__] = _command
            return
        else:
            raise TypeError(
                f"只能注册函数或者继承于'{command.__class__.__name__}'类的子类!")

    @register.register(str)
    def _(self, _command: str, commandObj: command):
        self.commands[_command] = commandObj

    def parse(self, _command: str) -> bool | None:
        if not _command: return
        commandList = list(filter(bool, _command.split(" ")))

        try:
            c.interpret(*commandList[1:]) if issubclass(c := self.commands[commandList[0]], command) else c(*commandList[1:])
        except KeyError:
            warn(
                f"在注册命令表中没有找到'{commandList[0]}', 请检查是否注册了该命令,或者注册或键入了错误的拼写!")
            return False
        else:
            return True


if __name__ == '__main__':
    pass
