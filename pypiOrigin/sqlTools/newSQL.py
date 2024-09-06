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
from typing import Callable, Final, final
from functools import wraps
from pymysql import Error, connect
from pymysql.cursors import Cursor
from enum import Enum


def stderr(msg: str) -> None:
    print(f"\033[31m{msg}\033[0m")


def errorf(errorindex: str = "10000") -> Callable:
    """
    用于将baseSql的错误输出转换为mysql格式的装饰器.

    :param errorindex: 错误的状态码,由于无法获取,该值需要手动设定.
    :type errorindex: str
    :return: 装饰后的函数.
    :retype: Callable
    """

    def getfunc(func: Callable) -> Callable:
        @wraps(func)
        def warp(*args, **kwargs) -> Callable:
            try:
                return func(*args, **kwargs)
            except Error as e:
                if isinstance(e.args, tuple):
                    stderr(f"ERROR {e.args[0]} ({errorindex}): {e.args[1]}")
                else:
                    stderr(f"Other Error: {e}")

        return warp

    return getfunc


class Type(Enum):
    """
    定义数据类型枚举.
    """
    VARCHAR = "varchar"
    INT = "int"
    CHAR = "char"
    DATE = "date"
    FLOAT = "float"
    TIME = "time"
    BOOLEAN = "boolean"


class Feedback:
    """
    定义反馈类,用于处理mysql的反馈信息.
    """
    @staticmethod
    def normal(listlen: int, *, spendtime: float = 0.00) -> str:
        """
        返回mysql中展示表的反馈(这其中并没有换行符,你需要根据实际的数据库反馈来在使用的字符串前后添加换行符).

        :param listlen: 数据表的行数
        :type listlen: int
        :param spendtime: 运行耗时
        :type spendtime: float
        :return: 返回填充后的字符串.
        :retype: str
        """
        return f"{listlen} row{'s' if listlen != 1 else ''} in set ({spendtime:.3f} sec)"

    @staticmethod
    def option(cursor: Cursor, spendtime: float = 0.00) -> str:
        """
        返回mysql中操作命令的反馈(这其中并没有换行符,你需要根据实际的数据库反馈来在使用的字符串前后添加换行符).

        :param spendtime: 运行耗时.
        :type spendtime: float
        :return: 填充后的字符串.
        :retype: str
        """
        return f"Query OK, {cursor.rowcount} rows affected ({spendtime:.3f} sec)"

    @staticmethod
    def empty(*, spendtime: float = 0.00) -> str:
        """
        mysql对于空表的反馈.

        :param spendtime: 运行耗时.
        :type spendtime: float
        :return: 填充后的字符串.
        :retype: str
        """
        return f"Empty set ({spendtime:.3f} sec)"

    @staticmethod
    def alter(cursor: Cursor) -> str:
        """
        mysql中修改列的反馈.

        :return: 填充后的字符串.
        :retype: str
        """
        return f"Records: {cursor.rowcount}  Duplicates: 0  Warnings: 0"


class MySQL:
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
        self._database = database
        self._connect = connect(host=host, user=user, password=password, database=database)
        self._cursor = self._connect.cursor()
        self._tbName = tableName

    @final
    def _singleForm(self, title: str, conlist: list[str], *, spendtime: float = None) -> str:
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
        conlist = [str(i).strip() for i in conlist]

        maxlen = max(getWidth(title), max(getWidth(i) for i in conlist))

        line = "+" + "-" * (maxlen + 2) + "+"

        head = f"{line}\n| {title:<{maxlen - getWidth(title)}} |\n{line}\n"

        for content in conlist:
            head += f"| {content:<{maxlen - getWidth(title)}} |\n"
        head += line + f"\n{Feedback.normal(len(conlist), spendtime=spendtime)}\n"

        return head

    @final
    def _mutliForm(self, columlist: list[str], conlist: list[tuple], *, spendtime: float = None) -> str:
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
        conlist = [str(i).strip() for i in conlist]

        if (conl := len(columlist)) != (cl := len(conlist[0])):
            raise ValueError(  # List length error
                f"列名列表长度必须与每行元素个数一致,{columlist}长为{conl},{conlist[0]}长为{cl}")

        lenlist = [max([4 if (l := alist[i]) is None else getWidth(l) for alist in conlist]) for i in
                   range(len(conlist[0]))]

        maxlen = [c if (c := getWidth(colum)) > wordlen else wordlen for colum, wordlen in zip(columlist, lenlist)]

        head = (line := "+") + "\n"

        for l in maxlen:
            line += f"{(l + 2) * '-'}+"

        for i, colum in enumerate(columlist):
            head += f"| {colum:<{maxlen[i] - getWidth(colum)}} "

        head += f"|\n{line}\n"

        for content in conlist:
            for i, word in enumerate(content):
                head += f"| {word}{(maxlen[i] - (4 if word is None else getWidth(word))) * ' '} "
            head += "|\n"

        head += f"{line}\n{Feedback.normal(len(conlist), spendtime=spendtime)}\n"

        return head

