#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/8 15:04
# 当前项目名: python
# 编码模式: utf-8
# 注释:
# -------------------------<Lenovo>----------------------------
from matplotlib.pyplot import show, bar
from confunc import sequence
from pandas import DataFrame
from numpy import array, ndarray
from functools import cached_property
from copy import deepcopy


class visualize:
    def __init__(self, **kwargs: list):
        self._kw = kwargs

        self._keys = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]

    @cached_property
    def freeTimeDict(self): return {k: self._kw[k] if k in self._kw else [] for k in self._kw}

    @cached_property
    def fullFTDict(self):
        maxNum = max(map(len, self.freeTimeDict.values()))

        freeTimeDict = deepcopy(self.freeTimeDict)

        for k in freeTimeDict:
            if (l := len(freeTimeDict[k])) < maxNum:
                freeTimeDict[k] += (maxNum - l) * [0]

        return freeTimeDict

    @cached_property
    def totalTime(self): return sum([array(l) @ array([1] * 5) for l in self.fullFTDict.values()])

    def stackedColumn(self, *args: list, reverse: bool = False):
        if not args: args = DataFrame(self.fullFTDict).values

        bottom = array([0] * len(args[0]))

        for i, l in enumerate(reversed(args) if reverse else args):

            bar(sequence(l, start=0), l, bottom=bottom)

            bottom += array(l)

        show()


if __name__ == '__main__':
    ins = visualize(Mon=[85, 50, 60, 60, 60], Tue=[60, 60, 60], Wen=[85, 75, 50, 60, 60], Thu=[75, 70, 60, 60, 60], Fri=[210], Sat=[450], Sun=[270])
    ins.stackedColumn(reverse=True)
