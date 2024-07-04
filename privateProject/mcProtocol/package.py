#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/6/11 下午7:03
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from baseType import *
from typing import TypeVar, Literal
from functools import cache, cached_property
from warnings import warn
from queue import Queue
from time import sleep
from threading import Thread


ParamMcType = TypeVar('ParamMcType')
ParamValue = TypeVar('ParamValue', str, int, bool)


@cache
def typeDict() -> dict[str, type]:
    import baseType
    return {name: getattr(baseType, name) for name in baseType.__all__ if name not in baseType.ignoreList}


def dictInterpret(**kwargs: tuple[ParamMcType | Basetype, ParamValue | tuple] | Literal["like: protocol=(VarInt, 123), sign=('Boolean', True)"]):
    result = b''

    for name, (Type, value) in kwargs.items():
        args, _kwargs = [], {}

        if isinstance(value, tuple):
            for arg in value:
                if isinstance(arg, dict):
                    _kwargs.update(arg)

                else:
                    args.append(arg)

        else:
            args.append(value)

        if isinstance(Type, str) and Type in typeDict():
            result += typeDict()[Type](*args, **_kwargs).byte

        elif issubclass(Type, Basetype):
            result += Type(value).byte

        else:

            warn(
                f"Available types: {', '.join(typeDict().keys())}")

            raise TypeError(
                f"Type {Type} is not supported.")

    return result


class Package:
    def __init__(self, _id: int = 0, compress: bool = False, **kwargs: tuple[ParamMcType | Basetype, ParamValue] | Literal["like: protocol=(VarInt, 123), sign=('Boolean', True)"]):
        self._id = _id
        self._compress = compress
        self._kwargs = kwargs

    @cached_property
    def data(self):
        return bytes(VarInt(len(b := ((b'\x00' if self._compress else b'') + VarInt.intToVarint(self._id) + dictInterpret(**self._kwargs)))).byte + b)


if __name__ == '__main__':
    print(Package(0, sign=('Boolean', True)).data)
    pass

