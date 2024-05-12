#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/12 上午10:56
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from functools import cached_property


class flag:
    idx = 0

    def __init__(self, name: str):
        self._name = name
        self._value = 1 << flag.idx
        flag.idx += 1

    @property
    def name(self):
        return self._name

    @cached_property
    def value(self):
        return self._value

    def __or__(self, other: 'flag'):
        if not isinstance(other, flag):
            raise TypeError(
                f"unsupported operand type(s) for |: 'flag' and '{other.__class__.__name__}'")

        return self.value | other.value

    def __ror__(self, other: int):
        if not isinstance(other, int):
            raise TypeError(
                f"unsupported operand type(s) for |: '{other.__class__.__name__}' and 'flag'")

        return other | self.value

    def __repr__(self):
        return f"<flag('{self.name}'): {self.value}>"


class flagParser:
    def __init__(self, *args: str):
        self._flags = args
        self._startIdx = 0
        self._flagsDict = {}
        self._resDict = {}

        for f in self.flags:
            self.register(f)

    @property
    def flags(self):
        return self._flags

    @property
    def flagsDict(self):
        return self._flagsDict

    @property
    def resDict(self):
        return self._resDict

    @property
    def startIdx(self):
        return self._startIdx

    def register(self, _flag: str | tuple[str, int] | flag):
        if isinstance(_flag, tuple):
            self._flagsDict[_flag[0]] = _flag[1]
            self.resDict[_flag[0]] = None

        elif isinstance(_flag, flag):
            self._flagsDict[_flag.name] = _flag.value
            self._resDict[_flag.name] = None

        else:
            self._flagsDict[_flag] = 1 << self.startIdx
            self._startIdx += 1
            self._resDict[_flag] = None

    def parse(self, flag: int):
        res = [f for f, v in self.flagsDict.items() if flag & v]
        for f in self._resDict:
            self._resDict[f] = f in res

        return res


if __name__ == '__main__':
    pass
