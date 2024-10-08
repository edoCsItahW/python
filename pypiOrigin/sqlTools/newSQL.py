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
from pymysql.cursors import Cursor
from functools import wraps
from functools import partial, singledispatch, cached_property
from tabulate import tabulate
from warnings import warn
from pymysql import Error, connect, Connection
from typing import Callable, final, Self, TypedDict, Protocol, Any, Optional, Literal, NoReturn, Final, overload
from string import ascii_uppercase
from random import choice, randint
from types import FunctionType as function, TracebackType
from time import time
from typeSup import *
from enum import Enum
from re import findall
from abc import ABC
from subprocess import Popen, PIPE

# TODO: 改善仿位掩码类引用方式过长问题.

SERVER_NAME = 'MySQL80'


@lambda _: _()
def feasibleTest() -> None:
    """ 先行测试,检查mysql是否安装以及服务是否启动. """
    # TODO: 添加对pymysql, tabulate的安装检查.
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

    del _, r, e, t, _r


del feasibleTest


def stderr(msg: str) -> None:
    """错误着色"""
    print(f"\033[31m{msg}\033[0m")


def stdout(msg: str, *, allow: bool = True, **kwargs) -> None:
    """
    输出信息

    :param msg: 输出信息
    :param allow: 是否允许输出
    :keyword kwargs: 其他print函数参数
    """
    if allow:
        print(msg, **kwargs)


@final
class Feedback:
    """
    反馈类,用于处理mysql的反馈信息.

    Note::
        该类的类方法中的参数名皆注册于Base类中.
    """
    @staticmethod
    def normal(rowcount: int, *, spendtime: float = 0.00) -> str:
        """
        输出表类型信息.

	@warning xxx

        :param rowcount: 行数
        :keyword spendtime: 耗时
        :return: 表类型信息
        """
        return f"{rowcount} row{'s' if rowcount != 1 else ''} in set ({spendtime:.3f} sec)"

    @staticmethod
    def query(rowcount: int, *, spendtime: float = 0.00) -> str:
        """ 输出查询信息. """
        return f"Query OK, {rowcount} rows affected ({spendtime:.3f} sec)"

    @staticmethod
    def empty(*, spendtime: float = 0.00) -> str:
        """ 输出空结果信息. """
        return f"Empty set ({spendtime:.3f} sec)"

    @staticmethod
    def alter(rowcount: int) -> str:
        """ 输出修改信息. """
        return f"Records: {rowcount}  Duplicates: 0  Warnings: 0"

    @staticmethod
    def useDb() -> str:
        """ 输出切换数据库信息. """
        return "Database changed"


def result(res: Result, fbFn: Callable[..., str] | function = None) -> Callable[..., Any]:
    """
    结果处理装饰器.

    :param res: 结果字典
    :type res: {'header': list[str],'result': list[list[Any]], 'rowcount': int,'spendtime': float}
    :param fbFn: 反馈函数,默认为None,即不输出反馈信息.
    :return: 装饰器
    """
    def getfunc(fn: Callable) -> Callable:
        @wraps(fn)
        def warp(*_args, **_kwargs) -> Any:
            """
            :raise RuntimeError: 结果处理失败
            """
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
                    print(tabulate(res["result"], headers=res["header"] or (), tablefmt="grid"))

                if fbFn:
                    print(fbFn(
                        *[r for i in fbFn.__code__.co_varnames[:fbFn.__code__.co_argcount] if (r := res.get(i)) or r == 0],
                        **{k: r for k in fbFn.__code__.co_varnames[fbFn.__code__.co_argcount:] if (r := res.get(k)) or r == 0}
                    ) + '\n')

                return _
            finally:
                for k in res:
                    res.setdefault(k, None)

        return warp

    return getfunc


def remap(_format: str, mapping: dict[str, str], **kwargs: str) -> str:
    """
    格式化字符串,生成sql语句.

    :param _format: 格式化字符串
    :param mapping: 映射字典
    :keyword kwargs: 特化参数
    :return: 格式化后的sql语句
    """
    needKeys = findall(r"(?<=\{)\w+(?=})", _format)

    mapping = (mapping.result if isinstance(mapping, Field) else mapping) or {}

    mapping = {k: mapping.get(k, '') for k in needKeys}

    return _format.format_map(mapping | kwargs)


def execute(conn: Connection, cur: Cursor, res: Result, cmd: str, *, allow: bool = True) -> None:
    """
    执行sql语句.

    :param conn: sql连接对象
    :param cur: sql游标对象
    :param res: 结果字典
    :param cmd: sql语句
    :keyword allow: 是否允许输出
    """
    stdout(cmd + ('' if cmd.endswith(';') else ';'), allow=allow) if allow else ...

    cur.execute(cmd)

    ... if conn.get_autocommit() else conn.commit()

    res['result'] = cur.fetchall()
    if cur.description: res['header'] = [i[0] for i in cur.description]
    res['rowcount'] = cur.rowcount


class Field:
    """
    字段类,通过仿位掩码类,实现自动处理.

    TODO: 实现嵌套Field功能,如: where(condition1 | and | condition2) | order(desc)

    Example::
        >>> # Usage:
        >>> charset = Field('charset', 'utf8mb4', handle=lambda x: f" CHARACTER SET {x}")('utf8mb4')
        >>> null = Field('null', 'NOT NULL', required=['NOT NULL', ''])
        >>> charset | null
        {'charset': 'CHARACTER SET utf8mb4', 'null': 'NOT NULL'}

        >>> # 赋值:
        >>> charset('gbk') | null
        {'charset': 'CHARACTER SET gbk', 'null': 'NOT NULL'}

        >>> # 多值:
        >>> join = Field('join', None, handle=lambda x: f" JOIN {x[0]} ON {x[1]}", err=True)
        >>> join
        ValueError: Field 'join' is required!
        >>> join(('foo', 'bar'))
        {'join': 'JOIN foo ON bar'}

        >>> # 关联:
        >>> tp = Field('type', 'int', handle=lambda x: f" {x}")
        >>> length = Field('length', None, handle=lambda x: f"({x})", required=['int', 'varchar', 'char'])
        >>> length.related(tp, int='', varchar='255', char='64')
        >>> tp | length
        {'type': 'int', 'length': ''}
        >>> tp('varchar') | length
        {'type': 'varchar', 'length': '(255)'}

    :ivar _key: 字段名
    :ivar _default: 默认值
    :ivar _handle: 处理函数
    :ivar _required: 值列表
    :ivar _err: 是否报错
    :ivar _value: 用户输入值
    :ivar _flag: 用户输入None标志位
    :ivar _related: 关联字段
    :ivar _mapping: 关联映射
    """
    def __init__(self, key: str, default: Optional[str | int | Type | tuple[Any, Any]], *, handle: Callable[[str], str] = lambda x: f" {x}", required: list[str] = None, err: bool = False):
        """
            考虑输入:
                1. value:
                    - 需要处理:
                        handle(value): 如(lambda x: f"CHARACTER SET {}")('utf8mb4') -> "CHARACTER SET utf8mb4"
                    - 不需要处理:
                        value: 如'utf8mb4', 如果仅有例如'NOT NULL'或者''两种值,那么用户理应输入True,但如果用户输入字符串,则判断是否在'NOT NULL'和''中,如果在,则返回True,否则抛错处理.
                2. True:
                    - 需要处理:
                        handle(default): 如default -> 'utf8mb4', (lambda x: f"CHARACTER SET {}")('utf8mb4') -> "CHARACTER SET utf8mb4"
                    - 不需要处理:
                        default: 如'NOT NULL'
                3. False:
                    暂时等同于None.
                4. None:
                    - 一般输出'',但不排除某些字段必填,则需要处理

                default理应不为空,但如果某些字段不好进行自动处理,则可以传入None,但应该添加警告或报错.

                :param key: 字段名
                :param default: 默认值
                :keyword handle: 处理函数(默认为: (str) -> f" {str}")
                :keyword required: 值列表
                :keyword err: 是否报错
            """
        self._key, self._default, self._handle, self._required, self._err = key, default, handle, required, err
        self._value = None
        self._flag = True
        self._related: Optional[Field] = None
        self._mapping: Optional[dict[str, str]] = None

    @property
    def value(self) -> str:
        """
        处理多个来源的输入

        :return: 处理后的输入值
        :raise ValueError: 值为空且为必填字段
        """
        res = self._value or self._default

        if not any((self._value, self._default)):
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
        """获取处理结果"""
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
        """
        用户输入

        :param value: 用户输入值
        :return: self
        :raise ArgumentError: 值不在值列表中
        """
        if self._required and value not in self._required:
            raise ArgumentError(
                f"Invalid value for field: 'value', must be one of: {', '.join(self._required)}")

        if value and not isinstance(value, bool):
            self._value = value

        elif value is None:
            self._flag = False

        return self

    def related(self, other: Self, **kwargs: str) -> None:
        """关联字段"""
        self._related, self._mapping = other, kwargs


class Base(ABC):
    """
    实现单例模式,并提供属性.

    :ivar instance: 单例实例
    :ivar _res: 结果字典
    """
    instance: Self = None
    _res: Result = {'header': None, 'result': None, 'rowcount': None}

    @final
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance


class DB:
    """
    数据库类,提供数据库操作对应的仿位掩码类.

    Methods::
        Create: 创建数据库

        Drop: 删除数据库
    """
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
        """
        创建数据库

        :param dbName: 数据库名
        :keyword cfg: 数据库配置
        :keyword autoUse: 是否自动切换到新创建的数据库
        :return: None
        """
        self._execute(remap("CREATE DATABASE{exists} {dbName}{charset}{collate}", cfg, dbName=dbName))

        if autoUse:
            self.database = dbName

    @result(Base._res, Feedback.query)
    def drop(self, dbName: str, *, cfg: Field | dict[str, str | bool | None | Type] = None):
        """
        删除数据库

        :param dbName: 数据库名
        :keyword cfg: 数据库配置
        :return: None
        """
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
    """
    将python数据格式转换为sql数据格式.

    :param data: python数据
    :return: sql数据
    :raise NotImplementedError: 未实现类型
    """
    if isinstance(data, str):
        return f"'{data}'"

    elif isinstance(data, bool):
        return 'TRUE' if data else 'FALSE'

    elif isinstance(data, int):
        return str(data)

    elif isinstance(data, float):
        return str(data)

    raise NotImplementedError(  # 未实现类型
        f"Unsupported type: {type(data).__name__}")


class TB:
    """
    表类,提供表操作对应的仿位掩码类.

    Methods::
        Create: 创建表

        Drop: 删除表

        Select: 查询表

        Update: 更新表

        Alter: 修改表

        Delete: 删除表
    """
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
    """
    表操作类.

    :ivar _conn: sql连接对象
    :ivar _cur: sql游标对象
    :ivar _table: 表名
    :ivar _execute: 执行sql语句函数
    """
    class _field:
        """
        字段类,用于链式创建表字段.

        :ivar _ins: 原实例
        :ivar _name: 字段名
        :ivar _cfg: 表字段配置
        :ivar _count: 配置次数
        :ivar _inner: 内部配置
        """
        __res = "CREATE TABLE{exists} {tableName}($\n){engine}{charset}"

        def __init__(self, ins: 'Table', name: str, *, cfg: Field | dict[str, str | bool | None | Type] = None):
            """
            :param ins: 原实例
            :param name: 字段名
            :param cfg: 表字段配置,会与end方法获取的配置合并
            """
            self._ins, self._name, self._cfg = ins, name, cfg
            self._count = 0
            self._inner = ""

        def addField(self, name: str, *, cfg: Field | dict[str, str | bool | None | Type] = None) -> Self:
            """
            添加行字段

            :param name: 字段名
            :keyword cfg: 行字段配置
            :return: self
            """
            self._inner += remap("\n\t{name}{type}{lenght}{null}{default}{autoIncrement}{primaryKey},", cfg, name=name)

            return self

        def config(self, cfg: Field | dict[str, str | bool | None | Type] = None) -> Self:
            """
            配置行末表属性字段

            :param cfg: 表属性配置
            :return: self
            """
            if self._count >= 1: raise RuntimeError(  # 超过配置次数
                "Cannot have more than one config!")

            if cfg:
                self._inner += remap("\n\t{primaryKey}{foreignKey}{references} ", cfg)

            self._count += 1

            return self

        def end(self, cfg: Field | dict[str, str | bool | None | Type] = None) -> None:
            """
            结束表字段创建
            :param cfg: 表配置
            """
            cfg = (cfg or {} | self._cfg) if self._cfg else cfg

            self.__res = remap(self.__res, cfg, tableName=self._name)
            self.__res = self.__res.replace("$", self._inner[:-1])
            self._ins._exec(self.__res)

        def __call__(self, cfg: Field | dict[str, str | bool | None | Type] = None) -> None:
            self.end(cfg)

    def __init__(self, conn: Connection, cur: Cursor, *, table: str = None) -> None:
        self._conn = conn
        self._cur = cur
        self._table = table
        self._execute: Callable[[str], None] = partial(execute, conn, cur, self._res)

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

    @result(Base._res, Feedback.normal)
    def describe(self) -> None:
        self._execute(f"DESCRIBE {self.table}")

    def create(self, tbName: str, *, cfg: Field | dict[str, str | bool | None | Type] = None, autoUse: bool = True) -> _field:
        """
        创建表

        Example::
            >>> # Usage:
            >>> (mysql.tb.create("test", cfg=TB.Create.EXISTS))                                                      \
            >>>      .addField("id", cfg=TB.Create.TYPE | TB.Create.PRIMARY_KEY | TB.Create.AUTO_INCREMENT)          \
            >>>      .addField("name", cfg=TB.Create.TYPE(Type.VARCHAR) | TB.Create.LENGHT(255) | TB.Create.NULL)    \
            >>>      .config(TB.Create.FOREIGN_KEY('user_id') | TB.Create.REFERENCES('users(id)'))                   \
            >>>      .end(TB.Create.ENGINE('InnoDB') | TB.Create.CHARSET('utf8mb4'))
            CREATE TABLE IF NOT EXISTS test(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

        :param tbName: 表名
        :keyword cfg: 表配置
        :keyword autoUse: 是否自动切换到新创建的表
        :return: 字段链式创建对象
        """
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
    def select(self, *fields: str, cfg: Field | dict[str, str | bool | None | Type] = None) -> tuple[tuple[Any, ...], ...]:
        fields = fields or '*'

        self._execute(remap("SELECT {fields} FROM {table}{where}{order}{inner}{on}{limit}", cfg, fields=', '.join(fields), table=self._table))

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


class MySQL(Base):
    """
    MySQL操作类.

    Example::
        >>> # Usage:
        >>> with MySQL('root', 'password') as sql:
        >>>     sql.db.create('db_name', cfg=DB.Create.EXISTS)
        CREATE DATABASE IF NOT EXISTS db_name;

        >>> # last time use database
        >>> with MySQL('root', 'password', 'db_name') as sql:
        >>>     sql.tb.create('tb_name', cfg=TB.Create.EXISTS) ...  # see Table.create() for more details
        CREATE TABLE IF NOT EXISTS tb_name(...);

        >>> # last time use table
        >>> with MySQL('root', 'password', 'db_name', table='tb_name') as sql:
        >>>     sql.tb.insert(name='Alice', age=18)
        INSERT INTO tb_name (name, age) VALUES ('Alice', 18);

        >>> # normal use
        >>> with MySQL('root', 'password') as sql:
        >>>     sql.db.create('db_name', cfg=DB.Create.EXISTS, autoUse=True)
        >>>     sql.db.use()
        >>>     sql.tb.create('tb_name', cfg=TB.Create.EXISTS, autoUse=True) ...  # see Table.create() for more details
        >>>     sql.tb.insert(name='Alice', age=18)
        >>>     sql.tb.select()
        >>>     sql.tb.update(grade=1, cfg=TB.Update.WHERE("student_id=1 AND subject = 'A+'"))
        >>>     sql.tb.select()
        >>>     sql.tb.create('tb_name2', cfg=TB.Create.EXISTS) ...  # see Table.create() for more details
        >>>     sql.tb.table = 'tb_name2'
        >>>     sql.tb.select()

    :ivar _database: 数据库名
    :ivar _connect: sql连接对象
    :ivar _cursor: sql游标对象
    :ivar _table: 表名
    """
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
                f"Exception occurred: {exc_type}({exc_val}), line {exc_tb.tb_lineno}")

    def __getattr__(self, item: str) -> Any:
        """
        获取数据库或表操作对象.

        Note::
            如果获取的对象不存在于当前实例,则会尝试从连接对象中获取.

        :param item: 数据库或表名
        :return: 数据库或表操作对象
        """
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


PASSWORD: str
if __name__ == '__main__':
    with MySQL('root', PASSWORD) as mysql:
        ...
