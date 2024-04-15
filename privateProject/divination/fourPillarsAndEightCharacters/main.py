#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/1/12 20:24
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from baseClassDefine import lunarCalendar, hsLead, ebLead
from typing import Literal


class divination:
    def __init__(self, year: int, month: int, day: int, time: int = None):
        self._date = lunarCalendar(year, month, day, time)

    def fate(self, gender: Literal["男", "女"]) -> list[tuple[str, str]]:
        """
        排六年大运

        :param gender: 性别
        :type gender: str
        :return: 六年大运列表
        :rtype: list
        """
        fateList = []

        date = self._date.date
        yearHsAttr = bool(date.year.hs.attribute)

        if (yearHsAttr and gender == "男") or (not yearHsAttr and gender == "女"):
            for i, j in zip(range(hsNum := date.month.hs.order + 1, hsNum + 6), range(ebNum := date.month.eb.order + 1, ebNum + 6)):
                fateList.append((hsLead.hsDict[i], ebLead.ebDict[j]))
        else:
            for i, j in zip(range(hsNum := date.month.hs.order - 1, hsNum - 6, -1), range(ebNum := date.month.eb.order - 1, ebNum - 6, -1)):
                fateList.append((hsLead.hsDict[i], ebLead.ebDict[j]))

        return fateList


if __name__ == '__main__':
    ins = divination(2004, 2, 16)
    print(ins.fate("女"))
