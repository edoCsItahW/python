#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/3 23:14
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from IPython.display import display, Math
from functools import cached_property, singledispatchmethod
from fractions import Fraction
from warnings import warn
from typing import overload
from cmath import pi, log, cos, acos, sqrt


class autoNumber:
    @overload
    def __init__(self, divisorOrFraction: int, dividend: int = None, *, latex: bool = False):
        ...

    @overload
    def __init__(self, divisorOrFraction: str, dividend: int = None, *, latex: bool = False):
        ...

    def __init__(self, divisorOrFraction: int | str, dividend: int = None, *, latex: bool = False):
        self._divisor, self._dividend = divisorOrFraction.split("/") if '/' in divisorOrFraction else (
            divisorOrFraction, 1) if dividend is None else (divisorOrFraction, dividend)
        self._flagLatex = latex

    @property
    def divisor(self): return Fraction(self._divisor if isinstance(self._divisor, int) else eval(self._divisor))

    @property
    def dividend(self):
        if self._dividend == 0: raise ZeroDivisionError("除数不能为0")

        return Fraction(self._dividend if isinstance(self._dividend, int) else eval(self._dividend))

    @property
    def value(self): return self.divisor / self._dividend

    @property
    def fraction(self): return Fraction(self.divisor, self.dividend)

    def __repr__(self): return fr"\frac{{{self.divisor}}}{{{self.dividend}}}" if self._flagLatex else str(self.fraction)

    def __str__(self): return self.__repr__()

    def __sub__(self, other): return self.fraction - (Fraction(other) if not isinstance(other, Fraction) else other)

    def __add__(self, other): return self.fraction + (Fraction(other) if not isinstance(other, Fraction) else other)

    def __mul__(self, other): return self.fraction * (Fraction(other) if not isinstance(other, Fraction) else other)

    def __truediv__(self, other): return self.fraction / (Fraction(other) if not isinstance(other, Fraction) else other)

    def __abs__(self): return abs(self.fraction)

    def __int__(self): return int(self.value)

    def __len__(self): return len(str(self.value))

    def __neg__(self): return - self.fraction

    def __pos__(self): return self.fraction

    def __float__(self): return self.value

    def __complex__(self): return complex(self.fraction)

    def __eq__(self, other): return self.fraction == Fraction(other)

    def __ne__(self, other): return self.fraction != Fraction(other)

    def __gt__(self, other): return self.fraction > Fraction(other)

    def __ge__(self, other): return self.fraction >= Fraction(other)

    def __lt__(self, other): return self.fraction < Fraction(other)

    def __le__(self, other): return self.fraction <= Fraction(other)


class CEoperator:
    def __init__(self, a: int | float | str | Fraction = None, b: int | float | str | Fraction = None,
                 c: int | float | str | Fraction = None, d: int | float | str | Fraction = None, *,
                 latex: bool = False):
        self._flagLatex = latex
        self._constantSym = ["a", "b", "c", "d"]

        self.sp = "\\"

        self._args = []

    def __repr__(self): return f"等式: <{''.join(self._constantFormat)}=0>"

    @property
    def textDict(self) -> dict:
        _ = {
            0: r"由韦达定理:\\\begin{cases} "
               fr"x_1+x_2+x_3=-\frac{{b}}{{a}}=\sigma_1={self.sigma1} \\"
               fr"x_1x_2+x_1x_3+x_2x_3=\frac{{c}}{{a}}=\sigma_2={self.sigma2} \\"
               fr"x_1x_2x_3=-\frac{{d}}{{a}}=\sigma_3={self.sigma3}"
               r"\end{cases} \\"
               r"(这是由于(\mathbf{x}-x_1)(\mathbf{x}-x_2)(\mathbf{x}-x_3)="
               r"x^3 -(x_1 +x_2 +x_3 )x^2 +(x_1 x_2 +x_1 x_2 +x_2 x_3 )x-x_1 x_2 x_3)",
            1: r"\begin{aligned}令: x_1+\omega x_2+\omega^2 x_3 &=X \\"
               r"x_1+\omega^2 x_2+\omega x_3 &=Y \\"
               r"(其中\omega^3 &=1)) \end{aligned}\\"
               r"为求解\omega我们将1变换为e^{2\pi i}(因为由欧拉公式e^{2\pi i}=cos(2\pi) +sin(2\pi)i =1),"
               r"则\omega =e^{\frac{1}{3} 2\pi \mathbf{k}}(k为常数) \\"
               r"\begin{aligned} \begin{cases}"
               r"当\mathbf{k} &=0时 \quad \omega =1 \\"
               r"当\mathbf{k} &=1时 \quad \omega ="
               r"e^{\frac{2\pi}{3}}="
               r"cos(\frac{2\pi}{3}) +sin(\frac{2\pi}{3})i ="
               r"-\frac{1}{2}+\frac{\sqrt{3}}{2}i \\"
               r"当\mathbf{k} &=2时 \quad \omega ="
               r"e^{\frac{4\pi}{3}}="
               r"cos(\frac{4\pi}{3}) +sin(\frac{4\pi}{3})i ="
               r"-\frac{1}{2}-\frac{\sqrt{3}}{2}i \\ "
               r"(注:\omega的三个解组成了一个循环集合,当k取大于等于3的整数时,解将重复, \\ "
               r"因此只考虑k = 0、1和2的情况就可以覆盖所有可能的解)\end{cases} \end{aligned}",
            2: r"\begin{aligned}则&(x_1+\omega x_2+\omega^2 x_3)^3 +(x_1+\omega^2 x_2+\omega x_3)^3 "
               fr"=X^3 +Y^3 =2{{\sigma_1}}^3 -9\sigma_1 \sigma_2 +27\sigma_3 = {self.A}\\"
               r"&(x_1+\omega x_2+\omega^2 x_3)^3 (x_1+\omega^2 x_2+\omega x_3)^3 "
               fr"=X^3 Y^3 =({{\sigma_1}}^2 -3\sigma_2)^3 = {self.B}\end{{aligned}}",
            3: r"联立\left\{\begin{aligned} "
               r"&X^3 +Y^3 \\"
               r"&X^3 Y^3 "
               r" \end{aligned}\right."
               r"\quad解得\left\{\begin{aligned}"
               fr"&Y=\sqrt[3]{{\frac{f'{self.A}-{self.sp}sqrt{self.A ** 2 - 4 * self.B}'}{{2}}}}"
               fr"&X=\sqrt[3]{{\frac{f'{self.A}+{self.sp}sqrt{self.A ** 2 - 4 * self.B}'}{{2}}}} \\"
               r"\end{aligned}\right.",
            4: r"为演示这里将$$A=X^3 +Y^3,B=X^3 Y^3$$(为下式计算,这里将\sqrt{-1}代为虚数i) \\"
               r"则\left\{\begin{aligned}"
               fr"&X=\sqrt[3]{{\frac{f'{{A+{self.sp}sqrt{{4B-A ^ 2}}i}}'}{{2}}}} \\"
               fr"&Y=\sqrt[3]{{\frac{f'{{A-{self.sp}sqrt{{4B-A ^ 2}}i}}'}{{2}}}}"
               r"\end{aligned}\right.",
            5: r"为将$$X,Y$$转化为三角函数，且符合三角恒等式sin^2 +cos^2 =1,我们将$$X$$转换为如下形式:\\"
               r"以X为例:X="
               r"\sqrt[6]{B} \sqrt[3]{\frac{A}{2\sqrt{B}} +\frac{\sqrt{4B-A^2}i}{2\sqrt{B}}} \\"
               r"(使用待定系数,即(\frac{A}{2C})^2 +(\frac{\sqrt{4B-A^2}}{2C})^2 =1,则C=\sqrt{B})",
            6: r"如此我们令\left\{\begin{aligned}"
               r"&cos\alpha =\frac{A}{2\sqrt{B}} \\"
               r"&sin\alpha =\frac{\sqrt{4B-A^2}}{2\sqrt{B}}i "
               r"\end{aligned}\right.",
            7: r"即相当于:X=\sqrt[6]{B} \sqrt[3]{cos\alpha +sin\alpha i}"
               r"(其中:\alpha =arccos(\frac{A}{2\sqrt{B}}))\\"
               r"\\ 由欧拉公式:e^{ix} =cosx+isinx \\"
               r"则\begin{aligned} "
               r"&X=\sqrt[6]{B} e^{\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i}\\"
               r"&Y=\sqrt[6]{B} e^{-\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i} \end{aligned} \\"
               r"接下来使用线性代数求解根的方程组 \\"
               r"\begin{cases}"
               r"x_1+\omega x_2+\omega^2 x_3 &=X \\"
               r"x_1+\omega^2 x_2+\omega x_3 &=Y \\"
               r"x_1 +x_2 +x_3 &=\sigma_1 \end{cases} \\"
               r"设系数矩阵A =\begin{pmatrix}"
               r"1 & \omega & \omega^2 \\"
               r"1 & \omega^2 & \omega \\"
               r"1 & 1 & 1 \end{pmatrix} \quad "
               r"X=\begin{pmatrix}"
               r"x_1 \\"
               r"x_2 \\"
               r"x_3 \end{pmatrix} \quad"
               r" B =\begin{pmatrix}"
               r"X \\"
               r"Y \\"
               r"\sigma_1 \end{pmatrix} \\"
               r"由AX=B,求解X=A^{-1}B \\"
               r"先求其A的逆矩阵A^{-1} \\"
               r"矩阵求逆我们先求A中所有元素a_{ij}的余子式M_{ij} \\"
               r"例如M_{11}=\begin{pmatrix}"
               r"\require{cancel} \cancel{1} & \cancel{\omega} & \cancel{\omega^2} \\"
               r"\cancel{1} & \omega^2 & \omega \\"
               r"\cancel{1} & 1 & 1 \end{pmatrix}"
               r"=\omega(\omega -1) \\"
               r"则M_{12} =1-\omega,M_{13} =1-\omega^2,M_{21} =... \\"
               r"接着求每个M_{ij}对应的代数余子式\tilde{A}_{ij},"
               r"且\tilde{A}_{ij} =(-1)^{i+j}M_{ij} \\"
               r"那么\tilde{A}_{11} =M_{ij},\tilde{A}_{12} =-M_{12},\tilde{A}_{13} =... \\"
               r"现将每个\tilde{A}_{ij}放到对应的行列上构成A的伴随矩阵A^* \\"
               r"即A^* =\begin{pmatrix}"
               r"\omega(\omega -1) & \omega -1 & -(\omega +1)(\omega -1) \\"
               r"\omega(\omega -1) & -(\omega +1)(\omega -1) & \omega -1 \\"
               r"\omega(\omega -1) & \omega(\omega -1) & \omega(\omega -1) \end{pmatrix} \\"
               r"则由A^{-1} =\frac{1}{det(A)}(A^*)^\top,"
               r"其中A的行列式det(A)=3\omega^2-\omega^4-2\omega=3\omega(\omega -1) \\"
               r"即A^{-1} =\frac{1}{3\omega(\omega -1)}\begin{pmatrix}"
               r"\omega(\omega -1) & \omega(\omega -1) & \omega(\omega -1) \\"
               r"\omega -1 & -(\omega +1)(\omega -1) & \omega(\omega -1) \\"
               r"-(\omega +1)(\omega -1) & \omega -1 & \omega(\omega -1) \end{pmatrix} ="
               r"\begin{bmatrix} "
               r"\frac{1}{3} & \frac{1}{3} & \frac{1}{3} \\"
               r"\frac{1}{3\omega} & -\frac{\omega +1}{3\omega} & \frac{1}{3} \\"
               r"-\frac{\omega +1}{3\omega} & \frac{1}{3\omega} & \frac{1}{3} \end{bmatrix} \\"
               r"那么X=A^{-1}B=\begin{bmatrix} "
               r"\frac{1}{3} & \frac{1}{3} & \frac{1}{3} \\"
               r"\frac{1}{3\omega} & -\frac{\omega +1}{3\omega} & \frac{1}{3} \\"
               r"-\frac{\omega +1}{3\omega} & \frac{1}{3\omega} & \frac{1}{3} \end{bmatrix}"
               r"\begin{pmatrix}"
               r"X \\"
               r"Y \\"
               r"\sigma_1 \end{pmatrix} \\"
               r"即\begin{pmatrix}"
               r"x_1 \\"
               r"x_2 \\"
               r"x_3 \end{pmatrix} =\begin{pmatrix}"
               r"\frac{1}{3}(\sigma_1 +X+Y) \\"
               r"\frac{1}{3} \left\{ \sigma_1 +\frac{1}{\omega} [X-(\omega +1)Y] \right\} \\"
               r"\frac{1}{3} \left\{ \sigma_1 +\frac{1}{\omega} [Y-(\omega +1)X] \right\} \end{pmatrix}",
            8: r"则原方程解x_1 =\frac{1}{3} (\sigma_1 +X+Y)="
               r"\frac{1}{3} \sigma_1 +\frac{1}{3} \sqrt[6]{B}"
               r"(e^{\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i} +e^{-\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i}) \\"
               r"与x_1不同的是我们将\omega =-\frac{1}{2}+\frac{\sqrt{3}}{2}i代入\frac{1}{\omega} [X-(\omega +1)Y]后"
               r"为 \\-[(\frac{1}{2}+\frac{\sqrt{3}}{2}i)X+(\frac{1}{2}-\frac{\sqrt{3}}{2}i)Y],"
               r"即-[e^{\frac{\pi}{3}i}X+e^{-\frac{\pi}{3}i}Y]\\"
               r"x_2 =\frac{1}{3} \left\{ \sigma_1 +\frac{1}{\omega} [X-(\omega +1)Y] \right\} "
               r"=\frac{1}{3} \sigma_1 -\frac{1}{3} \sqrt[6]{B}"
               r"(e^{\frac{\pi}{3} +\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i} +"
               r"e^{-[\frac{\pi}{3} +\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})]i}) \\"
               r"X_3同理",
            9: r"为凑成欧拉公式的余弦\frac{e^{ix} +e^{-ix}}{2} =cos(x)的形式，将x_1中提出2 \\"
               r"即\begin{aligned} x_1 &=\frac{1}{3} \sigma_1 +\frac{2}{3} \sqrt[6]{B}"
               r"(\frac{e^{\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i} "
               r"\quad +e^{-\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i}}{2}) \\"
               r"&=\frac{1}{3} \sigma_1 +\frac{2}{3} \sqrt[6]{B} cos(\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})) \\"
               r"x_2 &=\frac{1}{3} \sigma_1 -\frac{2}{3} \sqrt[6]{B} "
               r"cos(\frac{\pi}{3} +\frac{1}{3} arccos(\frac{A}{2\sqrt{B}}) \\"
               r"x_3 &=\frac{1}{3} \sigma_1 -\frac{2}{3} \sqrt[6]{B} "
               r"cos(-\frac{\pi}{3} +\frac{1}{3} arccos(\frac{A}{2\sqrt{B}}) \end{aligned}"
        }
        return _

    @cached_property  # autoNumber()
    def constantDict(self): return {i: Fraction(self._input(i)) for i in ['a', 'b', 'c', 'd']}

    @cached_property
    def _constantFormat(self): return [
        f"{'+' if v > 0 and v != 1 else ''}{v if v not in [-1, 0, 1] or (i == 3 and v != 0) else '{}'.format('-' if v == -1 else '')}{'x{}'.format('^{}'.format(3 - i) if i <= 1 else '') if v != 0 and i != 3 else ''}"
        for i, v in enumerate(self.constantDict.values())]

    @property
    def a(self): return self.constantDict['a']

    @property
    def b(self): return self.constantDict['b']

    @property
    def c(self): return self.constantDict['c']

    @property
    def d(self): return self.constantDict['d']

    @cached_property
    def sigma1(self): return - self.b / self.a

    @cached_property
    def sigma2(self): return self.c / self.a

    @cached_property
    def sigma3(self): return - self.d / self.a

    @cached_property
    def A(self): return 2 * self.sigma1 ** 3 - 9 * self.sigma1 * self.sigma2 + 27 * self.sigma3

    @cached_property
    def B(self): return (self.sigma1 ** 2 - 3 * self.sigma2) ** 3

    @staticmethod
    def _qualified(value: str | int | float, *, otherCondition: bool = True):
        return value in [*map(str, range(10)), "/", "-", "."] and otherCondition

    @singledispatchmethod
    def decimalsToFractions(self, num: float | int | complex):
        return num

    @decimalsToFractions.register(int)
    def _(self, num: int | float): return Fraction(num).limit_denominator()

    @decimalsToFractions.register(float)
    def _(self, num: int | float): return Fraction(num).limit_denominator()

    @decimalsToFractions.register(complex)
    def _(self, num: complex): return Fraction(num.real).limit_denominator() + num.imag * 1j

    def show(self, order):
        display(Math(self.textDict[order]))

    def _input(self, latter: str):
        while ((inp := input(f"请输入常数'{latter}'的值:")) == '0' and latter == 'a') or not all(
                [self._qualified(i) for i in inp]):
            warn(  # 入参错误
                f"常数'a'不能为0!" if latter == 'a' and inp == '0' else f"一个无法被解析的非数字输入'{inp}'",
                SyntaxWarning)

        return inp

    def calculate(self, num: int | float | Fraction):
        fracSq = lambda A, B: self.decimalsToFractions(A / sqrt(2 * abs(B)))

        startEq = self.decimalsToFractions(1 / 3) * self.sigma1

        return startEq + self.decimalsToFractions(-2/3)*(self.B**(1/6))*cos(num+self.decimalsToFractions(1/3)*acos(fracSq(self.A, self.B))) \
            if num != 0 else startEq + self.decimalsToFractions(2/3)*(self.B**(1/6))*cos(num+self.decimalsToFractions(1/3)*((pi/2)-1j*log(fracSq(self.A, self.B)+sqrt(fracSq(self.A, self.B)**2-1)))) \
            if self.B <= 0 else startEq + self.decimalsToFractions(2/3)*(self.B**(1/6))*cos(num+self.decimalsToFractions(1/3)*acos(fracSq(self.A, self.B)))

    def execute(self):
        for i in self.textDict:
            self.show(i)
        
        res1, res2, res3 = [self.decimalsToFractions(i) for i in (self.calculate(0), self.calculate(pi / 3), self.calculate(-pi / 3))]
        
        try:
            print(''.join([f"\nx_{i}={r}" for i, r in enumerate([res1, res2, res3], start=1)]))

        except Exception as err:
            raise err


if __name__ == '__main__':
    opt = CEoperator()
    opt.execute()
