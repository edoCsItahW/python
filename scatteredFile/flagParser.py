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
    """
    一个简单的flag类，用于管理flag的状态.

    Attributes:
        :ivar _name: flag的名称.
        :ivar _value: flag的值.

    Methods::
        :meth:`name`: 返回flag的名称.

        :meth:`value`: 返回flag的值.
    """
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
    """
    flag解析器,用于解析flag,并返回哪些flag被激活.

    Example::

        >>> a, b, c = flag('a'), flag('b'), flag('c')
        >>> fp = flagParser(a, b, c)
        >>> fp.parse(a | c)
        ['a', 'c']
        >>> fp.resDict
        {'a': True, 'b': False, 'c': True}


    Attributes:
        :ivar _flags: 待解析的flag列表.
        :ivar _startIdx: 左移位的起始位数.
        :ivar _flagsDict: 注册的flag字典.
        :ivar _resDict: 解析结果字典.

    Methods::
        :meth:`flags`: 返回待解析的flag列表.

        :meth:`flagsDict`: 返回注册的flag字典.

        :meth:`resDict`: 返回解析结果字典.

        :meth:`startIdx`: 返回左移位的起始位数.

        :meth:`register`: 注册一个flag.

        :meth:`parse`: 解析一个flag,并返回激活的flag列表.

    """
    def __init__(self, *args: str | flag | tuple[str, int]):
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

    def register(self, _flag: str | tuple[str, int] | flag) -> None:
        """
        注册flag.(一般情况下,flag在初始化时会将初始化参数中的flag注册到flagParser中,但也可以手动注册flag)

        :param _flag: 待注册的flag,可以是flag对象,flag名称字符串,或(flag名称字符串,flag值整数)元组.
        :type _flag: str | tuple[str, int] | flag
        """
        if isinstance(_flag, tuple):
            self._flagsDict[_flag[0]] = _flag[1]
            self.resDict[_flag[0]] = False

        elif isinstance(_flag, flag):
            self._flagsDict[_flag.name] = _flag.value
            self._resDict[_flag.name] = False

        else:
            self._flagsDict[_flag] = 1 << self.startIdx
            self._startIdx += 1
            self._resDict[_flag] = False

    def parse(self, _flag: int | None = None) -> list[str]:
        """
        解析flag,并返回激活的flag列表.

        :param _flag: 待解析的flag整数.
        :type _flag: int
        :return: 激活的flag列表.
        :rtype: list[str]
        """
        if _flag:
            res = [f for f, v in self.flagsDict.items() if _flag & v]

            for f in self._resDict:
                self._resDict[f] = f in res

            return res

        else:
            return []


if __name__ == '__main__':
    pass
