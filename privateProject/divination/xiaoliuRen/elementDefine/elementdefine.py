#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/1/13 22:29
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
def checkType(inType: type, normalType: type | tuple[type]):
    if not isinstance(inType, tuple([i.__class__ for i in normalType]) if isinstance(normalType, tuple) else normalType.__class__):
        raise TypeError(f"应为类'{normalType}'但接收到'{inType.__class__.__name__}'")


ebList = list("子丑寅卯辰巳午未申酉戌亥")
sixPalace = ["大安", "留恋", "速喜", "赤口", "小吉", "空亡"]


class aspect:
    def __init__(self, name: str):
        self._name = name

    def __repr__(self): return f"<方位: {self._name}>"

    @property
    def name(self): return self._name


class element:
    def __init__(self, name: str, *, _aspect: aspect):
        """
        五行元素

        :param name: 名称
        :type name: str
        :param _aspect: 方位
        :type _aspect: aspect
        """
        self._name = name
        self._aspect = _aspect

        self._restriction, self._generation = None, None

    def __repr__(self): return f"<五行: {self._name}>"

    @property
    def name(self): return self._name

    @property
    def aspect(self):
        """方位"""
        return self._aspect

    @property
    def restriction(self):
        """我生"""
        return self._restriction

    @restriction.setter
    def restriction(self, value: ...):
        checkType(value, self)
        self._restriction = value

    @property
    def generation(self):
        """我克"""
        return self._generation

    @generation.setter
    def generation(self, value: ...):
        checkType(value, self)
        self._generation = value


# 方位
North = aspect("北")
East = aspect("东")
West = aspect("西")
South = aspect("南")
Centre = aspect("中")

# 五行
Wood = element("木", _aspect=East)
Fire = element("火", _aspect=South)
Earth = element("土", _aspect=Centre)
Metal = element("金", _aspect=West)
Water = element("水", _aspect=North)

# 生
Wood.restriction = Fire
Fire.restriction = Earth
Earth.restriction = Metal
Metal.restriction = Water
Water.restriction = Wood

# 克
Water.generation = Fire
Fire.generation = Metal
Metal.generation = Wood
Wood.generation = Earth
Earth.generation = Water


class earthlyBranche:
    """地支"""
    def __init__(self, name: str, order: int, _element: element):
        self._name = name
        self._order = order
        self._element = _element

    def __repr__(self): return f"<地支: {self.name}>"

    @property
    def name(self): return self._name

    @property
    def order(self): return self._order

    @property
    def element(self): return self._element

    def relation(self, _object: 'earthlyBranche'):
        if self.element is _object.element:
            return "相同"
        elif self.element is _object.element.generation:
            return "克我"
        elif self.element is _object.element.restriction:
            return "生我"
        elif self.element.generation is _object.element:
            return "我克"
        elif self.element.restriction is _object.element:
            return "我生"
        else:
            raise ValueError(
                f"对比异常"
            )


Zi = earthlyBranche("子", 1, Water)
Chou = earthlyBranche("丑", 2, Earth)
Yin = earthlyBranche("寅", 3, Wood)
Mao = earthlyBranche("卯", 4, Wood)
Chen = earthlyBranche("辰", 5, Earth)
Si = earthlyBranche("巳", 6, Fire)
Wu_e = earthlyBranche("午", 7, Fire)
Wei = earthlyBranche("未", 8, Earth)
Shen = earthlyBranche("申", 9, Metal)
You = earthlyBranche("酉", 10, Metal)
Xu = earthlyBranche("戌", 11, Earth)
Hai = earthlyBranche("亥", 12, Water)


class sixGodLead:
    godList = {"寅卯": "青龙", "巳午": "朱雀", "丑辰": "勾陈", "未戌": "腾蛇", "申酉": "白虎", "亥子": "玄武"}

    def __getitem__(self, item: str):
        for k in self.godList:
            if item in k:
                return self.godList[k]


class ebLead:
    ebDict = {k: v for k, v in zip(ebList, [Zi, Chou, Yin, Mao, Chen, Si, Wu_e, Wei, Shen, You, Xu, Hai])}

    def __getitem__(self, item: str):
        return self.ebDict[item]


if __name__ == '__main__':
    print(Zi.relation(Chen))
