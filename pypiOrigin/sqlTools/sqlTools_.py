#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/3 下午11:16
# 当前项目名: pypiOrigin
# 编码模式: utf-8
# 注释: MySQL数据库操作工具类.
# pip install -i https://test.pypi.org/simple/ sqlTools
# -------------------------<edocsitahw>----------------------------

__all__ = [
    'Type',
    'ArgumentError',
    'Result',
    'Field',
    'DB',
    'Database',
    'TB',
    'Table',
    'MySQL',
    'py2sql'
]

from pymysql.cursors import Cursor
from functools import wraps
from functools import partial, singledispatch, cached_property, cache
from tabulate import tabulate
from warnings import warn
from pymysql import Error, connect, Connection, NULL
from typing import Callable, final, Self, TypedDict, Protocol, Any, Optional, Literal, NoReturn, Final, overload, Collection, Iterator
from string import ascii_uppercase
from random import choice, randint
from types import FunctionType as function, TracebackType
from time import time
# from typeSup import Type, Result, ArgumentError
from enum import Enum
from re import findall
from abc import ABC
from subprocess import Popen, PIPE
from pandas import Series, DataFrame
from inspect import currentframe, signature
from csv import reader, writer

# TODO: 改善仿位掩码类引用方式过长问题.
# TODO: 使仿位掩码类和SQL语句执行器尽量遵循开发封闭原则(针对新字段).

SERVER_NAME = 'MySQL80'
OUTPUT = True


class Result(TypedDict):
    result: tuple[tuple[Any, ...], ...]
    header: list[str] | tuple
    rowcount: int
    spendtime: Optional[float]


class Type(Enum):
    VARCHAR = "varchar"
    INT = "int"
    CHAR = "char"
    DATE = "date"
    FLOAT = "float"
    TIME = "time"
    BOOLEAN = "boolean"


FlagOrStr = Optional[bool | str | None]


class CanBeStr(Protocol):
    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...


class ArgumentError(Exception):
    def __init__(self, *args):
        super().__init__(*args or ("Invalid arguments",))


@lambda _: _()
def feasibleTest() -> None:
    _ = lambda cmd: tuple(getattr(Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE), i).read().decode("gbk", errors='ignore') for i in ["stdout", "stderr"])

    r, e = _("mysql --version")
    if e:
        raise EnvironmentError(  # mysql未安装
            f"MySQL not found: {e}") from RuntimeError("Feasible test failed")
    else:
        print(f"Using {r.strip()}")

    t = [None] * 2
    for i in ('MySQL', SERVER_NAME):
        t[0], t[1] = (_r := _(f"sc query {i}"))[0] or t[0], _r[1] or t[1]
    else:
        if not t[0]:
            raise EnvironmentError(  # 服务未启动
                f"MySQL service not found: {t[1]}") from RuntimeError("Feasible test failed")


del feasibleTest


def stderr(msg: str) -> None:
    print(f"\033[31m{msg}\033[0m")


def stdout(msg: str, *, allow: bool = True, **kwargs) -> None:
    if allow and OUTPUT:
        print(msg, **kwargs)


@final
class Feedback:
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
                stderr(  # 输出错误信息
                    f"ERROR {e.args[0]} ({''.join(str(r if (r := randint(0, 9)) % 2 else choice(ascii_uppercase)) for _ in range(5))}): {e.args[1]}")

            except Exception as e:
                raise e from RuntimeError(  # 结果处理失败
                    "Result processing failed")

            else:
                res['spendtime'] = time() - start

                if res['result'].__len__():
                    stdout(tabulate(res["result"], headers=res["header"] or (), tablefmt="grid"))

                if fbFn:
                    stdout(fbFn(
                        *[r for i in fbFn.__code__.co_varnames[:fbFn.__code__.co_argcount] if (r := res.get(i)) or r == 0],
                        **{k: r for k in fbFn.__code__.co_varnames[fbFn.__code__.co_argcount:] if (r := res.get(k)) or r == 0}
                    ) + '\n')

                return _
            finally:
                for k in res:
                    res.setdefault(k, None)

        return warp

    return getfunc


def remap(_format: str, mapping: Optional[dict[str, str]], **kwargs: str) -> str:
    needKeys = findall(r"(?<=\{)\w+(?=})", _format)

    mapping = (mapping.result if isinstance(mapping, Field) else mapping) or {}

    mapping = {k: mapping.get(k, '') for k in needKeys}

    return _format.format_map(mapping | kwargs)


def execute(conn: Connection, cur: Cursor, res: Result, cmd: str, *, allow: bool = True) -> None:
    stdout(cmd + ('' if cmd.endswith(';') else ';'), allow=allow) if allow else ...

    cur.execute(cmd)

    ... if conn.get_autocommit() else conn.commit()

    res['result'] = cur.fetchall()
    if cur.description: res['header'] = [i[0] for i in cur.description]
    res['rowcount'] = cur.rowcount


class Field:
    def __init__(self, key: str, default: Optional[str | int | Type | tuple[Any, Any]], *, handle: Callable[[str], str] = lambda x: f" {x}", required: list[str] = None, err: bool = False):
        self._key, self._default, self._handle, self._required, self._err = key, default, handle, required, err
        self._value = None
        self._flag = True
        self._related: Optional[Field] = None
        self._mapping: Optional[dict[str, str]] = None

    @property
    def value(self) -> str:
        res = v if (v := self._value) is not None else self._default

        if not any((self._value is not None, self._default)):
            if self._err:
                raise ValueError(  # 值为空且为必填字段
                    f"Field '{self._key}' is required!") from ArgumentError

            else:
                warn(  # 值为空且为非必填字段,但不排除有默认值
                    f"Field '{self._key}' is not recommended for automatic processing!", SyntaxWarning)

            if self._related and self._mapping:
                res = self._mapping.get(self._related.value)

        return res.value if isinstance(res, Enum) else res

    @property
    def result(self) -> dict[str, str]:
        return {self._key: self.__str__()}

    def __str__(self) -> str:
        if self._flag:
            return self._handle(self.value) if self._handle else self.value

        return ''

    def __or__(self, other: Self | dict[str, str]) -> dict[str, str]:
        if isinstance(other, dict): return self.result | other

        res = self.result | other.result

        self._value, self._flag = None, True  # 重置用户输入

        return res

    def __ror__(self, other: Self | dict[str, str]) -> dict[str, str]:
        if isinstance(other, dict): return other | self.result

        res = other.result | self.result

        self._value, self._flag = None, True  # 重置用户输入

        return res

    def __call__(self, value: str | bool | None | Type) -> Self:
        if self._required and value not in self._required:
            raise ArgumentError(
                f"Invalid value for field: 'value', must be one of: {', '.join(self._required)}")

        if value is not None and not isinstance(value, bool):
            self._value = value

        elif value is None:
            self._flag = False

        return self

    def related(self, other: Self, **kwargs: str) -> None:
        """关联字段"""
        self._related, self._mapping = other, kwargs


class Base(ABC):
    instance: Self = None
    _res: Result = {'header': None, 'result': None, 'rowcount': None}

    @final
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance


class DB:
    @final
    class Create(ABC):
        EXISTS = Field('exists', 'IF NOT EXISTS', required=['IF NOT EXISTS'])
        CHARSET = Field('charset', 'utf8mb4', handle=lambda x: f" CHARACTER SET {x}")
        COLLATE = Field('collate', 'utf8mb4_general_ci', handle=lambda x: f" COLLATE {x}")

    @final
    class Drop(ABC):
        EXISTS = Field('exists', 'IF EXISTS', required=['IF EXISTS'])


class Database(Base):
    def __init__(self, conn: Connection, cur: Cursor, database: Optional[str] = None, *, table: str = None):
        self._conn = conn
        self._cur = cur
        self.table = table
        self.database = database
        self._execute: Callable[[str], None] = partial(execute, conn, cur, self._res)

    @result(Base._res, Feedback.normal)
    def show(self) -> None:
        """显示数据库列表"""
        self._execute("SHOW DATABASES")

    @result(Base._res, Feedback.useDb)
    def use(self, database: str = None) -> None:
        """切换数据库"""
        database = database or self.database

        self._execute(f"USE {database}")

        self.database = database

    @result(Base._res, Feedback.query)
    def create(self, dbName: str, *, cfg: Field | dict[str, str | bool | None | Type] = None, autoUse: bool = True) -> None:
        self._execute(remap("CREATE DATABASE{exists} {dbName}{charset}{collate}", cfg, dbName=dbName))

        if autoUse:
            self.database = dbName
            self.use()

    @result(Base._res, Feedback.query)
    def drop(self, dbName: str, *, cfg: Field | dict[str, str | bool | None | Type] = None):
        self._execute(remap("DROP DATABASE {dbName}{exists}", cfg, dbName=dbName))


# @singledispatch
# def py2sql(data: Any) -> None:
#     raise NotImplementedError(
#         f"Unsupported type: {type(data)}")
#
#
# @py2sql.register(str)
# def _(data: str) -> str:
#     return f"'{data}'"
#
#
# @py2sql.register(bool)
# def _(data: bool) -> str:
#     return 'TRUE' if data else 'FALSE'
#
#
# @py2sql.register(int)
# def _(data: int) -> str:
#     return str(data)
#
#
# @py2sql.register(float)
# def _(data: float) -> str:
#     return str(data)
def py2sql(data: Any) -> Any:
    if isinstance(data, str):
        return f"'{data}'"

    elif isinstance(data, bool):
        return 'TRUE' if data else 'FALSE'

    elif isinstance(data, int):
        return str(data)

    elif isinstance(data, float):
        return str(data)

    elif data is None:
        return NULL

    raise NotImplementedError(  # 未实现类型
        f"Unsupported type: {type(data).__name__}")


class TB:
    @final
    class Create(ABC):
        TYPE = Field('type', 'int')
        LENGHT = Field('lenght', None, handle=lambda x: f"({x})" if x else '')
        LENGHT.related(TYPE, int='', varchar='128', char='255', date='', float='', time='', boolean='')
        NULL = Field('null', 'NOT NULL', required=['NOT NULL'])
        DEFAULT = Field('default', None, err=True)
        AUTO_INCREMENT = Field('autoIncrement', 'AUTO_INCREMENT', required=['AUTO_INCREMENT'])
        PRIMARY_KEY = Field('primaryKey', 'PRIMARY KEY', required=['PRIMARY KEY'])
        ENGINE = Field('engine', 'InnoDB', handle=lambda x: f" ENGINE={x}")
        CHARSET = Field('charset', 'utf8', handle=lambda x: f" DEFAULT CHARSET={x}")
        EXISTS = Field('exists', 'IF NOT EXISTS', required=['IF NOT EXISTS'])
        FOREIGN_KEY = Field('foreignKey', None, handle=lambda x: f" FOREIGN KEY ({x})", err=True)
        REFERENCES = Field('references', None, handle=lambda x: f" REFERENCES {x}", err=True)

    @final
    class Drop(ABC):
        EXISTS = Field('exists', 'IF EXISTS', required=['IF EXISTS'])

    @final
    class Select(ABC):
        WHERE = Field('where', None, handle=lambda x: f" WHERE {x}", err=True)
        ORDER = Field('order', None, handle=lambda x: f" ORDER BY {x}", err=True)
        LIMIT = Field('limit', 1, handle=lambda x: f" LIMIT {x}", err=True)
        INNER = Field('inner', None, handle=lambda x: f" INNER JOIN {x[0]} ON {x[1]}", err=True)
        OFFSET = Field('offset', None, handle=lambda x: f" OFFSET {x}", err=True)
        LEFT = Field('left', None, handle=lambda x: f" LEFT JOIN {x[0]} ON {x[1]}", err=True)

    @final
    class Update(ABC):
        WHERE = Field('where', None, handle=lambda x: f" WHERE {x}", err=True)

    @final
    class Alter(ABC):
        DROP = Field('drop', None, handle=lambda x: f" DROP {x}", err=True)

    @final
    class Delete(ABC):
        WHERE = Field('where', None, handle=lambda x: f" WHERE {x}", err=True)


class Table(Base):
    class _field:
        __res = "CREATE TABLE{exists} {tableName}($\n){engine}{charset}"

        def __init__(self, ins: 'Table', name: str, *, cfg: Field | dict[str, str | bool | None | Type] = None):
            self._ins, self._name, self._cfg = ins, name, cfg
            self._count = 0
            self._inner = ""

        def addField(self, name: str, *, cfg: Field | dict[str, str | bool | None | Type] = None) -> Self:
            self._inner += remap("\n\t{name}{type}{lenght}{null}{default}{autoIncrement}{primaryKey},", cfg, name=name)

            return self

        def config(self, cfg: Field | dict[str, str | bool | None | Type] = None) -> Self:
            if self._count >= 1: raise RuntimeError(  # 超过配置次数
                "Cannot have more than one config!")

            if cfg:
                self._inner += remap("\n\t{primaryKey}{foreignKey}{references} ", cfg)

            self._count += 1

            return self

        def end(self, cfg: Field | dict[str, str | bool | None | Type] = None) -> None:
            cfg = (cfg or {} | self._cfg) if self._cfg else cfg

            self.__res = remap(self.__res, cfg, tableName=self._name)
            self.__res = self.__res.replace("$", self._inner[:-1])
            self._ins._exec(self.__res)

        def __call__(self, cfg: Field | dict[str, str | bool | None | Type] = None) -> None:
            self.end(cfg)

    class _series:
        _ins: 'Table'

        def __new__(cls, *args, **kwargs):
            cls._ins = kwargs.get('ins')
            return super().__new__(cls)

        def __init__(self, data: tuple[Any, ...], *, columns: list[str], **kwargs):
            # TODO: 实现响应式数据
            self.__dict__['_data'] = self._data = data
            self.__dict__['_columns'] = self._columns = columns
            self.__dict__['_map'] = self._map = {k: v for k, v in zip(columns, data)}

        def __getitem__(self, item: str):
            return self._map[item]

        def __getattr__(self, item: str):
            if item not in self.__dir__():
                return self[item]

            return super().__getattribute__(item)

        def __iter__(self):
            return iter(self._data)

        def __setitem__(self, key: str, value: Any) -> None:
            self._ins.update(**{key: value}, cfg=TB.Update.WHERE(" and ".join(f'{k}={py2sql(v)}' for k, v in self._map.items())))

        def __setattr__(self, key: str, value: Any) -> None:
            if key not in self.__dir__():
                self[key] = value
            else:
                super().__setattr__(key, value)

        def __del__(self):
            self._ins.delete(cfg=TB.Delete.WHERE(" and ".join(f'{k}={py2sql(v)}' for k, v in self._map.items())))

        def __repr__(self):
            return f"<Series[{', '.join(f'{k}: {py2sql(v)}' for k, v in self._map.items())}]>"

    def __init__(self, conn: Connection, cur: Cursor, *, table: str = None) -> None:
        self._conn = conn
        self._cur = cur
        self._table = table
        self._execute: Callable[[str], None] = partial(execute, conn, cur, self._res)
        self._idx = 0

    @cached_property
    def content(self) -> tuple[tuple[Any, ...], ...]:
        if self._res['result'] is None:
            self.select()
        return self._res['result']

    def __getitem__(self, item: str | int) -> tuple[Any, ...] | _series:
        if isinstance(item, str):
            return self.select(item)
        elif isinstance(item, int):
            return self._series(self.content[item], columns=self._res['header'], ins=self)
        raise TypeError(  # 类型错误
            f"Unsupported type: {type(item).__name__}")

    def __getattr__(self, item: str) -> tuple[Any, ...]:
        if item not in self.__dir__():
            return self[item]

        return super().__getattribute__(item)

    def __delitem__(self, key: int) -> None:
        self.delete(cfg=TB.Delete.WHERE(" and ".join(f'{k}={py2sql(v)}' for k, v in self.content)))

    def __iter__(self):
        return self

    def __next__(self) -> _series:
        if self._idx >= len(self.content):
            self._idx = 0
            raise StopIteration

        data = self._res['result'][self._idx]
        self._idx += 1

        return self._series(data, columns=self._res['header'], ins=self)

    @property
    def table(self) -> str:
        if not self._table:
            raise ValueError(  # 未定义表名
                "'table' is not defined") from ArgumentError

        return self._table

    @table.setter
    def table(self, value: str) -> None:
        self._table = value

    @result(Base._res, Feedback.query)
    def _exec(self, cmd: str) -> None:
        self._execute(cmd)

    @result(Base._res, Feedback.query)
    def show(self) -> None:
        self._execute(f"SHOW TABLES")

    @result(Base._res, Feedback.normal)
    def describe(self) -> None:
        self._execute(f"DESCRIBE {self.table}")

    def create(self, tbName: str, *, cfg: Field | dict[str, str | bool | None | Type] = None, autoUse: bool = True) -> _field:
        if autoUse:
            self._table = tbName

        return self._field(self, tbName, cfg=cfg)

    @result(Base._res, Feedback.query)
    def drop(self, tbName: str, *, cfg: Field | dict[str, str | bool | None | Type] = None) -> None:
        self._execute(remap("DROP TABLE{exists} {tbName}", cfg, tbName=tbName))

    @result(Base._res, Feedback.query)
    def insert(self, **data: Any) -> None:
        self._execute(f"INSERT INTO {self.table} ({', '.join(data.keys())}) VALUES ({', '.join(map(py2sql, data.values()))})")

    @result(Base._res, Feedback.query)
    def select(self, *fields: str, cfg: Field | dict[str, str | bool | None | Type] = None, tbName: str = None) -> tuple[tuple[Any, ...], ...]:
        fields = fields or '*'

        self._execute(remap("SELECT {fields} FROM {table}{left}{where}{order}{inner}{on}{limit}{offset}", cfg, fields=', '.join(fields), table=tbName or self._table))
        return self._res['result']

    @result(Base._res, Feedback.query)
    def update(self, *, cfg: Field | dict[str, str | bool | None | Type] = None, **data: Any) -> None:
        self._execute(remap(f"UPDATE {self.table} SET {', '.join(map(lambda x: f'{x[0]}={py2sql(x[1])}', data.items()))}{{where}}", cfg))

    @result(Base._res, Feedback.query)
    def alter(self, tbName: str = None, *, cfg: Field | dict[str, str | bool | None | Type] = None) -> None:
        tbName = tbName or self._table
        self._execute(remap("ALTER TABLE {tbName}{drop}", cfg, tbName=tbName))

    @result(Base._res, Feedback.query)
    def delete(self, *, cfg: Field | dict[str, str | bool | None | Type] = None) -> None:
        self._execute(remap(f"DELETE FROM {self.table}{{where}}", cfg))

    def toDataFrame(self) -> DataFrame:
        return DataFrame(self.select(), columns=self._res['header'])

    def toCSV(self, csvPath: str) -> None:
        with open(csvPath, 'w', encoding='gbk', newline='') as file:
            data = self.select()
            (w := writer(file)).writerow(self._res['header'])
            w.writerows(data)

    def fromCSV(self, csvPath: str) -> None:
        warn("Not implemented yet.", DeprecationWarning)
        with open(csvPath, 'r', encoding='gbk') as file:
            print(list(reader(file)))


class MySQL(Base):
    def __init__(self, user: str, password: str, database: Optional[str] = None, *, host: str = 'localhost', table: str = None, **kwargs) -> None:
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
                f"Exception occurred: {exc_type.__name__}({exc_val}), line {exc_tb.tb_lineno}")

    def __getattr__(self, item: str) -> Any:
        if item not in self.__dir__():
            return getattr(self._connect, item)

        super().__getattribute__(item)

    @cached_property
    def db(self) -> Database:
        if not Database.instance:
            return Database(self._connect, self._cursor, self._database, table=self._table)

        if self._table:
            Database.instance.table = self._table

        if self._database:
            Database.instance.database = self._database

        return Database.instance

    @cached_property
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


# PASSWORD = ''
# if __name__ == '__main__':
#     with MySQL('root', PASSWORD) as mysql:
#         mysql.db.create('test', cfg=DB.Create.EXISTS, autoUse=True)
#
#         mysql.tb.create('users', autoUse=True).addField('id', cfg=TB.Create.TYPE | TB.Create.PRIMARY_KEY | TB.Create.AUTO_INCREMENT)  \
#             .addField('name', cfg=TB.Create.TYPE(Type.VARCHAR) | TB.Create.LENGHT(255) | TB.Create.NULL)                                      \
#             .addField('age', cfg=TB.Create.TYPE | TB.Create.NULL)                                                                             \
#             .addField('email', cfg=TB.Create.TYPE(Type.VARCHAR) | TB.Create.LENGHT(255) | TB.Create.NULL)                                     \
#             .end()
#
#         mysql.tb.create('orders').addField('id', cfg=TB.Create.TYPE | TB.Create.PRIMARY_KEY | TB.Create.AUTO_INCREMENT)                       \
#             .addField('user_id', cfg=TB.Create.TYPE | TB.Create.NULL)                                                                         \
#             .addField('sum', cfg=TB.Create.TYPE | TB.Create.NULL)                                                                             \
#             .addField('date', cfg=TB.Create.TYPE(Type.DATE) | TB.Create.NULL)                                                                 \
#             .config(TB.Create.FOREIGN_KEY('user_id') | TB.Create.REFERENCES('users(id)'))                                                           \
#             .end()
#
#         mysql.tb.table = 'users'
#
#         mysql.tb.insert(name='Bob', age=18, email='bob@example.com')
#
#         mysql.tb.select()
#
#         mysql.tb.table = 'orders'
#
#         mysql.tb.insert(user_id=1, sum=100, date='2022-01-01')
#
#         mysql.tb.table = 'users'
#
#         for user in mysql.tb:
#             print(f"name: {user.name}, orderCount: {len(mysql.tb.select(tbName='orders', cfg=TB.Select.WHERE(f'user_id={user.id}')))}")
#
#         mysql.tb.select(cfg=TB.Select.LEFT(('orders', 'orders.user_id=users.id')))

