#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/1/12 15:47
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from abc import ABC, abstractmethod
from netTools import request
from warnings import warn
from typing import final, Literal, Iterator
from bs4 import BeautifulSoup
from methodDefine import dict1, dict2


springDoc = "春季为农历二月至四月以立春为始."
summerDoc = "夏季为农历五月至六月以立夏为始."
longsummerDoc = "长夏为农历的七月以夏至为始."
autumnDoc = "秋季为农历八月至十月以立秋为始."
winterDoc = "冬季为农历十一月至十二月以立冬为始."


def checkType(inType: type, normalType: type | tuple[type]):
    if not isinstance(inType, tuple([i.__class__ for i in normalType]) if isinstance(normalType, tuple) else normalType.__class__):
        raise TypeError(f"应为类'{normalType}'但接收到'{inType.__class__.__name__}'")


class base(ABC):
    @abstractmethod
    def __init__(self, name: str):
        self._name = name

    @property
    @abstractmethod
    def name(self):
        return self._name


class aspect(base):
    """方位类"""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self): return self._name


North = aspect("北")
East = aspect("东")
West = aspect("西")
South = aspect("南")
Southwest = aspect("西南")


class attribute(base):
    def __init__(self, name: str, Bool: bool):
        self._name = name
        self._bool = Bool

    def __repr__(self): return f"<属性: {self._name}>"

    def __bool__(self): return self._bool

    @property
    def name(self): return self._name


Yin_0 = attribute("阴", False)
Yang_1 = attribute("阳", True)


class heavenlyStem(base):
    """天干"""
    def __init__(self, name: str, order: int):
        self._name = name
        self._order = order
        self._element = None

    def __repr__(self): return f"<天干: {self.name}>"

    @property
    def name(self): return self._name

    @property
    def order(self): return self._order

    @property
    def attribute(self):
        """阴阳属性"""
        return [Yin_0, Yang_1][self.order % 2]

    @property
    def element(self):
        """五行所属"""
        return self._element

    @element.setter
    def element(self, value: ...):
        self._element = value


Jia = heavenlyStem("甲", 1)
Yi = heavenlyStem("乙", 2)
Bing = heavenlyStem("丙", 3)
Ding = heavenlyStem("丁", 4)
Wu_h = heavenlyStem("戊", 5)
Ji = heavenlyStem("己", 6)
Geng = heavenlyStem("庚", 7)
Xin = heavenlyStem("辛", 8)
Ren = heavenlyStem("壬", 9)
Gui = heavenlyStem("癸", 10)


class _limmit:
    def __init__(self, _I: dict1 | dict2, *, degree: int = 10):
        self._I = _I
        self._degree = degree

    def __getitem__(self, item: ...):
        if isinstance(item, int):
            return self._I[self.idxLimmit(item, degree=self._degree)]
        return self._I[item]

    @staticmethod
    def idxLimmit(index: int, *, degree: int = 10):
        if not (index % degree):
            return degree
        return index % degree


class hsLead:
    hsList = list("甲乙丙丁戊己庚辛壬癸")
    hsDict = _limmit(dict1(list(range(1, len(hsList) + 1)), hsList))
    hsClassDict = {k: v for k, v in zip(hsList, [Jia, Yi, Bing, Ding, Wu_h, Ji, Geng, Xin, Ren, Gui])}

    def __new__(cls, name: Literal["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"] | str):
        return cls.hsClassDict[name]


class earthlyBranche(base):
    """地支"""
    def __init__(self, name: str, order: int, *, hide: list[tuple[heavenlyStem, ...]] = None):
        self._name = name
        self._order = order
        self._hide = hide

    def __repr__(self): return f"<地支: {self.name}>"

    @property
    def name(self): return self._name

    @property
    def order(self): return self._order

    @property
    def conceal(self):
        """支中所藏"""
        return self._hide

    @conceal.setter
    def conceal(self, value):
        if isinstance(value, list) and all(map(lambda x: isinstance(x, tuple), value)):
            self._hide = value
        else:
            raise ValueError(
                f"类型错误,属性`conceal`应为列表(list),且内容为元组(tuple)"
            )


Zi = earthlyBranche("子", 1)
Chou = earthlyBranche("丑", 2)
Yin = earthlyBranche("寅", 3)
Mao = earthlyBranche("卯", 4)
Chen = earthlyBranche("辰", 5)
Si = earthlyBranche("巳", 6)
Wu_e = earthlyBranche("午", 7)
Wei = earthlyBranche("未", 8)
Shen = earthlyBranche("申", 9)
You = earthlyBranche("酉", 10)
Xu = earthlyBranche("戌", 11)
Hai = earthlyBranche("亥", 12)


class ebLead:
    ebList = list("子丑寅卯辰巳午未申酉戌亥")
    ebDict = _limmit(dict1(list(range(1, len(ebList) + 1)), ebList), degree=12)
    ebClassDict = {k: v for k, v in zip(ebList, [Zi, Chou, Yin, Mao, Chen, Si, Wu_e, Wei, Shen, You, Xu, Hai])}

    def __new__(cls, name: Literal["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"] | str):
        return cls.ebClassDict[name]


class season(base):
    """季节"""
    def __init__(self, name: str, *, doc: str = None):
        self._name = name
        self.doc = doc

    @property
    def name(self): return self._name


Spring = season("春", doc=springDoc)
Sunmmer = season("夏", doc=summerDoc)
LongSummer = season("长夏", doc=longsummerDoc)
Autumn = season("秋", doc=autumnDoc)
Winter = season("冬", doc=winterDoc)


class element(base):
    """五行元素"""
    def __init__(self, name: str, order: int, Aspect: aspect, Season: season, *, branche: earthlyBranche = None):
        self._name = name
        self._order = order
        self._aspect = Aspect
        self._branche = branche
        self._generation, self._restriction = None, None

    @property
    def name(self): return self._name

    @property
    def order(self): return self._order

    @property
    def aspect(self): return self._aspect

    @property
    def branche(self): return self._branche

    @property
    def generation(self):
        """被克"""
        return self._generation

    @generation.setter
    def generation(self, value):
        checkType(value, self)
        self._generation = value

    @property
    def restriction(self):
        """生育"""
        return self._restriction

    @restriction.setter
    def restriction(self, value):
        checkType(value, self)
        self._restriction = value


Metal = element("金", 4, West, Autumn)
Wood = element("木", 3, East, Spring)
Water = element("水", 1, North, Winter, branche=Zi)
Fire = element("火", 2, South, Sunmmer, branche=Wu_e)
Earth = element("土", 5, Southwest, LongSummer)

# 生
Metal.restriction = Water
Wood.restriction = Fire
Water.restriction = Wood
Fire.restriction = Earth
Earth.restriction = Metal

# 克
Metal.generation = Wood
Wood.generation = Earth
Water.generation = Fire
Fire.generation = Metal
Earth.generation = Water

# 支中所藏
Zi.conceal = [(Gui, Water)]
Chou.conceal = [(Ji, Earth), (Xin, Metal), (Gui, Water)]
Yin.conceal = [(Jia, Wood), (Bing, Fire), (Wu_h, Earth)]
Mao.conceal = [(Yi, Wood)]
Chen.conceal = [(Yi, Wood), (Gui, Water), (Wu_h, Earth)]
Si.conceal = [(Bing, Fire), (Wu_h, Earth), (Geng, Metal)]
Wu_e.conceal = [(Ding, Fire), (Ji, Earth)]
Wei.conceal = [(Yi, Wood), (Ji, Earth), (Ding, Fire)]
Shen.conceal = [(Geng, Metal), (Ren, Water), (Wu_h, Earth)]
You.conceal = [(Xin, Metal)]
Xu.conceal = [(Xin, Metal), (Ding, Fire), (Wu_h, Earth)]
Hai.conceal = [(Ren, Water), (Jia, Wood)]

# 五行
Jia.element = Wood


class usefulMeathod:
    """常用方法"""
    @classmethod
    def calendarConversion(cls, year: int) -> tuple[str, str]:
        """计算阴历年份对应阳历干支"""
        hs = (year1 := year - 3) % 10
        eb = year1 % 12
        return hsLead.hsList[hs], ebLead.ebList[eb]

    @classmethod
    def solarCalendar(cls, year: int) -> None:
        """打印阴历年份对应阳历干支信息"""
        h, b = cls.calendarConversion(year)
        print(f"{year}年为{h}{b}年")


class _pillar:
    def __init__(self, text: str):
        self._text = list(text)

    @property
    def hs(self): return hsLead(self._text[0])

    @property
    def eb(self): return ebLead(self._text[1])

    def __repr__(self): return f"<天干: {self.hs.name}, 地支: {self.eb.name}>"


class _lunarDate:
    def __init__(self, text: str, time: int = None):
        self._text = text

        self._year, self._month, self._day = self._format()
        self._time = time

    def _format(self):
        text = self._text.replace(" ", "").replace("年", "|").replace("月", "|").replace("日", "|")

        return [i for i in text.split("|") if i]

    def __repr__(self): return f"<四柱 | 年柱: {self._year}, 月柱: {self._month}, 日柱: {self._day}, 时柱: {self._Time}>"

    @property
    def year(self): return _pillar(self._year)

    @property
    def month(self): return _pillar(self._month)

    @property
    def day(self): return _pillar(self._day)

    @property
    def _Time(self):
        if self._time:
            timeDict = {(i, i + 2): h for i, h in zip(range(1, 23, 2), list("丑寅卯辰巳午未申酉戌亥"))}

            eb = timeDict[keyList[0]] if (keyList := [k for k in timeDict if (k[0] <= self._time < k[1])]) else "子"

            baseNum = hsLead.hsDict[self.day.hs.name]

            timeHS = (baseNum % 5 - 1) * 2 + 1

            ebGap = ebLead.ebDict[eb] - 1

            return f"{hsLead.hsDict[timeHS + ebGap]}{eb}"

        else:
            return "无"

    @property
    def time(self): return _pillar(self._Time)


class lunarCalendar:
    """万年历查询器"""
    def __init__(self, year: int, month: int, day: int, time: int = None, *, debug: bool = False):
        self._year = year
        self._month = month
        self._day = day
        self._time = time

        self._date = {
            "y": self.year,
            "m": self.month,
            "d": self.day,
            "action": "ganzhi",
            "huangli": "天干地支查询"
        }
        self._debug = debug

        self._url = "https://www.yinliyangli.com/tiangandizhi.2.php"

        self._dayHS = None
        self._lunarDate = None

    def __repr__(self):
        self._fetch()
        return (f"<阴历: {self.year}年{self.month}月{self.day}日{'' if self._time is None else f'{self.time}时'}"
                f", 阳历: {self._dayHS.replace(' ', '')}>")

    @property
    def year(self):
        if self._year < 3 or self._year >= 10000:
            raise ValueError(f"输入的年份'{self._year}'不符合规范")

        return self._year

    @property
    def month(self):
        if self._month < 1 or self._month > 12:
            raise ValueError(f"输入的月份'{self._month}'不符合规范")

        return self._month

    @property
    def day(self):
        if self._day < 1 or self._day > 31:
            raise ValueError(f"输入的日期'{self._day}'不符号规范")

        return self._day

    @property
    def time(self):
        if self._time and not (0 < int(self._time) <= 24):
            raise ValueError(
                f"时间'{self._time}'不符合规范,请按照24小时制."
            )

        return self._time

    def _fetch(self):
        soup: BeautifulSoup = request(self._url, self._date).getPostinfo().soup

        for elem in soup.find_all("p"):
            if self._debug:
                print(elem)
            text = elem.text
            if "今日干支：" in text or "当日干支：" in text:
                self._dayHS = text.replace("今日干支：", "").replace("当日干支：", "")
            if any([(t in text) for t in ["今日农历：", "当日农历：", "当天农历："]]):
                self._lunarDate = text.replace("今日农历：", "").replace("当日农历：", "").replace("当天农历：", "")

    @property
    def date(self):
        if self._dayHS is None:
            self._fetch()
        return _lunarDate(self._dayHS, self.time)

    @property
    def lunarDate(self):
        self._fetch()
        return self._lunarDate


if __name__ == '__main__':
    ins = lunarCalendar(2004, 2, 16, 2)
    print(ins.lunarDate)
