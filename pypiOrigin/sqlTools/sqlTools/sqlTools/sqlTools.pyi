__all__: list
from pymysql.cursors import Cursor
from functools import wraps
from functools import cached_property
from warnings import warn
from pymysql import Connection, NULL
from typing import Callable, final, Self, TypedDict, Protocol, Any, Optional
from types import TracebackType
from enum import Enum
from abc import ABC
from pandas import DataFrame
SERVER_NAME: str
OUTPUT: bool


class Result(TypedDict):
    result: tuple[tuple[Any, ...], ...]
    header: list[str] | tuple
    rowcount: int
    spendtime: Optional[float]


class Type(Enum):
    VARCHAR = 'varchar'
    INT = 'int'
    CHAR = 'char'
    DATE = 'date'
    FLOAT = 'float'
    TIME = 'time'
    BOOLEAN = 'boolean'


FlagOrStr: subscript


class CanBeStr(Protocol):

    def __str__(self) ->str:
        ...
        ...

    def __repr__(self) ->str:
        ...
        ...


class ArgumentError(Exception):

    def __init__(self, *args):
        super().__init__(*(args or ('Invalid arguments',)))
        ...


@(lambda _: _())
def feasibleTest() ->None:
    """ 先行测试,检查mysql是否安装以及服务是否启动. """
    ...


del feasibleTest


def stderr(msg: str) ->None:
    """错误着色"""
    ...


def stdout(msg: str, *, allow: bool=True, **kwargs) ->None:
    """
    输出信息

    :param msg: 输出信息
    :param allow: 是否允许输出
    :keyword kwargs: 其他print函数参数
    """
    ...


@final
class Feedback:
    """
    反馈类,用于处理mysql的反馈信息.

    Note::
        该类的类方法中的参数名皆注册于Base类中.
    """

    @staticmethod
    def normal(rowcount: int, *, spendtime: float=0.0) ->str:
        """
        输出表类型信息.

	@warning xxx

        :param rowcount: 行数
        :keyword spendtime: 耗时
        :return: 表类型信息
        """
        ...

    @staticmethod
    def query(rowcount: int, *, spendtime: float=0.0) ->str:
        """ 输出查询信息. """
        ...

    @staticmethod
    def empty(*, spendtime: float=0.0) ->str:
        """ 输出空结果信息. """
        ...

    @staticmethod
    def alter(rowcount: int) ->str:
        """ 输出修改信息. """
        ...

    @staticmethod
    def useDb() ->str:
        """ 输出切换数据库信息. """
        ...


def result(res: Result, fbFn: (Callable[..., str] | function)=None) ->Callable[
    ..., Any]:

    def getfunc(fn: Callable) ->Callable:

        @wraps(fn)
        def warp(*_args, **_kwargs) ->Any:
            """
            :raise RuntimeError: 结果处理失败
            """
            ...


def remap(_format: str, mapping: Optional[dict[str, str] | 'Field'], **
    kwargs: str) ->str:
    """
    格式化字符串,生成sql语句.

    :param _format: 格式化字符串
    :param mapping: 映射字典
    :keyword kwargs: 特化参数
    :return: 格式化后的sql语句
    """
    ...


def execute(conn: Connection, cur: Cursor, res: Result, cmd: str, *, allow:
    bool=True) ->None:
    """
    执行sql语句.

    :param conn: sql连接对象
    :param cur: sql游标对象
    :param res: 结果字典
    :param cmd: sql语句
    :keyword allow: 是否允许输出
    """
    ...


class Field:
    """
    字段类,通过仿位掩码类,实现自动处理.

    TODO: 实现嵌套Field功能,如: where(condition1 | and | condition2) | order(desc)
    TODO: 修复0被误判为假的问题

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

    def __init__(self, key: str, default: Optional[str | int | Type | tuple
        [Any, Any]], *, handle: Callable[[str], str]=lambda x: f' {x}',
        required: list[str]=None, err: bool=False):
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
        ...

    @property
    def value(self) ->str:
        """
        处理多个来源的输入

        :return: 处理后的输入值
        :raise ValueError: 值为空且为必填字段
        """
        ...

    @property
    def result(self) ->dict[str, str]:
        """获取处理结果"""
        ...

    def __str__(self) ->str:
        ...

    def __or__(self, other: (Self | dict[str, str])) ->dict[str, str]:
        ...

    def __ror__(self, other: (Self | dict[str, str])) ->dict[str, str]:
        ...

    def __call__(self, value: (str | bool | None | Type)) ->Self:
        """
        用户输入

        :param value: 用户输入值
        :return: self
        :raise ArgumentError: 值不在值列表中
        """
        ...

    def related(self, other: Self, **kwargs: str) ->None:
        """关联字段"""
        ...


class Base(ABC):
    """
    实现单例模式,并提供属性.

    :ivar instance: 单例实例
    :ivar _res: 结果字典
    """

    @final
    def __new__(cls, *args, **kwargs):
        ...


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
        CHARSET = Field('charset', 'utf8mb4', handle=lambda x:
            f' CHARACTER SET {x}')
        COLLATE = Field('collate', 'utf8mb4_general_ci', handle=lambda x:
            f' COLLATE {x}')


    @final
    class Drop(ABC):
        EXISTS = Field('exists', 'IF EXISTS', required=['IF EXISTS'])


class Database(Base):

    def __init__(self, conn: Connection, cur: Cursor, database: Optional[
        str]=None, *, table: str=None):
        ...

    @result(Base._res, Feedback.normal)
    def show(self) ->None:
        """显示数据库列表"""
        ...

    @result(Base._res, Feedback.useDb)
    def use(self, database: str=None) ->None:
        """切换数据库"""
        ...

    @result(Base._res, Feedback.query)
    def create(self, dbName: str, *, cfg: (Field | dict[str, str | bool |
        None | Type])=None, autoUse: bool=True) ->None:
        """
        创建数据库

        :param dbName: 数据库名
        :keyword cfg: 数据库配置
        :keyword autoUse: 是否自动切换到新创建的数据库
        :return: None
        """
        ...

    @result(Base._res, Feedback.query)
    def drop(self, dbName: str, *, cfg: (Field | dict[str, str | bool |
        None | Type])=None):
        """
        删除数据库

        :param dbName: 数据库名
        :keyword cfg: 数据库配置
        :return: None
        """
        ...


def py2sql(data: Any) ->Any:
    """
    将python数据格式转换为sql数据格式.

    :param data: python数据
    :return: sql数据
    :raise NotImplementedError: 未实现类型
    """
    ...


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
        LENGHT = Field('lenght', None, handle=lambda x: f'({x})' if x else '')
        LENGHT.related(TYPE, int='', varchar='128', char='255', date='',
            float='', time='', boolean='')
        NULL = Field('null', 'NOT NULL', required=['NOT NULL'])
        DEFAULT = Field('default', None, err=True)
        AUTO_INCREMENT = Field('autoIncrement', 'AUTO_INCREMENT', required=
            ['AUTO_INCREMENT'])
        PRIMARY_KEY = Field('primaryKey', 'PRIMARY KEY', required=[
            'PRIMARY KEY'])
        ENGINE = Field('engine', 'InnoDB', handle=lambda x: f' ENGINE={x}')
        CHARSET = Field('charset', 'utf8', handle=lambda x:
            f' DEFAULT CHARSET={x}')
        EXISTS = Field('exists', 'IF NOT EXISTS', required=['IF NOT EXISTS'])
        FOREIGN_KEY = Field('foreignKey', None, handle=lambda x:
            f' FOREIGN KEY ({x})', err=True)
        REFERENCES = Field('references', None, handle=lambda x:
            f' REFERENCES {x}', err=True)


    @final
    class Drop(ABC):
        EXISTS = Field('exists', 'IF EXISTS', required=['IF EXISTS'])


    @final
    class Select(ABC):
        WHERE = Field('where', None, handle=lambda x: f' WHERE {x}', err=True)
        ORDER = Field('order', None, handle=lambda x: f' ORDER BY {x}', err
            =True)
        LIMIT = Field('limit', 1, handle=lambda x: f' LIMIT {x}', err=True)
        INNER = Field('inner', None, handle=lambda x:
            f' INNER JOIN {x[0]} ON {x[1]}', err=True)
        OFFSET = Field('offset', None, handle=lambda x: f' OFFSET {x}', err
            =True)
        LEFT = Field('left', None, handle=lambda x:
            f' LEFT JOIN {x[0]} ON {x[1]}', err=True)


    @final
    class Update(ABC):
        WHERE = Field('where', None, handle=lambda x: f' WHERE {x}', err=True)


    @final
    class Alter(ABC):
        DROP = Field('drop', None, handle=lambda x: f' DROP {x}', err=True)


    @final
    class Delete(ABC):
        WHERE = Field('where', None, handle=lambda x: f' WHERE {x}', err=True)


class Table(Base):
    """
    表操作类.

    :ivar _conn: sql连接对象
    :ivar _cur: sql游标对象
    :ivar _table: 表名
    :ivar _execute: 执行sql语句函数
    """

    def __init__(self, conn: Connection, cur: Cursor, *, table: str=None
        ) ->None:
        ...

    @cached_property
    def content(self) ->tuple[tuple[Any, ...], ...]:
        ...

    def __getitem__(self, item: (str | int)) ->(tuple[Any, ...] | _series):
        """
        实现ORM功能,通过[]访问表字段.

        :param item: 表字段名或行索引
        :return: 表字段操作对象
        """
        ...

    def __getattr__(self, item: str) ->tuple[Any, ...]:
        """
        实现ORM功能,通过属性访问表字段.

        :param item: 表字段名
        :return: 表字段操作对象
        """
        ...

    def __delitem__(self, key: int) ->None:
        self.delete(cfg=TB.Delete.WHERE(' and '.join(f'{k}={py2sql(v)}' for
            k, v in self.content)))
        ...

    def __iter__(self):
        ...

    def __next__(self) ->_series:
        ...

    @property
    def table(self) ->str:
        ...

    @table.setter
    def table(self, value: str) ->None:
        ...

    @result(Base._res, Feedback.query)
    def _exec(self, cmd: str) ->None:
        self._execute(cmd)
        ...

    @result(Base._res, Feedback.query)
    def show(self) ->None:
        self._execute(f'SHOW TABLES')
        ...

    @result(Base._res, Feedback.normal)
    def describe(self) ->None:
        self._execute(f'DESCRIBE {self.table}')
        ...

    def create(self, tbName: str, *, cfg: (Field | dict[str, str | bool |
        None | Type])=None, autoUse: bool=True) ->_field:
        """
        创建表

        Example::
            >>> # Usage:
            >>> (mysql.tb.create("test", cfg=TB.Create.EXISTS))                                                                  >>>      .addField("id", cfg=TB.Create.TYPE | TB.Create.PRIMARY_KEY | TB.Create.AUTO_INCREMENT)                      >>>      .addField("name", cfg=TB.Create.TYPE(Type.VARCHAR) | TB.Create.LENGHT(255) | TB.Create.NULL)                >>>      .config(TB.Create.FOREIGN_KEY('user_id') | TB.Create.REFERENCES('users(id)'))                               >>>      .end(TB.Create.ENGINE('InnoDB') | TB.Create.CHARSET('utf8mb4'))
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
        ...

    @result(Base._res, Feedback.query)
    def drop(self, tbName: str, *, cfg: (Field | dict[str, str | bool |
        None | Type])=None) ->None:
        self._execute(remap('DROP TABLE{exists} {tbName}', cfg, tbName=tbName))
        ...

    @result(Base._res, Feedback.query)
    def insert(self, **data: Any) ->None:
        self._execute(
            f"INSERT INTO {self.table} ({', '.join(data.keys())}) VALUES ({', '.join(map(py2sql, data.values()))})"
            )
        ...

    @result(Base._res, Feedback.query)
    def select(self, *fields: str, cfg: (Field | dict[str, str | bool |
        None | Type])=None, tbName: str=None) ->list[dict[str, Any]]:
        ...

    @result(Base._res, Feedback.query)
    def update(self, *, cfg: (Field | dict[str, str | bool | None | Type])=
        None, **data: Any) ->None:
        self._execute(remap(
            f"UPDATE {self.table} SET {', '.join(map(lambda x: f'{x[0]}={py2sql(x[1])}', data.items()))}{{where}}"
            , cfg))
        ...

    @result(Base._res, Feedback.query)
    def alter(self, tbName: str=None, *, cfg: (Field | dict[str, str | bool |
        None | Type])=None) ->None:
        ...

    @result(Base._res, Feedback.query)
    def delete(self, *, cfg: (Field | dict[str, str | bool | None | Type])=None
        ) ->None:
        self._execute(remap(f'DELETE FROM {self.table}{{where}}', cfg))
        ...

    def toDataFrame(self) ->DataFrame:
        ...

    def toCSV(self, csvPath: str) ->None:
        ...

    def fromCSV(self, csvPath: str) ->None:
        warn('Not implemented yet.', DeprecationWarning)
        ...


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

    def __init__(self, user: str, password: str, database: Optional[str]=
        None, *, host: str='localhost', table: str=None, **kwargs) ->None:
        ...

    def __enter__(self) ->Self:
        self._connect.connect()
        ...

    def __exit__(self, exc_type, exc_val, exc_tb: TracebackType) ->None:
        self._cursor.close()
        ...

    def __getattr__(self, item: str) ->Any:
        """
        获取数据库或表操作对象.

        Note::
            如果获取的对象不存在于当前实例,则会尝试从连接对象中获取.

        :param item: 数据库或表名
        :return: 数据库或表操作对象
        """
        ...

    @cached_property
    def db(self) ->Database:
        ...

    @cached_property
    def tb(self) ->Table:
        ...

    @property
    def database(self) ->str:
        ...

    @database.setter
    def database(self, value: str) ->None:
        ...

    @property
    def table(self) ->str:
        ...

    @table.setter
    def table(self, value: str) ->None:
        ...
