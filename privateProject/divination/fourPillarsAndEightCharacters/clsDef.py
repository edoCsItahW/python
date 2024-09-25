#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/9/18 下午6:50
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------

__all__ = [
    "TianGan",
    "DiZhi",
    "Zhu",
    "SZBZ"
]

from netTools import request
from typing import Any, Literal, overload, NoReturn, Self
from enum import Enum
from functools import singledispatchmethod


class YinYang(Enum):
    YIN = "Yin"
    YANG = "Yang"


class GanZhiBase:
    @overload
    def __new__(cls, num: int): ...

    @overload
    def __new__(cls, name: str): ...

    def __new__(cls, *args, **kwargs):
        return cls.__getitem__(args[0])

    @classmethod
    def __getitem__(cls, item: Any):
        if isinstance(item, int):
            return DIZHIS[item]
        if isinstance(item, str):
            return next(filter(lambda x: x.name == item, DIZHIS))
        raise TypeError(
            f"Invalid argument type: {type(item).__name__}")


class _GanZhiBase:
    def __init__(self, name: str, *, gender: YinYang):
        self._name = name
        self._gender = gender

    @property
    def gender(self) -> YinYang:
        return self._gender

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name


class _TianGan(_GanZhiBase):
    ...


class TianGan(GanZhiBase):
    ...


class _DiZhi(_GanZhiBase):
    ...


class DiZhi(GanZhiBase):
    ...


TIANGANS = [
    _TianGan("甲", gender=YinYang.YANG),
    _TianGan("乙", gender=YinYang.YIN),
    _TianGan("丙", gender=YinYang.YANG),
    _TianGan("丁", gender=YinYang.YIN),
    _TianGan("戊", gender=YinYang.YANG),
    _TianGan("己", gender=YinYang.YIN),
    _TianGan("庚", gender=YinYang.YANG),
    _TianGan("辛", gender=YinYang.YIN),
    _TianGan("壬", gender=YinYang.YANG),
    _TianGan("癸", gender=YinYang.YIN),
]


DIZHIS = [
    _DiZhi("子", gender=YinYang.YANG),
]


class Zhu:
    @overload
    def __init__(self, num: int) -> None: ...

    @overload
    def __init__(self, num: str) -> None: ...

    def __init__(self, *args):
        match len(args):
            case 1:
                if isinstance(a := args[0], str):
                    self._gan, self._zhi = TianGan(a[0]), DiZhi(a[1])

    def __repr__(self) -> str:
        return f"<干: {self._gan.name}, 支: {self._zhi.name}>"


class SZBZ:
    Keys = Literal['year', 'month', 'day', 'hour', 'GregorianDateTime', 'LunarDateTime', 'LunarShow', 'IsJieJia', 'LJie', 'GJie', 'Yi', 'Ji', 'ShenWei', 'Taishen', 'Chong', 'SuiSha', 'WuxingJiazi', 'WuxingNaYear', 'WuxingNaMonth', 'WuxingNaDay', 'MoonName', 'XingEast', 'XingWest', 'PengZu', 'JianShen', 'TianGanDiZhiYear', 'TianGanDiZhiMonth', 'TianGanDiZhiDay', 'LMonthName', 'LYear', 'LMonth', 'LDay', 'SolarTermName']

    def __init__(self, *args) -> None:
        match len(args):
            case 3 | 4:
                self._year, self._month, self._day = args[:3]
                self._hour = args[3] if len(args) == 4 else 0
                self.__dict__['_value'] = (_ := self.now(self._year, self._month, self._day, self._hour))
                self._value = _

    @classmethod
    def now(cls, year: int, month: int, day: int, hour: int = 0):
        return eval(request("https://www.36jxs.com/api/Commonweal/almanac", params={"sun": '-'.join(map(str, [year, month, day]))}).getsoup().text)["data"]

    @property
    def year(self) -> Zhu:
        return Zhu(self._year)

    @property
    def month(self) -> Zhu:
        return Zhu(self._month)

    @property
    def day(self) -> Zhu:
        return Zhu(self._day)

    def __getitem__(self, item: Keys) -> Any:
        if item in self._value:
            return self._value[item]
        raise KeyError(
            f"Invalid key: {item}")

    def __getattr__(self, item: Keys) -> Any:
        if item in (v := self.__dict__['_value']):
            return v[item]


