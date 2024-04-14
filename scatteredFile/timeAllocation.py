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
from matplotlib.pyplot import show, bar, subplots, savefig, gca
from matplotlib.patches import Polygon
from pypiOrigin.conFunc.confunc import sequence
from pandas import DataFrame
from numpy import array, ndarray
from sympy import symbols, cos, simplify, pi, sin, sqrt, tan, Rational
from functools import singledispatchmethod
from typing import Self


class coordinate:
    def __init__(self, x: int | float, y: int | float):
        self._x = x
        self._y = y

    @property
    def x(self): return self._x

    @x.setter
    def x(self, value: int | float): self._x = value

    @property
    def y(self): return self._y

    @y.setter
    def y(self, value: int | float): self._y = value

    @property
    def value(self): return [self.x, self.y]

    @singledispatchmethod
    def __sub__(self, other):
        raise TypeError("与坐标类相减的也必须是坐标类!")

    @__sub__.register(tuple)
    def _(self, value: Self): return coordinate(self.x + value.x, self.y + value.y)

    @singledispatchmethod
    def __add__(self, other):
        raise TypeError("与坐标类相减的也必须是坐标类!")

    @__add__.register(tuple)
    def _(self, value: Self): return coordinate(self.x - value.x, self.y - self.y)

    def __repr__(self): return f"({self.x},{self.y})"

    def __call__(self): return self.value


class visualize:
    def __init__(self, u: int = 2, w: int = 2):  # , mon: list, tue: list, wen: list, thu: list, fri: list, sat: list, sun: list):
        self._unit = u
        self._width = w
        self._var = symbols("x")

    @property
    def unit(self): return self._unit

    @property
    def width(self): return self._width

    @property
    def x(self): return self._var

    @staticmethod
    def _toDg(degree: int | float): return degree * pi / 180

    @staticmethod
    def stackedColumn(*args: list, reverse: bool = False):
        bottom = array([0] * len(args[0]))

        for i, l in enumerate(reversed(args) if reverse else args):

            bar(sequence(l, start=0), l, bottom=bottom)

            bottom += array(l)

        show()

    def point(self, x: int | float, *, degree: int = 45, unit: int | float = None):
        unit = unit if unit else self.unit

        return [
            [(-sqrt(unit) + self.x * cos(self._toDg(degree))).subs(self.x, x), (-self.x * sin(self._toDg(degree))).subs(self.x, x)],
            [(sqrt(unit) + self.x * cos(self._toDg(degree))).subs(self.x, x), (-self.x * sin(self._toDg(degree))).subs(self.x, x)],
            [(sqrt(unit) - self.x * cos(self._toDg(degree))).subs(self.x, x), (self.x * sin(self._toDg(degree))).subs(self.x, x)],
            [(-sqrt(unit) - self.x * cos(self._toDg(degree))).subs(self.x, x), (self.x * sin(self._toDg(degree))).subs(self.x, x)],
        ]

    def outside(self, x: int | float, *, degree: int = 45, unit: int | float = None):
        xValueL = self.width / tan(self._toDg(180 - degree) / 2)
        xValueR = self.width / tan(self._toDg(degree) / 2)

        return (list1 := self.point(x, degree=degree, unit=unit)), [
            [list1[0][0] - xValueL, list1[0][1] - self.width],
            [list1[1][0] + xValueR, list1[1][1] - self.width],
            [list1[2][0] + xValueL, list1[2][1] + self.width],
            [list1[3][0] - xValueR, list1[3][1] + self.width]
        ]

    def draw(self, x: int | float, degree: int = 45):
        expr = self.x / (2 * cos(self._toDg(45)))

        print(simplify(expr))

        unit = expr.subs(self.x, self.unit)

        left, right = coordinate(0, -unit), coordinate(0, unit)

        w = h = self.x * cos(self._toDg(45))

        print(left, right)

    @staticmethod
    def show4(*args: tuple):
        fig, ax = subplots()

        for arr in args:
            ax.add_patch(Polygon(array(arr[0]), edgecolor="black", facecolor="none"))
            ax.add_patch(Polygon(array(arr[1]), edgecolor="black", facecolor="none"))

        ax.set_xlim(-30, 30)
        ax.set_ylim(-28, 28)

        gca().xaxis.set_visible(False)
        gca().yaxis.set_visible(False)
        for s in gca().spines.values():
            s.set_visible(False)

        savefig(r"C:\Users\Lenovo\Desktop\x.png", dpi=300)

        show()


if __name__ == '__main__':
    # freeTimeDict = {
    #     "mon": [85, 50, 60, 60, 60],
    #     "Tue": [0, 0, 60, 60, 60],
    #     "Wen": [85, 75, 50, 60, 60],
    #     "Thu": [75, 70, 60, 60, 60],
    #     "Fri": [0, 0, 0, 0, 210],
    #     "Sat": [0, 0, 0, 0, 450],
    #     "Sun": [0, 0, 0, 0, 270]
    # }

    # totalTime = sum([array(l) @ array([1] * 5) for l in freeTimeDict.values()])

    # taskTimeDict = {
    #     "A": 0
    # }
    # print(totalTime)
    # visualize.stackedColumn(*DataFrame(freeTimeDict).values, reverse=True)
    pass