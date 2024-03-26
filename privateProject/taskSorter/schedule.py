#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/10 17:30
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
"""
任务分配的时间可以根据以下属性进行分配：

任务的优先级：优先级高的任务可以分配更多的时间，以确保它们在截止日期之前完成。0.2

任务的难度：难度大的任务可能需要更多的时间来完成。0.1

任务的紧急程度：如果任务的截止日期很近，那么需要分配更多的时间来确保任务能够按时完成。0.2

任务的重要性：如果任务对于项目或组织的成功非常重要，那么需要分配更多的时间来确保任务能够完成得很好。0.2

任务的复杂性：如果任务需要完成多个步骤或涉及多个团队或部门，那么可能需要更多的时间来完成任务。0.1

任务的资源需求：如果任务需要特殊的设备、技能或资金，那么可能需要更多的时间来准备这些资源。0.1

任务的风险程度：如果任务涉及高风险活动，那么可能需要分配更多的时间来确保任务能够安全完成。0.1
"""
from conFunc import sequence, Table, Arrange
from calendar import calendar, month, monthcalendar
from datetime import date, datetime
from pandas import DataFrame
from numpy import array, ndarray, hstack, vstack, full
from typing import Sequence
from collections.abc import Collection
from abc import ABC, abstractmethod


class task:
    def __init__(self, start: datetime | str, end: datetime | str, taskName: str, *, todo: str = None):
        self._start = start
        self._end = end
        self.name = taskName
        self.todo = todo

    def __repr__(self):
        Day = self.start.date() if self.start.date() == self.end.date() else f"{self.start.date()}-{self.end.date()}"
        return f"任务名:{self.name},日期:{self.start.date()},时限:({self.start.time()}-{self.end.time()}),任务:{self.todo}"

    @property
    def start(self):
        if isinstance(self._start, datetime): return self._start
        elif isinstance(self._start, str): return datetime.fromisoformat(self._start)
        else: raise ValueError("参数start仅允许datetime和str类型.")

    @property
    def end(self):
        if isinstance(self._end, datetime): return self._end
        elif isinstance(self._end, str): return datetime.fromisoformat(self._end)
        else: raise ValueError("参数end仅允许datetime和str类型.")


class timeBase(ABC):
    def __init__(self, data: ..., column: ...):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @property
    @abstractmethod
    def column(self):
        pass

    @staticmethod
    @abstractmethod
    def _toTable(*args) -> str:
        pass

    @abstractmethod
    def toDict(self) -> dict:
        pass


class day(Collection, timeBase):
    def __init__(self, data: ndarray | list, column: ... = None, *, Date: str = None):
        self._column = column
        self._data = data
        self._null = "None"
        self._date = Date

    def __iter__(self):
        yield from self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        if not isinstance(item, int): raise TypeError(f"索引值应为数组,而你的输入'{item}'.")
        return self.data[item]

    def __contains__(self, __x):
        if __x in self.data: return True

    def __repr__(self):
        dataDict = {str(self.column) if isinstance(self.column, list) else self.column: self.data}
        return self._toTable(dataDict)

    def __add__(self, other):
        if isinstance(other, day):

            lenDict = {len(self.data): (self.data, other.data), len(other.data): (other.data, self.data)}

            maxLen = max(lenDict.keys())

            lener, shorter = lenDict[maxLen]

            shorter += (2 * maxLen - sum(lenDict.keys())) * [self._null]

            if maxLen == len(self.data):
                item = (shorter, lener)
            else:
                item = (lener, shorter)

            return Schedule(array(list(map(list, zip(*item)))), [self.column, other.column])
        elif isinstance(other, Schedule):
            print("day -> Schedule")
            # TODO: (10.26)添加支持Schedule的加法运算.
            pass
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'day' and '{type(other).__name__}'")

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    @property
    def date(self):
        if self._date is not None:
            try:
                return date.fromisoformat(self._date)
            except Exception as e:
                print(f"格式错误:{e},应如2020-10-01")

    @property
    def data(self):
        if isinstance(self._data, ndarray) and len(self._data.shape) > 1: raise ValueError(
            "不支持高维数组,如需包含列表元素,请使用list而不是ndarray.")
        return self._data

    @property
    def column(self):
        return str(self._column) if isinstance(self._column,
                                               Sequence) else self._column if self._column is not None else "empty"

    def dict(self): return {self.column: self.data}

    @staticmethod
    def _toTable(dataDict: dict):
        column, data = list(dataDict.items())[0]

        return str(Arrange(data, column))

    def toDict(self) -> dict:
        return {self.column: self.data}


class Schedule(Collection, timeBase):
    def __new__(cls, *args, **kwargs):
        if args[0] is not None and len(args[0].shape) == 1:

            if len(args) == 1: args = (args[0], None)

            return day(list(args[0]), None if args[1] is None else args[1])

        else:
            return super().__new__(cls)

    def __init__(self, data: ndarray = None, column: list = None, *, week: bool = False):
        self._data = data
        self._column = column
        self._emptyStr = "Empty Schedule"
        self._defaultColumn = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self._week = week
        self._null = "None"
        if self._week is not None and self._data is not None and (
                data.shape[0] if len(self.data.shape) == 1 else self.data.shape[1]) != (
                7 if column is None else len(self._column)):
            raise ValueError(
                f"data的列长: '{self.data.shape[0] if len(self.data.shape) == 1 else self.data.shape[1]}',与列名长度: '{0 if self._column is None else len(self._column)}'不符.")

        self.nowTime = date.today()
        self.monthStr = month(
            int((TIME := str(self.nowTime).split("-"))[0]),
            int(TIME[1])
        )
        self.thisMonth = DataFrame(data=array(monthcalendar(2023, 10)), columns=self.getDayName)

    def __len__(self):
        pass

    def __iter__(self):
        pass

    def __contains__(self, __x):
        pass

    def __repr__(self):
        if self.data is None: return self._emptySchedule

        return self._toTable(self.data, column=self._defaultColumn if self._week else sequence(
            self.data.shape[0]) if self._column is None else self._column)

    def __add__(self, other):
        if isinstance(other, day):

            lenDict = {self.data.shape[0]: (self.data, other.data), len(other.data): (other.data, self.data)}

            maxLen = max(lenDict.keys())

            lener, shorter = lenDict[maxLen]

            if isinstance(lener, ndarray):
                data = hstack(
                    (lener, array([[i] for i in shorter + [self._null] * (2 * maxLen - sum(lenDict.keys()))])))
            elif isinstance(lener, list):
                data = vstack((shorter, full((2 * maxLen - sum(lenDict.keys()), self.data.shape[1]), self._null)))
                data = hstack((data, array([[i] for i in lener])))
            else:
                raise ValueError("an unknow error.")

            return Schedule(data, self.column + [other.column])

        elif isinstance(other, Schedule):
            # TODO: (10.26)This
            print("Schedule -> Schedule")
            pass

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'day' and '{type(other).__name__}'")

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    @property
    def data(self):
        if isinstance(self._data, ndarray):
            return self._data
        elif isinstance(self._data, list):
            return array(self._data)
        elif self._data is None:
            return None
        else:
            raise ValueError(f"参数data可以是ndarry类型和list类型,但不能为其它类型,你的输入{type(self._data)}")

    @property
    def column(self):
        return self._column  # 由于参数data为单列的会被__new__直接返回为day类,所以无需再归一化.

    @property
    def getDayName(self):
        return [i for i in self.monthStr.replace("\n", " ").split(" ")
                if not i.isdigit() and i and len(i) == 2]

    @property
    def _emptySchedule(self):
        line = "+" + (strLen := len(self._emptyStr) + 2) * "-" + "+"
        head = "\n| " + self._emptyStr + " |\n"
        return line + head + line

    @staticmethod
    def _toTable(data: ndarray | dict, column: list = None):
        return str(Table(data, column))

    def toDict(self) -> dict:
        pass


class timeManger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.coedict: dict = {
            "急迫性":   42,
            "难度":     13,
            "重要性":   20,
            "资源要求": 11,
            "风险":     14
        }  # coefficient

    def createTask(self) -> ndarray:

        levellist = [
            ["明天", "三天后", "一周后", "半个月后", "一个月后", "三个月后", "半年后", "一年后", "三年后", "十年后"],
            ["当前不可及", "涉及数理", "涉及背诵", "涉及编程", "轻而易举", "走个过场"],
            ["必须完成", "次重要", "较为重要", "尝试完成", "有无皆可", "附加技能"],
            ["无需外物", "可有可无", "物品明确", "中心物品"],
            ["为眼下而学", "为毕业而学", "为就业而学", "为兴趣而学"]
        ]

        def checkInp(tag: str, leve: list):
            while not (inp := input(f"请输入{tag}的值(重要性从上至下):\n" + "".join(
                    [f"\t{i}.{v}\n" for i, v in enumerate(leve, start=1)]
            ) + "输入:")) or inp not in map(str, list(range(1, 10))):
                print(f"非法输入'{inp}'")

            return int(inp)

        inplist = array(
            list(
                reversed(
                    [checkInp(tag, leve) for tag, leve in zip(self.coedict.keys(), levellist)]
                )
            )
        )

        return inplist @ array(list(self.coedict.values()))


if __name__ == '__main__':
    # t = timeManger()
    # t.createTask()

    # print(Schedule())
    day1 = day(["边缘计算", "创新创业方法"], "星期一", Date="2023-10-23")
    day2 = day(["机器视觉", "高数", "人工智能"], "星期二", Date="2023-10-24")
    day3 = day(["创新思维"], "星期三", Date="2023-10-25")
    day4 = day(["大数据", "ps"], "星期四", Date="2023-10-26")
    day5 = day(["ardino"], "星期五", Date="2023-10-27")
    # new = Schedule(array(["2", 2, 3, 4, 5, 6, 7]), week=True)
    # print(new)
    print(day1 + day2 + day3 + day4 + day5)
    pass
