#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/5/8 下午4:43
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
__all__ = [
    'Dbg',
    'DbgOpt'
]


from typing import Literal, Callable, Any, Optional
from functools import wraps
from warnings import warn
from traceback import format_exc
from enum import StrEnum


class DbgOpt(StrEnum):
    """
    调试选项.

    :ivar PRINT: 打印错误信息.
    :ivar IGNORE: 忽略错误.
    :ivar LOG: 记录错误.
    :ivar WARN: 警告错误.
    :ivar RAISE: 抛出错误.
    :ivar STOP: 停止程序.
    """
    PRINT = 'print'
    IGNORE = 'ignore'
    LOG = 'log'
    WARN = 'warn'
    RAISE = 'raise'
    STOP = 'stop'


class Dbg:
    """
    调试器.

    Example::

        >>> @Dbg(DbgOpt.LOG, group='test', info='test info', note='test note')
        >>> def func():
        >>>     print(1 / 0)
        >>> func()
        >>> Dbg.raiseErrorGroup()
        >>> #Error...

    Attributes:
        :ivar _option: 调试选项,可选值为'print', 'ignore', 'log', 'warn', 'raise', 'stop'.
        :ivar group: 调试组.
        :ivar info: 调试信息.
        :ivar note: 调试备注.
        :ivar fromError: 引发错误的异常.

    Methods:
        :meth:`__new__`: 单例模式.
        :meth:`__init__`: 初始化调试器.
        :meth:`__call__`: 装饰器,用于装饰函数.
        :meth:`handleError`: 处理错误.
        :meth:`_formatErrorGroup`: 将错误记录字典(dict)递归的组装成嵌套的ExceptionGroup字典.
        :meth:`raiseErrorGroup`: 引发错误组.
    """
    _instance: 'Dbg' = None

    errorLog: dict[str, list[Exception]] = {}

    @property
    def option(self) -> DbgOpt:
        """
        :return: 调试选项, 参见 DbgOption.
        """
        return self._option

    @option.setter
    def option(self, value: DbgOpt):
        self._option = value

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        cls._instance.option = DbgOpt.LOG
        cls._instance.group = 'default'
        cls._instance.info = None
        cls._instance.note = None
        cls._instance.fromError = None

        return cls._instance

    def __init__(self, option: DbgOpt = DbgOpt.LOG, *, group: str = 'default', info: Optional[str] = None, note: Optional[str] = None, fromError: Optional[Exception | type[Exception]] = None):
        """
        初始化调试器.

        :param option: 调试选项, 参见 DbgOption.
        :keyword group: 调试组.
        :keyword info: 调试信息.
        :keyword note: 调试备注.
        :keyword fromError: 引发错误的异常.
        """
        self._option = option
        self.group = group
        self.info = info
        self.note = note
        self.fromError = fromError

    def __call__(self, _fn: Callable) -> Callable:
        """
        装饰器,用于装饰函数.

        :param func: 被装饰的函数.
        :type func: Callable
        :return: 装饰后的函数.
        """
        @wraps(_fn)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return _fn(*args, **kwargs)

            except Exception as e:
                self._handleError(e, info=format_exc())

        return wrapper

    def _handleError(self, e: Exception, *, info: str) -> None:
        """
        根据调试选项处理错误.

        :param e: 错误.
        :type e: Exception
        :keyword info: 错误信息.
        :type info: str
        """
        if self.note: e.add_note(self.note)
        info = self.info or info

        match self.option:
            case DbgOpt.PRINT:
                print(f"[{self.group}]: {info}")

            case DbgOpt.IGNORE:
                pass

            case DbgOpt.LOG:
                self.errorLog.setdefault(self.group, []).append(e)

            case DbgOpt.WARN:
                warn(  # warning
                    f"[{self.group}]: {info}")

            case DbgOpt.RAISE:
                if self.fromError:
                    raise e from self.fromError
                raise e

            case DbgOpt.STOP:
                exit(f"不可恢复的错误导致程序退出: \n{info}")

    @classmethod
    def _formatErrorGroup(cls, *, _lastKey: list[str] = None, _result: list = None) -> ExceptionGroup:
        """
        将错误记录字典(dict)递归的组装成嵌套的ExceptionGroup字典.

        :keyword _lastKey: 上一个键
        :type _lastKey: list
        :keyword _result: 结果
        :type _result: list
        :return: 如果_lastKey不为空,则返回ExceptionGroup字典,否则递归的执行_formatErrorGroup函数.
        :rtype: ExceptionGroup | dict
        """
        if _lastKey is not None:
            if len(_lastKey):
                firstKey = _lastKey[0]

                _result = [firstKey, cls.errorLog[firstKey] + [ExceptionGroup(*_result)]]

                return cls._formatErrorGroup(_lastKey=_lastKey[1:], _result=_result)

            return ExceptionGroup(*_result)

        else:
            if not isinstance(list(cls.errorLog.values())[0], list):
                return ExceptionGroup(
                    "Error", [ValueError(f"[{cls.__name__}内部错误]: 类<{cls.__name__}>的错误记录字典的值必须为列表!")])

            firstKey, _lastKey = (keyList := list(cls.errorLog.keys()))[0], keyList[1:]

            _result = [firstKey, cls.errorLog[firstKey]]

            return cls._formatErrorGroup(_lastKey=_lastKey, _result=_result)

    @classmethod
    def raiseErrorGroup(cls) -> None:
        """
        引发错误组.
        """
        if cls.errorLog:
            raise cls._formatErrorGroup()


if __name__ == '__main__':
    @Dbg(DbgOpt.LOG, group='普通函数组', info='调试信息', note='可能会抛除零错?')
    def func():
        print(1 / 0)

    class Test:
        def __init__(self, x: int):
            self.x = x

        @Dbg(DbgOpt.LOG, group='类方法组', info='调试信息', note='self.x可能为0?')
        def func(self):
            if not self.x:
                raise ValueError("x不能为0")

    func()
    Test(0).func()
    print(Dbg.errorLog)
    Dbg.raiseErrorGroup()
