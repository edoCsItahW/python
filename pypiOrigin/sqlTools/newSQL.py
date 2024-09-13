#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/9/3 下午11:16
# 当前项目名: ansiDefine.py
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from pymysql.cursors import Cursor
from functools import wraps
from functools import partial, singledispatch
from tabulate import tabulate
from warnings import warn
from pymysql import Error, connect, Connection
from typing import Callable, final, Self, TypedDict, Protocol, Any, Optional, Literal, NoReturn, Final
from string import ascii_uppercase
from random import choice, randint
from types import FunctionType as function, TracebackType
from time import time
from abc import ABC, abstractmethod
from typeSup import *


class _funcWarp:
    """
    单分发器.

    Attributes:
        :ivar _func: 被装饰的函数.
        :ivar _rulesDict: 规则字典.
        :ivar _pos: 进行对比的参数位置.

    Methods:
        _checkRule: 验证规则.

        register: 注册规则.

        __call__: 执行函数.
    """

    def __init__(self, func: Callable):
        self._func = func
        self._rulesDict: dict[Callable, Callable] = {}
        self._pos: Optional[int | str] = None

    @staticmethod
    def _checkRule(value: Any, _type: type) -> Callable[[Any], bool]:
        if isinstance(value, type):
            raise ValueError(
                f"参数'{value}'不能是类型,如要验证类型,请使用'_type'参数!")

        if _type is None and value is not None:
            return lambda x: x == value

        elif _type is not None and value is None:
            # 如果_type传入了type,则验证规则为有值即可
            if _type == type: return lambda x: True

            return lambda x: isinstance(x, _type)

        else:
            return lambda x: x is None

    def register(self, pos: int | str = 0, *, value: Optional[Any] = None, type_: Optional[type] = None):
        if pos is not None:
            if self._pos is not None and self._pos != pos:
                raise ValueError(
                    f"进行对比的参数位置不一致: '{self._pos}'和'{pos}'冲突!")

            else:
                self._pos = pos

        def getFunc(func: Callable):
            wraps(func)

            self._rulesDict[self._checkRule(value, type_)] = func

        return getFunc

    def __call__(self, *args, **kwargs):
        for rule, func in self._rulesDict.items():
            if rule(args[self._pos] if isinstance(self._pos, int) else kwargs[self._pos]):
                return func(*args, **kwargs)

        return self._func(*args, **kwargs)


def GsingleDispatch(func: Callable) -> _funcWarp:
    """
    广义单分发器.

    Example::

        对比函数传入的参数中的第一个参数的值::

            >>> @GsingleDispatch
            >>> def func(x: int, y: int):
            >>>     return x + y
            >>>
            >>> # 对比函数传入的参数中的第一个参数的值
            >>> @func.register(0, value=1)
            >>> def _(x: int, y: int):
            >>>     return x - y
            >>>
            >>> @func.register(0, value=2)
            >>> def _(x: int, y: int):
            >>>     return x * y
            >>>
            >>> func(1, 2)
            1
            >>> func(1, 3)
            2
            >>> func(2, 2)

        对比函数传入的参数中的第一个参数的类型::

            >>> # 对比函数传入的参数中的第一个参数的类型
            >>> @GsingleDispatch
            >>> def func(x: int, y: int):
            >>>     return x + y
            >>>
            >>> @func.register(0, Type=int)
            >>> def _(x: int, y: int):
            >>>     return x - y
            >>>
            >>> @func.register(0, Type=str)
            >>> def _(x: str, y: int):
            >>>     return x + str(y)
            >>>
            >>> func(1, 2)
            1
            >>> func("1", 2)
            '12'
            >>> func(1, 3)
            -2
            >>> func("1", 3)

    :param func: 被装饰的函数.
    :return: _funcWarp实例.
    """
    wraps(func)
    return _funcWarp(func)


def stderr(msg: str) -> None:
    print(f"\033[31m{msg}\033[0m")


def stdout(msg: str, *, allow: bool = True, **kwargs) -> None:
    if allow:
        print(msg, **kwargs)


@final
class Feedback:
    """
    定义反馈类,用于处理mysql的反馈信息.
    """

    @staticmethod
    def normal(rowcount: int, *, spendtime: float = 0.00) -> str:
        return f"{rowcount} row{'s' if rowcount != 1 else ''} in set ({spendtime:.3f} sec)"

    @staticmethod
    def query(rowcount: int, *, spendtime: float = 0.00) -> str:
        return f"Query OK, {rowcount} rows affected ({spendtime:.3f} sec)"

    @staticmethod
    def empty(*, spendtime: float = 0.00) -> str:
        return f"Empty set ({spendtime:.3f} sec)"

    @staticmethod
    def alter(rowcount: int) -> str:
        return f"Records: {rowcount}  Duplicates: 0  Warnings: 0"

    @staticmethod
    def useDb() -> str:
        return "Database changed"


def result(res: Result, fbFn: Callable[..., str] | function = None) -> Callable[..., Any]:
    def getfunc(fn: Callable) -> Callable:
        @wraps(fn)
        def warp(*_args, **_kwargs) -> Any:
            start = time()

            try:
                _ = fn(*_args, **_kwargs)

            except Error as e:
                stderr(
                    f"ERROR {e.args[0]} ({''.join(str(r if (r := randint(0, 9)) % 2 else choice(ascii_uppercase)) for _ in range(5))}): {e.args[1]}")

            except Exception as e:
                raise e from RuntimeError

            else:
                res['spendtime'] = time() - start

                if res['result'].__len__():
                    print(tabulate(res["result"], headers=res["header"] or (), tablefmt="grid"))

                if fbFn:
                    print(fbFn(
                        *[r for i in fbFn.__code__.co_varnames[:fbFn.__code__.co_argcount] if
                          (r := res.get(i)) or r == 0],
                        **{k: r for k in fbFn.__code__.co_varnames[fbFn.__code__.co_argcount:] if
                           (r := res.get(k)) or r == 0}
                    ))

                return _
            finally:
                for k in res:
                    res.setdefault(k, None)

        return warp

    return getfunc


@GsingleDispatch
def remap(data: dict, mapping: dict[str, str | tuple[str, str]], *, default: Any = '') -> NoReturn:
    raise NotImplementedError(
        f"Type {type(data)} is not supported")


@remap.register(0, type_=None)
def _(data: None, mapping: dict[str, str | tuple[str, str]], *, default: CanBeStr = '') -> dict[str, CanBeStr]:
    return { k: default for k in mapping}


@remap.register(0, type_=dict)
def _(data: dict, mapping: dict[str, str | tuple[str, str]], *, default: CanBeStr = '') -> dict[str, CanBeStr]:
    return {k: (
        (
            (
                f" {mapping[k][0]} {mapping[k][1]}"
                if isinstance(mapping[k], tuple) and len(mapping[k]) >= 2 else  #
                " " + mapping[k]
            )
            if r else  #
            default
        )
        if isinstance(r, bool) else  #
        (
            f" {mapping[k][0]} {r}"
            if isinstance(mapping[k], tuple) and len(mapping[k]) >= 2 else  #
            r
        )
    )
    if (r := data.get(k)) else  #
    default
            for k in mapping}


def execute(conn: Connection, cur: Cursor, res: Result, cmd: str, *, allow: bool = True) -> None:
    stdout(cmd + ('' if cmd.endswith(';') else ';'), allow=allow) if allow else ...

    cur.execute(cmd)

    ... if conn.get_autocommit() else conn.commit()

    res['result'] = cur.fetchall()

    if cur.description: res['header'] = [i[0] for i in cur.description]

    res['rowcount'] = cur.rowcount


FlagOrStr = Optional[bool | str | None]


class Database:
    instance: Self = None
    _res: Result = {'header': None, 'result': None, 'rowcount': None}

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self, conn: Connection, cur: Cursor, database: Optional[str] = None, *, table: str = None):
        self._conn = conn
        self._cur = cur
        self.table = table
        self.database = database
        self._execute: Callable[[str], None] = partial(execute, conn, cur, self._res)

    @result(_res, Feedback.normal)
    def show(self):
        self._execute("SHOW DATABASES")

    @result(_res, Feedback.useDb)
    def use(self, database: str = None):
        database = database or self.database

        self._execute(f"USE {database}")

        self.database = database

    @result(_res, Feedback.query)
    def create(self, dbName: str, *, cfg: DBCreateCfg = None, exists: FlagOrStr | Literal['IF NOT EXISTS'] = False,
               charset: FlagOrStr = None, collate: FlagOrStr = None):
        cfg = remap({
            **(cfg or {}),
            'exists':  exists,
            'charset': charset,
            'collate': collate
        },
            {
                'exists':  "IF NOT EXISTS",
                'charset': ('CHARACTER SET', 'utf8mb4'),
                'collate': ('COLLATE', 'utf8mb4_unicode_ci')
            })

        self._execute(f"CREATE DATABASE{cfg['exists']} {dbName}{cfg['charset']}{cfg['collate']}")

    @result(_res, Feedback.query)
    def drop(self, dbName: str, *, cfg: DBDropCfg = None, exists: FlagOrStr | Literal['IF EXISTS'] = False):
        cfg = remap({**(cfg or {}), 'exists': exists}, {'exists': "IF EXISTS"})

        self._execute(f"DROP DATABASE {dbName}{cfg['exists']}")


class ArgumentError(Exception):
    def __init__(self, *args):
        super().__init__(*args or ("Invalid arguments",))


class Table:
    instance: Self = None
    _res: Result = {'header': None, 'result': None, 'rowcount': None}

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self, conn: Connection, cur: Cursor, *, table: str = None):
        self._conn = conn
        self._cur = cur
        self._table = table
        self._execute: Callable[[str], None] = partial(execute, conn, cur, self._res)

    @property
    def table(self):
        if not self._table:
            raise ValueError(
                "'table' is not defined") from ArgumentError

        return self._table

    @table.setter
    def table(self, value: str):
        self._table = value

    @result(_res, Feedback.normal)
    def describe(self):
        self._execute(f"DESCRIBE {self.table}")

    @result(_res, Feedback.query)
    def create(self, tbName: str, **kwargs):
        ...


class MySQL:
    _instance: Self = None

    def __new__(cls, *args, **kwargs) -> 'MySQL':
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, user: str, password: str, database: Optional[str] = None, *, host: str = 'localhost',
                 table: str = None, **kwargs) -> None:
        self._database = database
        self._connect = connect(host=host, user=user, password=password, database=database, **kwargs)
        self._cursor = self._connect.cursor()
        self._table = table

    def __enter__(self) -> Self:
        self._connect.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb: TracebackType) -> None:
        self._cursor.close()
        self._connect.close()

        if any((exc_type, exc_val, exc_tb)):
            warn(  # 退出上下文异常
                f"Exception occurred: {exc_type}({exc_val}), line {exc_tb.tb_lineno}")

    @property
    def db(self) -> Database:
        if not Database.instance:
            return Database(self._connect, self._cursor, self._database, table=self._table)

        if self._table:
            Database.instance.table = self._table

        if self._database:
            Database.instance.database = self._database

        return Database.instance

    @property
    def tb(self) -> Table:
        if not Table.instance:
            return Table(self._connect, self._cursor, table=self._table)

        if self._table:
            Table.instance.table = self._table

        return Table.instance

    @property
    def database(self) -> str:
        return self._database

    @database.setter
    def database(self, value: str) -> None:
        self._database = value

        if Database.instance:
            Database.instance.database = value

        else:
            warn(
                "Database instance not found, please create a new instance.")

    @property
    def table(self) -> str:
        return self._table

    @table.setter
    def table(self, value: str) -> None:
        self._table = value

        if Database.instance:
            Database.instance.tbName = value

        else:
            warn(
                "Database instance not found, please create a new instance.")


if __name__ == '__main__':
    # 1. tuple[tuple[], ...]
    mysql = MySQL('root', '135246qq', 'mysql', table='db', autocommit=True)
    mysql.db.show()
