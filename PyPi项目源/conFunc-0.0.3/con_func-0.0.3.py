#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/20 20:01
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
# coding=utf-8
from __future__ import annotations

from collections.abc import Container
from textTools import getWidth
from functools import cache
from threading import Thread, Event
from typing import Union, Iterable, Literal, TypeGuard, Callable, Sequence
from queue import Queue as tQueue
from numpy import ndarray, array
from math import floor, sqrt
from time import sleep
from sys import stdout
from re import findall

__all__ = [
    "backlist",
    "decrypt",
    "find_factors",
    "partitem",
    "pathFinder",
    "returnAllpath",
    "sequence",
    "splitList",
    "square",
    "supcount",
    "temPrint",
    "waiter",
    "Table",
    "Arrange",
    "getFuncVars"
]


# source: docstring
def find_factors(n: int) -> tuple:
    """
    寻找质因数.

    :param n: 目标数字.
    :type n: int
    :return: 由质数和因数构成的元组.
    :retype: tuple
    """

    # 计算 n 的平方根
    a = int(sqrt(n))

    # 如果 n 的平方根是整数，则直接返回结果
    if a * a == n:
        return a, a

    # 向下搜索
    for b in range(a, 0, -1):
        if n % b == 0:
            return min(b, n // b), max(b, n // b)

    # 向上搜索
    for b in range(a + 1, n):
        if n % b == 0:
            return min(b, n // b), max(b, n // b)

    # 如果都没有找到，则说明 n 是质数
    return 1, n


def supcount(aimstr: str | list, *args: int | str | float):
    """
    计算除第一个参数以外的参数在第一个参数里出现的次数

    :data aimstr: 目标变量
    :type aimstr: Union[str, list]
    :return: 对应参数在目标变量中出现的个数.
    :retype: dict
    """
    return {str(k): aimstr.count(k) for k in args}


class pathFinder:
    """
    由棋盘路径计数问题引出
    问:从一个对角线的起点到另一个对角线的终点,只能向右或向下移动,
    且不能再次移动到已经路过的格子,有多少种不同的路径可以到达终点.
    这里通过递归创建类来实现

    # 这里将上一个格子创建的类称为当前格子的类的父类,同理下一个格子的类称为子类
    该类作为一个数据记录类,做着接受父类传递的历史路径,并为下一个格子创建一个类,
    将当前格子的坐标添加到历史路径列表之后传给子类的工作.
    该类不能单独运行,需要借助外部函数returnAllpath来启动,递归和输出.

    Attributes:
        size: 棋盘的尺寸限定为正方形.
        pos: 起始位置.(默认为(1, 1)并且父类的位置就是子类的起始位置)
        x: 起始位置的x坐标
        y: 起始位置的y坐标
        all: 将传递给子类的历史位置
        lastlist: 不包含当前位置的路径历史
    Methods:
        logtimes: 测试工具,启用将导入heartrate模块,这个模块会打开一个浏览器,浏览器会显示栈和每步代码执行的次数.
        nextpos: 计算并排除超出范围和在历史路径中的下一步的可能位置,也作为到达重点和陷入死路的判断条件.
        logRes_CreateLast: 该方法将会对nextpos的列表做判断,为空则记录,不为空则为每一个路径创建一个实例.
    """

    def __init__(self, size: int, *, bepos: tuple = (1, 1), lastlist: TypeGuard[list[int]] = None):
        if lastlist is None:
            lastlist = []
        self.size = size
        self.pos = bepos
        self.x, self.y = bepos[0], bepos[1]
        self.all = lastlist + [bepos]
        self.lastlist = lastlist

    @staticmethod
    def logtimes(allowlog: bool):
        if __name__ == "__main__" and allowlog:
            __import__("heartrate").trace(browser=True)

    @cache
    def nextpos(self):
        x, y = self.x, self.y
        return [] if self.pos == (self.size, self.size) \
            else [i for i in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
                  if i[0] != 0 and i[1] != 0
                  and i[0] != self.size + 1 and i[1] != self.size + 1
                  and i not in self.lastlist]

    def logRes_CreateLast(self):
        if not self.nextpos():
            globals()['finall'].append(self.all)
            return self.all
        for pos in pathFinder.nextpos(self):
            instance = pathFinder(self.size, bepos=pos, lastlist=self.all)
            yield instance


def returnAllpath(size: int, outtype: int = 0):
    """
    用于获取方形网格中从坐标(1, 1)移动至其对角的位置的所有路径.

    :param size: 网格的边长
    :type size: int
    :param outtype: 输出结果,1将输出正确结果,-1输出死路结果,其它输出全部.(默认为0)
    :return: 包含所有路径的列表.
    :retype: list
    """

    def enginerun(insiter: Iterable):
        for instance in insiter:
            enginerun(instance.logRes_CreateLast())

    globals()['finall'] = []

    enginerun(pathFinder(size).logRes_CreateLast())
    if outtype == 1:
        return [i for i in globals()['finall'] if (size, size) in i]
    elif outtype == -1:
        return [i for i in globals()['finall'] if (size, size) not in i]
    else:
        return globals()['finall']


def splitList(aimlist: list, part: int) -> list[list]:
    """
    分割列表.

    :param aimlist: 被作用的列表.
    :type aimlist: list
    :param part: 要分成多少分.
    :type part: int
    :return: 分割后的多个列表.
    :retype: list
    """
    long = len(aimlist)
    wigth = floor(long / part)
    return [aimlist[i:i + wigth] for i in range(0, long, wigth if wigth else 1)]


class waiter(Thread):
    """
    一个等待动画

    Attributes:
        length: 等待条长度.
        stop: 停止信号.(非用户参数)
        interval: 动画帧数.
        queue: 多线程队列.(非用户参数)
    Methods:
        print_last: 打印下一个.
        run: 循环核心.
        begin_wait: 开始等待.
        end_wait: 结束等待.
    """

    def __init__(self, length: int, stop: bool = True, interval: int = 0.3, queue: tQueue = None):
        super().__init__()
        self.right, self.left = "\u25c9", "\u25cb"
        self.stop = stop
        self.length = length
        self.interval = interval
        self.queue = queue if queue is not None else tQueue()
        self.event = Event()

    @staticmethod
    def print_last(updated_text: str):
        stdout.write(f"\r{updated_text}")
        stdout.flush()

    def run(self):
        while self.stop:
            for i in range(0, self.length + 1):
                if self.event.is_set():
                    waiter.print_last(f"end[{self.right * i}{self.left * (self.length - i)}]end")
                    return
                waiter.print_last(f"waitting...[{self.right * i}{self.left * (self.length - i)}]")
                sleep(self.interval)

    def begin_wait(self):
        self.event.clear()
        self.start()

    def end_wait(self):
        self.stop = False
        self.event.set()
        self.join()


def decrypt(text: str) -> str:
    """
    对一段文本进行编码及转码,使进制数转换为文字.

    :param text: 需要进行转换的文本.
    :type text: str
    :return: 转换后的文本.
    :retype: str
    """
    for i in findall(r"\\x\w{2}", text):
        text = text.replace(i, chr(int(i[-2:], 16)))
    for k in findall(r"\\u\w{4}", text):
        text = text.replace("\\" + k[-5:], chr(int(k[-4:], 16)))
    for v in findall(r"0x\w{2}", text):
        text = text.replace(v, chr(int(v[-2:], 16)))
    return text


def backlist(beginnum: int, endnum: int, *, x: int = 0, y: int = 0) -> list[tuple]:
    """
    制造类似
    "[(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3), (4, 5), (5, 4)]"
    的列表.

    :param beginnum: 起始数字,这决定了从哪个数字开始.
    :type beginnum: int
    :param endnum: 结束数字,这决定了列表中元素的个数.
    :type endnum: int
    :param x: 每个元组第1位数的偏移量,即当x=1时,所有元组的第一位加1.
    :type x: int
    :param y: 每个元组第2位数的偏移量,即当y=1时,所有元组的第二位加1.
    :return: 包含对应元组的列表.
    :retype: list
    """
    return [(x + (i // 2) + (i % 2), y + (i // 2) + ((i + 1) % 2)) for i in range(beginnum, endnum)]


def sequence(index: int | tuple | Container, *, start: int = 0) -> list:
    """
    使用数字,元组或其它容器类的长度快速生成列表.

    :param index:
        当index为整数时,将生成以0开头到index结尾的,间隔为1的列表.
        当index为元组时,将生成以元组第一位数至元组第二为数结尾的,间隔为1的列表.
        当index为其它容器时,将生成以0开头到由容器内元素个数决定的该容器的长度整数结尾的,间隔为1的列表.
    :type index: Container
    :return: 返回什么.
    :retype: 返回值的类型
    """
    if isinstance(index, int):
        return list(range(start, index))

    elif isinstance(index, tuple):
        return list(range(index[0], index[1]))

    return list(range(start, len(index)))


def square(start: int, end: int, part: int):
    """
    将数字平均分组.

    :param start: 初始数值
    :type start: int
    :param end: 结束数值
    :type end: int
    :param part: 份数
    :type part: int
    :return: 分组后的列表
    :rtype: list
    """

    if start < 0 or end <= 0 or part < 0:
        raise ValueError("存在不支持的参数")

    elif end - start < part:
        raise ValueError(f"无法将{end - start}个数字分成{part}组")

    partlen = (end - start) / part

    if isinstance(partlen, int) or str(partlen)[-2:] == ".0":
        return [(i, i + int(partlen) - 1) for i in range(start, end, int(partlen))]

    else:
        partlen = floor(partlen)
        return [(i, num if (num := (i + partlen - 1)) < end else end - 1) for i in range(start, end, partlen)]


def partitem(itemlist: list) -> list:
    """
    函数zip的逆函数,它将[(1, 2, ...), (3, 4, ...)]类型列表解包为[[1, 3, ...], [2, 4, ...]]

    :param itemlist: 目标列表.
    :type itemlist: list
    :return: 解包后的列表.
    :retype: list
    """
    return [[i[k] for i in itemlist] for k in range(len(itemlist[0]))]


def temPrint(text: ...) -> None:
    """
    可擦除打印,当使用该函数进行输出时,再次使用该函数输出可以请求上次的输出.

    :param text: 打印的目标.
    :type text: ...
    :return: 操作执行函数不做返回.
    :retype: None
    """
    stdout.write(f"\r{text}")
    stdout.flush()


class Arrange:
    def __init__(self, data: list, column: ..., *, Type: Literal["len", "wid"] = "wid"):
        self._data = data
        self._column = column
        self._type = Type

    def __repr__(self):
        head = f"{self.line}\n| {self.column}{(self.maxLen() - getWidth(self.column)) * ' '} |\n{self.line}\n"

        for content in self.data:
            head += f"| {content}{(self.maxLen() - getWidth(content)) * ' '} |\n"
        head += self.line
        return head

    @property
    def data(self):
        if not isinstance(self._data, list):
            if not isinstance(self._data, Sequence):
                return [self._data]
            return list(self._data)
        return self._data

    @property
    def column(self):
        if isinstance(self._column, Sequence):
            return str(self._column)
        return self._column

    @property
    def line(self): return f"+{'-' * (self.maxLen() + 2)}+"

    def dataLen(self):
        return list(map(
            lambda x: getWidth(str(x)) if self._type == "wid" else len(str(x)),
            self.data
        ))

    def maxLen(self): return d if (d := max(self.dataLen())) >= (c := len(self.column)) else c


class Table:
    def __init__(self, data: ndarray | list, column: list = None, *, title: str = None, Type: Literal["len", "wid"] = "wid"):
        self._data = data
        self._column = column
        self._title = title
        self._type = Type

    def lenMethod(self, any: ...): return getWidth(any) if self._type == "wid" else len(any)

    @property
    def data(self): return array(self._data) if isinstance(self._data, list) else self._data

    @property
    def column(self): return self._column

    @property
    def shape(self): return self.data.shape

    @property
    def dataColumnLen(self): return self.shape[0] if len(self.shape) == 1 else self.shape[1]

    @property
    def columnLen(self): return len(self.column)

    @property
    def shapeLen(self): return len(self.shape)

    @property
    def dataMaxLen(self):
        """
        计数出数据每一列的最大长度
        """
        return [max(map(lambda x: self.lenMethod(str(x)), self.data if self.shapeLen == 1 else self.data[:, i])) for i in range(self.dataColumnLen)]

    @property
    def finMaxLen(self):
        """
        将dataMaxLen与对应column的每一个元素的长度进行对比,获取最大的长度
        """
        return [max(d, c) for d, c in zip(self.dataMaxLen, map(lambda x: len(str(x)), self.column))]

    @property
    def line(self):
        """
        制作分割线
        """
        return "+" + "".join([f"{(i + 2) * '-'}+" for i in self.finMaxLen])

    @property
    def lineLen(self): return len(self.line)

    def __repr__(self):
        if self.dataColumnLen != self.columnLen: raise ValueError(f"数据元素个数: {self.dataColumnLen},与列数: {self.columnLen}不相等.")

        if self._title:
            # 头线
            upline = f"+{(self.lineLen - 2) * '-'}+\n"

            # 局中
            titleline = f"| {(rlen := floor((spacelen := (self.lineLen - 4 - self.lenMethod(self._title))) / 2)) * ' '}{self._title}{(spacelen - rlen) * ' '} |\n"

            # 合并
            title = upline + titleline

        # 制作表头
        head = f"{'' if self._title is None else self._title}{self.line}\n" + "".join([f"| {column}{(self.finMaxLen[i] - self.lenMethod(column)) * ' '} " for i, column in enumerate(self.column)]) + f"|\n{self.line}\n"

        # 向表中填充剩下的数据
        for idx in range(1 if self.shapeLen == 1 else self.shape[0]):
            for i, word in enumerate(self.data if self.shapeLen == 1 else self.data[idx]):
                head += f"| {word}{(self.finMaxLen[i] - (4 if word is None else self.lenMethod(str(word)))) * ' '} "
            head += "|\n"

        # 结尾
        head += f"{self.line}\n"

        return head


def getFuncVars(func: Callable):
    varTuple, varCount = (funcCode := func.__code__).co_varnames, funcCode.co_argcount
    return varTuple[:varCount]


if __name__ == '__main__':
    pass

