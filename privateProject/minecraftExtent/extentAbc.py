#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/5/4 上午1:03
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from mcpi.minecraft import Minecraft
from abc import ABC, abstractmethod
from typing import final, Callable
from functools import wraps


__all__ = [
    'MC',
    'Extent',
    'MCPI'
]


countLog = {'_checkAttr': 0}


class MC(ABC):
    @final
    def run(self, instance: 'Extent'):
        try:
            getattr(instance, '_checkAttr')()
        except AttributeError:
            raise NotImplementedError(
                f"该实例没有实现'_checkAttr'方法, 请在实例中实现该方法!")


def trackCount(func: Callable):
    global countLog

    if func.__name__ in countLog:
        countLog[func.__name__] += 1
    else:
        countLog[func.__name__] = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


class Extent(ABC):
    def __init__(self, *, address: str = '127.0.0.1', port: int):
        self._address = address
        self._port = port

    @abstractmethod
    @property
    def session(self):
        pass

    @final
    @trackCount
    def _checkAttr(self):
        if not all(hasattr(self, attr) for attr in ('_address', '_port')):
            raise AttributeError(
                f"extent object must have '_address' and '_port' attributes")

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    if countLog['_checkAttr'] == 0:
        raise NotImplementedError(
            f"请在__init__方法最后调用'_checkAttr'方法!")


class MCPI(Extent):
    @final
    def __init__(self, *, address: str = '127.0.0.1', port: int = 4711):
        self._address = address
        self._port = port

    @final
    @property
    def session(self):
        return Minecraft.create(self._address, self._port)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


