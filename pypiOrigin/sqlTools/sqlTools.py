#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/24 22:26
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from collections.abc import Container
from functools import wraps
from warnings import warn
from pymysql import connect, Error, NULL
from typing import Callable, Literal, final, Final, TypeVar
from pandas import DataFrame
from types import EllipsisType
from time import time
from csv import writer, reader


__version__ = "0.0.9"


try:
    from ANSIdefine.ansiDefine import ansiManger
except ModuleNotFoundError:
    try:
        from ansiDefine.ansiDefine import ansiManger  # type: ignore
    except ModuleNotFoundError as e:
        raise e from RuntimeError("没有安装ANSIdefine模块,使用`pip install -i https://test.pypi.org/simple ANSI-Define`安装。")

__all__ = [
    "baseSQL",
    "errorf"
]

__author__ = "Xiao Songtao"

color = ansiManger()

con1 = TypeVar("((TYPE: str, ), )")
con2 = TypeVar("((TYPE: str, length: int), )")
con3 = TypeVar("((TYPE: str, length: int), notNull: bool, default: str | bool, auto: bool)")
con4 = TypeVar("((TYPE: str, length: int), notNull: bool, default: str | bool, auto: bool, other: str | None)")


def errorf(errorindex: str = "10000"):
    """
    用于将baseSql的错误输出转换为mysql格式的装饰器.

    :param errorindex: 错误的状态码,由于无法获取,该值需要手动设定.
    :type errorindex: str
    :return: 装饰后的函数.
    :retype: Callable
    """

    def getfunc(func: Callable):
        @wraps(func)
        def warp(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Error as e:
                if isinstance(e.args, tuple):
                    print(color.f_systemRED(f"ERROR {e.args[0]} ({errorindex}): {e.args[1]}"))
                else:
                    print(color.f_systemRED(f"Other Error: {e}"))

        return warp

    return getfunc


class baseSQL:
    """
    包装了pyMySql部分功能的类.

    Attributes:
        _user: 用户名.
        _password: 用户密码.
        _database: 数据库名
        _host: 主机名.
        _connect: 链接.
        _cursor: 执行指针.
        datatype: 部分数据类型.
        tbName: 数据表名称.

    Methods::
        _show_feedback: 返回mysql中展示表的反馈.\n
        _op_feedback: 返回mysql中操作命令的反馈.\n
        _empty_feedback: mysql对于空表的反馈.\n
        _alter_feedback: mysql中修改列的反馈.\n
        _security_check: 某些操作将导致不可逆的后果,使用该函数进行警告,并且检查返回的布尔值以决定是否继续.\n
        _checkParam: 当某些参数不能为空时使用该函数进行检测.\n
        _to_show: 表格化单列输出.\n
        _mutlishow: 表格化多列输出.\n
        _checkDict: 对输入数据进行数据库的兼容性修改.\n
        COLUMN: 获取数据表表头(要求在之前有查询表操作).\n
        DATABASE: 获取和显示所有数据库.\n
        TABLE: 获取和显示数据库的所有数据表.\n
        getColumn: 获取表头,与方法COLUMN不同的是,COLUMN需要先查表,而该函数自动进行查表.\n
        showTableFrame: 获取和显示数据表结构.\n
        showTableContent: 获取和显示数据表内容.\n
        selectColumn: 获取和展示选择数据表的某列.\n
        createDB: 创建数据库.\n
        dropDB: 删除数据库.\n
        createTable: 创建数据表.\n
        dropTable: 删除数据表.\n
        insert: 向数据表添加数据.\n
        updata: 修改数据表中数据.\n
        delete: 删除数据表中当个或所有数据.\n
        column_add: 为数据表添加一列.\n
        column_drop: 删除数据表中的某一列.\n
        column_modify: 修改数据表中某一列的定义.\n
        column_default: 修改数据表中某一列的默认值.\n
        column_dropDef: 删除数据表中某一列的默认值.\n
        column_change: 使用change方式对某一列的定义进行修改.\n
        tbName_modify: 修改数据表的名称.\n
        executeOther: 执行其它命令(MySql移植).\n
        to_csv: 将数据表导出为csv文件.\n
        csv_to_mysql: 导入csv文件为数据表.\n
        table_to_DataFrame: 将数据表导出为DataFrame.\n
        checkId: 遍历数据表的id索引值,检测id是否连续以判断是缺漏数据.\n
        randomChoice: 返回随机选择数据表中的数据
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, user: str, password: str, database: str = None, *, host: str = 'localhost',
                 tableName: str = None):
        self._user = user
        self._password = password
        self._database = database
        self._host = host
        self._connect = connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=database
        )
        self._cursor = self._connect.cursor()
        self.datatype: Final = {"v": "varchar",
                                "i": "int",
                                "c": "char",
                                "d": "date",
                                "f": "float",
                                "t": "time",
                                "b": "boolean"
                                }
        self.tbName = tableName

    @staticmethod
    def _show_feedback(listlen: int, *, spendtime: float = 0.00) -> str:
        """
        返回mysql中展示表的反馈(这其中并没有换行符,你需要根据实际的数据库反馈来在使用的字符串前后添加换行符).

        :param listlen: 数据表的行数
        :type listlen: int
        :param spendtime: 运行耗时
        :type spendtime: float
        :return: 返回填充后的字符串.
        :retype: str
        """
        return f"{listlen} {'rows' if listlen != 1 else 'row'} in set ({spendtime:.3f} sec)"

    @final
    def _to_show(self, title: str, conlist: list[str], *, spendtime: float = None) -> str:
        """
        在数据库只返回单个列的值的情况下,将返回的列表数据转换为可以被打印的表格的形式.

        :param title: 该表的表头,例如`SHOW DATABASES;`输出的表头为'Database'.
        :type title: str
        :param conlist: 内容列表.
        :type conlist: list
        :param spendtime: 消耗的时间,这将显示在例如'Query OK, 0 row affected (spendtime sec)',可以使用time的time()函数在指针执行前后进行计时以获得.
        :type spendtime: float
        :return: 返回转换后的字符串.
        :retype: str
        """
        from textTools import getWidth
        conlist = list(map(lambda x: str(x).replace(" ", ""), conlist))

        maxlen = m if (m := max([getWidth(i) for i in conlist])) >= (l := getWidth(title)) else l

        line = "+" + "-" * (maxlen + 2) + "+"

        head = f"{line}\n| {title}{(maxlen - getWidth(title)) * ' '} |\n{line}\n"

        for content in conlist:
            head += f"| {content}{(maxlen - getWidth(content)) * ' '} |\n"
        head += line

        head += f"\n{self._show_feedback(len(conlist), spendtime=spendtime)}\n"

        return head

    @final
    def _mutlishow(self, columlist: list[str], conlist: list[tuple], *, spendtime: float = None) -> str:
        """
        在数据库只返回多个列的值的情况下,将返回的列表数据转换为可以被打印的表格的形式.

        :param columlist: 展示的表头,你可以通过self.COLUM获取.
        :type columlist: list
        :param conlist: 内容列表.
        :type conlist: list
        :param spendtime: 运行耗时.
        :type spendtime: float
        :return: 返回什么.
        :retype: str
        """
        from textTools import getWidth
        conlist = [list(map(lambda x: str(x).replace(" ", ""), content)) for content in conlist]

        if (conl := len(columlist)) != (cl := len(conlist[0])):
            raise ValueError(f"列名列表长度必须与每行元素个数一致,{columlist}长为{conl},{conlist[0]}长为{cl}")

        lenlist = [max([4 if (l := alist[i]) is None else getWidth(l) for alist in conlist]) for i in
                   range(len(conlist[0]))]

        maxlen = [c if (c := getWidth(colum)) > wordlen else wordlen for colum, wordlen in zip(columlist, lenlist)]

        line = "+"

        for l in maxlen:
            line += f"{(l + 2) * '-'}+"

        head = f"{line}\n"

        for i, colum in enumerate(columlist):
            head += f"| {colum}{(maxlen[i] - getWidth(colum)) * ' '} "

        head += f"|\n{line}\n"

        for content in conlist:
            for i, word in enumerate(content):
                head += f"| {word}{(maxlen[i] - (4 if word is None else getWidth(word))) * ' '} "
            head += "|\n"

        head += f"{line}\n{self._show_feedback(len(conlist), spendtime=spendtime)}\n"

        return head

    def _op_feedback(self, spendtime: float = 0.00) -> str:
        """
        返回mysql中操作命令的反馈(这其中并没有换行符,你需要根据实际的数据库反馈来在使用的字符串前后添加换行符).

        :param spendtime: 运行耗时.
        :type spendtime: float
        :return: 填充后的字符串.
        :retype: str
        """
        return f"Query OK, {self._cursor.rowcount} rows affected ({spendtime:.3f} sec)"

    @staticmethod
    def _empty_feedback(*, spendtime: float = 0.00) -> str:
        """
        mysql对于空表的反馈.

        :param spendtime: 运行耗时.
        :type spendtime: float
        :return: 填充后的字符串.
        :retype: str
        """
        return f"Empty set ({spendtime:.3f} sec)"

    def _alter_feedback(self):
        """
        mysql中修改列的反馈.

        :return: 填充后的字符串.
        :retype: str
        """
        return f"Records: {self._cursor.rowcount}  Duplicates: 0  Warnings: 0"

    @staticmethod
    def _security_check(checkparam: bool, *, warnstr: str = None) -> None:
        """
        某些操作将导致不可逆的后果,使用该函数进行警告,并且检查返回的布尔值以决定是否继续.

        :param checkparam: 传入该参数决定是否启用检测.
        :type checkparam: bool
        :param warnstr: 提示的字符串, 如为None或为空则默认为:'此操作将删除所有值.你确定要继续吗?(Y.是,N.否)'.
        :type warnstr: str
        :return: 操作执行函数不做返回.
        :retype: None
        """
        if warnstr is None:
            warnstr = "此操作将删除所有值.你确定要继续吗?(Y.是,N.否)"

        if checkparam:
            inp = input(color.f_yellow(warnstr))
            if inp.lower() != "y":
                exit(f"用户输入了{inp}以中断了操作.")

    @staticmethod
    def _checkParam(func: Callable, param, paramName: str, *, warnstr: str = None) -> None:
        """
        当某些参数不能为空时使用该函数进行检测.

        :param func: 执行的函数.
        :type func: Callable
        :param param: 进行检测的参数.
        :type param: ...
        :param warnstr: 警告的字符串.
        :type warnstr: str
        :return: 操作执行函数不做返回.
        :retype: None
        """
        warnstr = f"{baseSQL.__name__}.{func.__name__}() missing 1 required positional argument: '{paramName}'" if warnstr is None else warnstr
        if param is None:
            raise TypeError(warnstr)

    @staticmethod
    def _checkDict(aimContainer: list | dict):
        """
        用以检测和转换容器中的内容使其兼容mysql语法.

        :param aimContainer: 需要检测的参数.
        :type aimContainer: 容器或单个元素.
        :return: 返回什么.
        :retype: ...
        """
        Nullset = {"null", "none", ""}
        excludeDict = {r"/null": 'null', r"/none": 'none'}

        if isinstance(aimContainer, dict):
            for key in aimContainer.keys():
                value = aimContainer[key]
                if isinstance(value, int):
                    aimContainer[key] = str(value)
                elif isinstance(value, str):
                    if not value.isdigit():
                        if value.lower() in Nullset:
                            aimContainer[key] = NULL
                        elif value.lower() in excludeDict:
                            aimContainer[key] = f"'{excludeDict[value.lower()]}'"
                        else:
                            aimContainer[key] = f"'{value}'"
                elif value is None:
                    aimContainer[key] = NULL
            return aimContainer
        elif isinstance(aimContainer, list):
            for i, v in enumerate(aimContainer):
                if isinstance(v, int):
                    aimContainer[i] = str(v)
                elif isinstance(v, str):
                    if not v.isdigit():
                        if v.lower() in Nullset:
                            aimContainer[i] = NULL
                        elif v.lower() in excludeDict:
                            aimContainer[i] = f"'{excludeDict[v.lower()]}'"
                        else:
                            aimContainer[i] = f"'{v}'"
                elif v is None:
                    aimContainer[i] = NULL
            return aimContainer
        elif isinstance(aimContainer, int) or isinstance(aimContainer, float):
            return str(aimContainer)
        elif isinstance(aimContainer, str):
            if aimContainer in Nullset:
                return NULL
            else:
                return f"'{aimContainer}'"
        elif aimContainer is None:
            return NULL
        else:
            warn("由于没有该类型的检测,所有我将返回原参数,你可能需要对内容逐个的使用该函数进行检测和转换.",
                 SyntaxWarning)
            return aimContainer

    @property
    def tableLen(self):
        self._cursor.execute(f"SELECT * FROM {self.tbName} ORDER BY id DESC LIMIT 1;")
        self._connect.commit()

        return self._cursor.fetchall()[0][0]

    @property
    def COLUMN(self):
        """
        用于获取数据表的表头.(在获取之前应进行查询表操作.)

        原返回的元组中包括:
        1.列名：表示查询结果列的名称.
        2.列类型代码: 表示查询结果列的数据类型代码.
        常见的类型代码包括:
            1: CHAR
            2: NUMERIC
            3: DECIMAL
            4: INT
            5: SMALLINT
            7: FLOAT
            8: DOUBLE
            9: NULL
            10: DATE
            11: TIME
            12: DATETIME
            252: BLOB
            253: VARCHAR
            254: CHARACTER
            等等
        3.列长度: 表示查询结果列的最大长度.
        4.列精度: 对于数值类型的列，表示精度(总位数).
        5.列小数位数: 对于数值类型的列，表示小数位数.
        6.列标志: 一个整数，表示列的一些特性。例如，是否为主键、是否可为空等.
        7.是否可为空: 一个布尔值，表示查询结果列是否允许为空.

        返回的列表中只包含列名.
        """
        try:

            return [column[0] for column in self._cursor.description]

        except TypeError:

            raise TypeError("在获取列数据前,应先进行查询表操作.")

    @property
    def DATABASE(self, *, show: bool = True) -> list:
        """
        返回并默认展示所有数据库.

        获取Databases数据::

            >>> sql = baseSQL("username", "password")
            >>> data = sql.DATABASE

        仅查看数据::

            >>> sql = baseSQL("username", password)
            >>> sql.DATABASE

        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 包含所有数据库名称的列表.
        :retype: list
        """

        start = time()

        print("mysql> show databases;") if show else None

        self._cursor.execute("show databases;")
        self._connect.commit()

        DBlist = [i[0] for i in self._cursor.fetchall()]

        print(self._to_show(self.COLUMN[0], DBlist, spendtime=time() - start)) if show else None

        return DBlist

    @property
    def TABLE(self, *, show: bool = True):
        """
        展示数据库中的所有数据表.

        获取Table数据::

            >>> sql = baseSQL("username", "password")
            >>> data = sql.TABLE

        仅查看数据::

            >>> sql = baseSQL("username", "password")
            >>> sql.TABLE

        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 包含所有数据表名称的列表.
        :retype: list
        """

        if self._database is None: raise ValueError("数据库参数为空.")

        start = time()

        print(f"mysql> use {self._database};\n"
              f"Database changed;\n"
              f"mysql> show tables;") if show else None

        self._cursor.execute("show tables;")
        self._connect.commit()

        tablelist = [i[0] for i in self._cursor.fetchall()]

        if tablelist:
            print(self._to_show(self.COLUMN[0], tablelist, spendtime=time() - start)) if show else None
        else:
            print(self._empty_feedback(spendtime=time() - start))

        return tablelist

    @errorf()
    def getColumn(self, tbName: str = None) -> list[str]:
        """
        获取表头,与方法COLUMN不同的是,COLUMN需要先查表,而该函数自动进行查表.

        获取列名::

            >>> print(sql.getColumn())  # ['id', 'username', ...]

        :param tbName: 数据表名称.
        :type tbName: str
        :return: 包含数据表的列名.
        :retype: list[str]
        """

        if tbName is None:
            tbName = self.tbName

        if self.tbName is None:
            raise ValueError(
                f"使用该方法的前提是填写baseSQL初始方法中的关键字参数`tableName`"
            )

        self._cursor.execute(f"select * from {tbName}")
        self._connect.commit()

        return [column[0] for column in self._cursor.description]

    @errorf()
    def showTableFrame(self, tbName: str = None, *, show: bool = True) -> list:
        """
        获取和展示数据表的结构.

        :param tbName: 数据表的名称,如果在__init__()中已经定义,则可为None或留空.
        :type tbName: str
        :param show: 是否打印以展示.
        :type show: bool
        :return: 包含数据结构的列表.
        :retype: list
        """

        if tbName is None:
            tbName = self.tbName

        start = time()

        print(f"mysql> describe {tbName};") if show else None

        self._cursor.execute(f"describe {tbName};")
        self._connect.commit()

        frame = list(self._cursor.fetchall())

        print(self._mutlishow(self.COLUMN, frame, spendtime=time() - start)) if show else None

        return frame

    @errorf()
    def showTableContent(self, tbName: str = None, *, show: bool = True) -> list:
        """
        展示数据表的所有内容,等价于`SELECT * FROM TABLWNAME;`.

        :param tbName: 数据表名称.
        :type tbName: str
        :param show: 是否打印以展示.
        :type show: bool
        :return: 包含所有内容的列表.
        :retype: list
        """

        if tbName is None:
            tbName = self.tbName

        start = time()

        print(f"mysql> select * from {tbName};") if show else None

        self._cursor.execute(f"select * from {tbName};")
        self._connect.commit()

        res = self._cursor.fetchall()

        if isinstance(res, Container) and not len(res):
            print(f"{self._empty_feedback(spendtime=start - time())}\n") if show else None
            return []

        print(self._mutlishow(self.COLUMN, list(res), spendtime=time() - start)) if show else None

        return list(res)

    @errorf()
    def selectColumn(self, tbName: str | tuple[str] = None, columns: tuple[str, EllipsisType] = None, *,
                     condition: Literal["where ... and/or ... (like %str )"] | str = None, show: bool = True) -> list:
        """
        返回或展示数据表中的某些列的内容.

        获取::

            >>> sql.selectColumn(None, ("label", ), condition="where id > 0")  # 获取label列下id大于0的列

            >>> sql.selectColumn(None, ("*", ))  # 获取所有数据

        :param tbName: 数据表名称.
        :type tbName: ...
        :param columns: 选择的列名.(PS.如需选择全部则为('*', ))
        :type columns: tuple
        :keyword condition: 符合mysql语法的条件,如:`WHERE COLUMN1 > 0`
        :type condition: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 返回单个或多个列的内容列表.
        :retype: list
        """

        if tbName is None:
            tbName = self.tbName

        if not isinstance(columns, tuple):
            raise ValueError(f"参数columns必须为元组类型,如(column1,).")

        text = f"select {', '.join(columns)} from {', '.join(tbName) if isinstance(tbName, tuple) else tbName}{';' if condition is None else f' {condition};'}"

        print(f"mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        res = self._cursor.fetchall()

        if isinstance(res, Container) and not len(res):
            print(f"{self._empty_feedback(spendtime=time() - start)}\n") if show else None
            return []

        if len(columns) == 1 and columns[0] != "*":
            unlist = [i[0] for i in res]
            print(self._to_show(self._cursor.description[0][0], unlist, spendtime=time() - start)) if show else None
            return unlist
        else:
            mutilist = list(res)
            print(self._mutlishow(self.COLUMN, mutilist, spendtime=time() - start)) if show else None
            return mutilist

    @errorf("42000")
    def createDB(self, dbName: str, *, show: bool = True) -> None:
        """
        创建数据库.

        创建::

            >>> sql.createDB("database")

        :param dbName: 数据库名称.
        :type dbName: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        start = time()

        print(f"mysql> create database {dbName};") if show else None

        self._cursor.execute(f"create database {dbName};")
        self._connect.commit()

        print(f"{self._op_feedback(spendtime=time() - start)}\n") if show else None

    @errorf("HY000")
    def dropDB(self, dbName: str, *, show: bool = True, check: bool = True) -> None:
        """
        删除数据库.

        :param dbName: 数据库名称.
        :type dbName: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :keyword check: 是否进行安全检查.
        :type check: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        self._security_check(check)

        start = time()

        print(f"mysql> drop database {dbName};") if show else None

        self._cursor.execute(f"drop database {dbName};")
        self._connect.commit()

        print(f"{self._op_feedback(spendtime=time() - start)}\n") if show else None

    @errorf()
    def createTable(self, tableName: str, id_AUTO: bool | str = True, primarykey: str = None, show: bool = True, **kwargs: con1 | con2 | con3 | con4) -> None:
        r"""
        创建数据表.

        例子::

            create table tablename (
                id int auto_increment primary key,
                username varchar(50) not null,
                date date,
                bool boolean default true,
                或者primary key (id)
            )

        实现代码::

        >>> sql.createTable("tablename", True, username=(('v', 50), False), date=(('d', ), ), bool=(('b', ), True, "true"))

        可用类型::

            v: varchar
            i: int
            c: char
            d: date
            f: float
            t: time
            b: boolea

        :param tableName: 数据表名称.
        :type tableName: str
        :param id_AUTO: 是否需要id主键,如果为True则默认使用自增id主键,如为str类型则将使用传入的字符串作为名称创建自增主键.(该参数仅为快捷方式,同样可以在primarykey,args中定义id主键.)
        :type id_AUTO: str or bool
        :param primarykey: 指定主键.(此主键应在参数args中被定义).
        :type primarykey: str
        :param show: 是否打印以展示.
        :type show: bool
        :keyword kwargs: 指定表中的列名和其定义,且参数应形如'列名=定义元组',其中元组应形如:
            1.((类型, 长度[可选可空]), )
            2.((类型, 长度[可选可空]), 是否可为空, 默认值, 自增,)
            3.((类型, 长度[可选可空]), 是否可为空, 默认值, 自增, 其它约束)
        :return: 操作执行函数不做返回.
        :retype: None
        """

        keyName = id_AUTO if isinstance(id_AUTO, str) else 'id'

        text = f"create table {tableName} ({'' if id_AUTO is False else f'{keyName} int auto_increment primary key,'}"

        def raiseError(key: str, value):
            raise ValueError(f"用户输入了一个非正确格式参数:'{k}={f'{v}' if isinstance(v, str) else v}'")

        for k, v in kwargs.items():
            if v and isinstance(v, tuple):

                t = v[0]
                if isinstance(t, tuple):
                    if t[0] in self.datatype:
                        if len(t) == 1:
                            if t[0].lower() == "v":
                                warn("VARCHAR数据类型一般有长度限制,否则可能引起mysql语法错误.", SyntaxWarning)
                            t = self.datatype[t[0]]
                        elif len(t) == 2 and isinstance(t[1], int):
                            t = f"{self.datatype[t[0]]}({t[1]})"
                        else:
                            raiseError(k, v)
                    else:
                        warn(f"该值{t}不在数据类型缩写字典中,该类型将完整的运用在命令中,也许会造成错误,如否请忽略.",
                             SyntaxWarning)
                else:
                    raiseError(k, v)

                if (l := len(v)) == 1:
                    text += f"{k} {t},"
                elif l >= 4:
                    text += f'{k} {t}' \
                            f'{" not null" if v[1] else ""}' \
                            f'{f" default {v[2]}" if v[2] and isinstance(v[2], str) else ""}' \
                            f'{" auto_increment" if v[3] else ""}' \
                            f'{f" {v[4]}" if l == 5 and v[4] else ""},'
                else:
                    raiseError(k, v)
            else:
                raiseError(k, v)

        text = text[:-1] + f",primary key ({primarykey}))" if isinstance(primarykey, str) else f"{text[:-1]})"

        if show:
            index = (textlist := list("mysql> " + ",\n    -> ".join(text.split(",")) + ";")).index("(")
            textlist.insert(index + 1, "\n    -> ")
            print("".join(textlist))

        start = time()

        self._cursor.execute(f"{text};")
        self._connect.commit()

        print(f"{self._op_feedback(spendtime=time() - start)}\n") if show else None

    @errorf()
    def dropTable(self, tbName: str, *, show: bool = True, check: bool = True) -> None:
        """
        删除表.

        :param tbName: 表名.
        :type tbName: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :keyword check: 是否进行安全检查.
        :type check: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        start = time()

        self._security_check(check)

        print(f"mysql> drop table {tbName};") if show else None

        self._cursor.execute(f"drop table {tbName};")
        self._connect.commit()

        print(f"Query OK, {self._cursor.rowcount} rows affected ({(time() - start):.3f} sec)\n") if show else None

    @errorf()
    def insert(self, tbName: str = None, show: bool = True, **kwargs) -> None:
        """
        向数据表中添加数据.
        (Null和None关键字需要在开头添加/,如/None,/null.)

        插入数据::

            >>> sql.insert("tableName", label1="value1", label2="value2", other="/None")

        :param tbName: 数据表名.
        :type tbName: str
        :param show: 是否打印以展示.
        :type show: bool
        :keyword kwargs: 添加的数据,应形如'列名=对应数据'
        :type kwargs: ...
        :return: 返回什么.
        :retype: 返回值的类型
        """

        if tbName is None:
            tbName = self.tbName

        kwargs = self._checkDict(kwargs)

        start = time()

        print(
            f"mysql> insert into {tbName} \n    -> ({', '.join(kwargs.keys())})\n    -> values\n    -> ({', '.join(map(str, kwargs.values()))});") if show else None

        self._cursor.execute(
            f"insert into {tbName} ({', '.join(kwargs.keys())}) values ({', '.join(map(str, kwargs.values()))});")
        self._connect.commit()

        print(f"{self._op_feedback(spendtime=time() - start)}\n") if show else None

    @errorf()
    def update(self, tbName: str = None, condition: Literal["where ... in ...", "where ... and/or ..."] | str = None,
               show: bool = True, check: bool = True, **kwargs) -> None:
        """
        修改表中的数据.
        (Null和None关键字需要在开头添加/,如/None,/null.)

        修改::

            >>> sql.update(None, "where id = 1" other="info")

        :param tbName: 数据表名称.
        :type tbName: str
        :param condition: 形如`WHERE COLUMN1 > 0`的约束条件.
        :type condition: str
        :param show: 是否打印以展示.
        :type show: bool
        :param check: 是否进行安全检查.
        :type check: bool
        :keyword kwargs: 修改的数据,应形如'列名=对应数据',(仅输入需要修改的列即可.)
        :type kwargs: ...
        :return: 操作执行函数不做返回.
        :retype: None
        """

        if tbName is None:
            tbName = self.tbName

        self._security_check(check and (condition is None or "id" not in condition), warnstr="您没有输入用于索引的id值,"
                                                                                             "这可能会导致所有数据都被修改.您确定吗"
                                                                                             "?(Y.是, N.否)\n")

        kwargs = self._checkDict(kwargs)

        textlist = [f"{k}={kwargs[k]}" for k in kwargs]

        text = f"update {tbName} set {', '.join(textlist)}{';' if condition is None else f' {condition};'}"

        print(f"mysql> {text}") if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        print(f"{self._op_feedback(spendtime=time() - start)}\n") if show else None

    @errorf()
    def delete(self, tbName: str = None, *, condition: Literal["where ... and/or ..."] | str = None, show: bool = True,
               check: bool = True) -> None:
        """
        删除表中的一行,多行或所有数据.

        删除::

            >>> sql.delete(None, condition="where id > 0")

        :param tbName: 数据表名称.
        :type tbName: str
        :param condition: 形如`WHERE COLUMN1 > 0`的约束条件.
        :type condition: str
        :param show: 是否打印以展示.
        :type show: bool
        :param check: 是否进行安全检查.
        :type check: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        if tbName is None:
            tbName = self.tbName

        self._security_check(check and condition is None, warnstr="此操作将删除所有值,确定继续吗?(Y.是, N.否)\n")

        text = f"delete from {tbName}{'' if condition is None else f' {condition}'};"

        print("mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        print(f"{self._op_feedback(spendtime=time() - start)}\n") if show else None

    @errorf()
    def column_add(self, tbName: str = None, columnName: str = None, dataType: str = None, *, First: bool = False,
                   After: Literal["columnName"] = None, notNull: bool = False, show: bool = True) -> None:
        """
        向数据表中添加列.

        添加列::

            >>> sql.column_add(None, "newLabel", "varchar(64)", After="aimLabel", notNull=False)

        :param tbName: 表名.
        :type tbName: str
        :param columnName: 新列名.
        :type columnName: str
        :param dataType: 数据类型.
        :type dataType: str
        :keyword First: 插入到所有列之前.
        :type First: bool
        :keyword After: 插入到某一列之后,应输入目标的列名,且不可于First同时使用.
        :type After: str
        :keyword notNull: 是否可为空.
        :type notNull: bool
        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        self._checkParam(self.column_add, columnName, "columnName")
        self._checkParam(self.column_add, dataType, "dataType")

        if First and After is not None:
            raise TypeError(f"The 'First' and 'After' parameters cannot be set simultaneously")

        if tbName is None:
            tbName = self.tbName

        text = f"alter table {tbName} add {columnName} {dataType}{' not null' if notNull else ''}{' first' if First else ''}{'' if After is None else f' after {After}'};"

        print("mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        if show:
            print(f"{self._op_feedback(spendtime=time() - start)}")
            print(f"{self._alter_feedback()}\n")

    @errorf()
    def column_drop(self, tbName: str = None, columnName: str = None, *, show: bool = True, check: bool = True) -> None:
        """
        删除数据表中的某一列.

        删除::

            >>> sql.column_drop(None, "dropLabel")

        :param tbName: 表名.
        :type tbName: str
        :param columnName: 要删除的列名.
        :type columnName: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :keyword check: 是否进行安全检查.
        :type check: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        self._checkParam(self.column_drop, columnName, 'columnName')

        if tbName is None:
            tbName = self.tbName

        self._security_check(check)

        text = f"alter table {tbName} drop {columnName};"

        print("mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        if show:
            print(f"{self._op_feedback(spendtime=time() - start)}")
            print(f"{self._alter_feedback()}\n")

    @errorf()
    def column_modify(self, tbName: str = None, columnName: str = None, dataType: str = None, *, NoNULL: bool = False,
                      default: str = None, show: bool = True) -> None:
        """
        对表的定义进行修改.

        修改::

            >>> sql.column_modify(None, "label", "varchar(64)", NoNULL=False)

        :param tbName: 表名.
        :type tbName: str
        :param columnName: 列名.
        :type columnName: str
        :param dataType: 数据类型.
        :type dataType: str
        :param NoNULL: 是否可为空.
        :type NoNULL: bool
        :param default: 设置的默认值.
        :type default: str
        :param show: 是否打印以展示.
        :type show: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        self._checkParam(self.column_modify, columnName, "columnName")
        self._checkParam(self.column_modify, dataType, "dataType")

        if tbName is None:
            tbName = self.tbName

        text = f"alter table {tbName} modify {columnName} {dataType}{' not null' if NoNULL else ''}{'' if default is None else f' default {default}'};"

        print("mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        if show:
            print(f"{self._op_feedback(spendtime=time() - start)}")
            print(f"{self._alter_feedback()}\n")

    @errorf()
    def column_default(self, tbName: str = None, columnName: str = None, defValue: str = None, *,
                       show: bool = True) -> None:
        """
        设置或修改列默认值.

        设置默认值::

            >>> sql.column_default(None, "label", "value")

        :param tbName: 表名.
        :type tbName: str
        :param columnName: 列名.
        :type columnName: str
        :param defValue: 设置的默认值.
        :type defValue: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        self._checkParam(self.column_default, columnName, "columnName")
        self._checkParam(self.column_default, defValue, "defVelue")

        if tbName is None:
            tbName = self.tbName

        text = f"alter table {tbName} alter {columnName} set default {defValue};"

        print("mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        if show:
            print(f"{self._op_feedback(spendtime=time() - start)}")
            print(f"{self._alter_feedback()}\n")

    @errorf()
    def column_dropDef(self, tbName: str = None, columnName: str = None, *, show: bool = True) -> None:
        """
        删除列的默认值.

        :param tbName: 表名.
        :type tbName: str
        :param columnName: 列名.
        :type columnName: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        self._checkParam(self.column_dropDef, columnName, "columnName")

        if tbName is None:
            tbName = self.tbName

        text = f"alter table {tbName} alter {columnName} drop default;"

        print("mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        if show:
            print(f"{self._op_feedback(spendtime=time() - start)}\n")
            print(f"{self._alter_feedback()}\n")

    @errorf()
    def tbName_modify(self, tbName: str = None, newTbName: str = None, *, show: bool = True) -> None:
        """
        修改数据表名.

        :param tbName: 表名.
        :type tbName: str
        :param newTbName: 新的表名.
        :type newTbName: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        self._checkParam(self.tbName_modify, newTbName, "newTbName")

        if tbName is None:
            tbName = self.tbName

        text = f"alter table {tbName} rename to {newTbName}"

        print("mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        if show:
            print(f"{self._op_feedback(spendtime=time() - start)}")
            print(f"{self._alter_feedback()}\n")

    @errorf()
    def column_change(self, tbName: str = None, columnName: str = None, newColumnName: str = None, dataType: str = None,
                      *, show: bool = True) -> None:
        """
        对表进行change修改.

        :param tbName: 表名.
        :type tbName: str
        :param columnName: 列名.
        :type columnName: str
        :param newColumnName: 新的列名.
        :type newColumnName: str
        :param dataType: 数据类型.
        :type dataType: str
        :keyword show: 是否打印以展示.
        :type show: bool
        :return: 操作执行函数不做返回.
        :retype: None
        """

        self._checkParam(self.column_change, columnName, "columnName")
        self._checkParam(self.column_change, newColumnName, "newColumnName")
        self._checkParam(self.column_change, dataType, "dataType")

        if tbName is None:
            tbName = self.tbName

        text = f"alter table {tbName} change {columnName} {newColumnName} {dataType};"

        print("mysql> " + text) if show else None

        start = time()

        self._cursor.execute(text)
        self._connect.commit()

        if show:
            print(f"{self._op_feedback(spendtime=time() - start)}")
            print(f"{self._alter_feedback()}\n")

    @errorf()
    def executeOhter(self, command: str = None, *, _input: bool = False, allowprint: bool = False,
                     circulate: bool = False) -> EllipsisType:
        """
        执行其它命令.

        当关键字参数_input, allowprint, circulate同时启用时将会模拟mysql终端.
        但是单独启用_input或circulate关键字参数都是没有意义的或会引发错误的.

        :param command: 命令.
        :type command: str
        :keyword _input: 是否进行手动循环输入.
        :type _input: bool
        :keyword allowprint: 是否允许打印.
        :type allowprint: bool
        :keyword circulate: 是否循环.
        :type circulate: bool
        :return: 结果.
        """

        while True:
            if _input:

                times = 0
                commandlist = []

                while True:
                    command = input("mysql> " if times == 0 else "    -> ")
                    commandlist.append(command)
                    if command and command[-1] == ";":
                        break

                    times += 1

                command = "".join(commandlist)
                if "quit" in command.lower(): break

                start = time()

                self._cursor.execute(command)
                self._connect.commit()

                res = self._cursor.fetchall()

                if allowprint:

                    if isinstance(res, Container):

                        if res and (column := self.COLUMN):

                            if len(column) == 1:
                                print(self._to_show(column[0], [i[0] for i in res], spendtime=time() - start))
                            elif len(column) > 1:
                                print(self._mutlishow(column, list(res), spendtime=time() - start))
                            else:
                                print(f"{self._empty_feedback(spendtime=time() - start)}\n")

                        else:
                            print(f"{self._op_feedback(spendtime=time() - start)}\n")

                    else:
                        print(res)

                else:
                    return res

            else:
                self._cursor.execute(command)
                self._connect.commit()

                print(self._cursor.fetchall())

            if not circulate: break

    @errorf()
    def to_csv(self, csv_path: str, tbName: str, *,
               condition: Literal["where ... = ...", "where ... and/or ..."] | str = None) -> None:
        """
        将数据库导出为csv文件.

        :param csv_path: csv文件路径.
        :type csv_path: str
        :param tbName: 数据表名称.
        :type tbName: str
        :keyword condition: 对取出的数据的mysql语法限定.
        :type condition: str
        :return: 操作执行函数不做返回.
        :retype: None
        """

        velous = self.showTableContent(tbName, show=False) if condition is None else self.selectColumn(columns=("*",),
                                                                                                       condition=condition,
                                                                                                       show=False)

        with open(csv_path, "w", encoding="gbk", newline="") as file:
            w = writer(file)
            w.writerow(self.COLUMN)
            for row in velous:
                w.writerow(row)

    @errorf()
    def csv_to_mysql(self, csv_path: str, tbName: str) -> None:
        """
        将csv文件导入为数据表.

        :param csv_path: csv文件路径.
        :type csv_path: str
        :param tbName: 数据表名称.
        :type tbName: str
        :return: 操作执行函数不做返回.
        :retype: None
        """

        with open(csv_path, "r", encoding="gbk") as file:
            r = list(reader(file))

        df = DataFrame(r[1:], columns=r[0])

        column = df.columns

        for i in range(len(r) - 1):
            self.insert(tbName, **{k: (v if v else NULL) for k, v in zip(column, list(df.iloc[i]))})

    @errorf()
    def table_to_DataFrame(self, tbName: str) -> DataFrame:
        """
        将数据表转换为DataFrame.

        :param tbName: 数据表名称.
        :type tbName: str
        :return: DataFrame形式的数据表.
        :retype: DataFrame
        """
        return DataFrame({k: self.selectColumn(tbName, (k,), show=False) for k in self.getColumn(tbName)})

    def checkId(self, tbName: str = None, *, firstNum: int = 1) -> None:
        """
        遍历数据表的id索引值,检测id是否连续以判断是缺漏数据.

        :param tbName: 需要检测的数据表名
        :type tbName: str
        :param firstNum: 首个索引的值
        :type firstNum: int
        :return: 操作执行函数不做返回
        :rtype: None
        """

        if tbName is None:
            tbName = self.tbName

        for i in self.showTableContent(tbName, show=False):
            if firstNum != i[0]: raise ValueError(f"第{firstNum}个缺失.")
            firstNum += 1

        print("检测完毕,没有检测到缺失.")

    @errorf()
    def randomChoice(self, tbName: str = None, *,
                     condition: Literal["where ... in ...", "where ... and/or ..."] | str = None,
                     limit: int = 1) -> list:
        """
        随机选择数据表中的`limit`条数据

        :param tbName: 数据表名
        :type tbName: str
        :param condition: 对取出数据的mysql语法限定.
        :type condition: str
        :param limit: 要求输出多少条随机数据
        :type limit: int
        :return: 有随机数据组成的列表
        :rtype: list
        """

        if tbName is None:
            tbName = self.tbName

        self._cursor.execute(
            f"SELECT * FROM {tbName}{'' if condition is None else ' ' + condition} ORDER BY RAND() LIMIT {limit};")
        self._connect.commit()

        return list(self._cursor.fetchall())


if __name__ == '__main__':
    sql = baseSQL("root", "135246qq", "temp")
    # sql.executeOhter(_input=True, allowprint=True, circulate=True)
    # sql.createTable("users", True, username=(('v', 50), False, False, False), age=(('i', ),), email=(('v', 50),))
    # sql.createTable("orders", False, ordername=(('v', 50), False, False, False), orderid=(('i', ),), count=(('i', ),), date=(('d', ),))
    # sql.dropDB("test1")
    # sql.insert("users", username="v", age=20, email="v@v.v")
    # sql.insert("orders", ordername="v", orderid=1, count=2, date="2022-01-01")
    sql.selectColumn("users", ("username", ))
    sql.selectColumn("orders", ("count", ))
    pass
