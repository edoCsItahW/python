#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
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
from typing import overload, Callable, Self, Any, Literal, TypeVar, final, Protocol, Annotated
from abc import ABC, abstractmethod
from ctypes import windll, create_string_buffer


class Fraction: ...
class Exponential: ...


Number = int | float | complex | Fraction | Exponential


class Evaluable(Protocol):
    @property
    def value(self) -> int | float: ...


class Operator(ABC):
    @final
    @property
    def left(self):
        return self._left

    @final
    @property
    def right(self):
        return self._right

    @property
    @abstractmethod
    def value(self): ...

    def __init__(self, left: Evaluable | int | float, right: Evaluable | int | float):
        self._left = left
        self._right = right

    @staticmethod
    def _calc(num: Evaluable | int | float) -> int | float:
        return num.value if hasattr(num, 'value') else num

    @abstractmethod
    def __str__(self) -> str: ...


class Add(Operator):
    @property
    def value(self) -> Number:
        return self._calc(self._left) + self._calc(self._right)

    def __str__(self) -> str:
        return f"{self._left} + {self._right}"


class Sub(Operator):
    @property
    def value(self) -> Number:
        return self._calc(self._left) - self._calc(self._right)

    def __str__(self) -> str:
        return f"{self._left} - {self._right}"


class Mul(Operator):
    @property
    def value(self) -> Number:
        return self._calc(self._left) * self._calc(self._right)

    def __str__(self) -> str:
        return f"{self._left} * {self._right}"


class Div(Operator):
    @property
    def value(self) -> Number:
        return self._calc(self._left) / self._calc(self._right)

    def __str__(self) -> str:
        return f"{self._left} / {self._right}"


LATEX_OUTPUT = False


def gcd(a: int, b: int) -> int:
    return gcd(b, a % b) if b else a


def floatToFrac(decimal: float) -> tuple[int, int]:
    den = 1
    while decimal != int(decimal):
        decimal *= 10
        den *= 10
    return int((i := int(decimal)) / (div := gcd(i, den))), int(den / div)


def binPow(_base: Number, _exp: int) -> Number:
    if isinstance(_base, float):
        _base = Fraction(_base)
    if _exp == 0: return 1
    res = binPow(_base, _exp // 2)
    if _exp % 2 == 0: return res * res
    return res * res * _base


def scanf(_fmt: bytes, _len: int) -> tuple[str]:
    windll.msvcrt.scanf(_fmt, *(args := [create_string_buffer(100) for _ in range(_len)]))
    return tuple(arg.value.decode() for arg in args)


def numExec(_expr: str):
    if _expr.isdigit():
        return int(_expr)
    elif '.' in _expr:
        return Fraction(eval(_expr))
    elif '/' in _expr:
        num, den = _expr.split('/')
        return Fraction(int(num), int(den))
    elif '^' in _expr:
        num, den = _expr.split('^')
        return Exponential(num, int(den))
    else:
        raise ValueError(f"无法解析表达式 {_expr}")


class Fraction:
    @property
    def numerator(self) -> Number:
        if not self.SIMPLEST:
            self._reduce()
        return self._numerator

    @property
    def denominator(self) -> Number:
        if not self.SIMPLEST:
            self._reduce()
        return self._denominator

    @property
    def value(self) -> Number:
        return self._numerator / self._denominator

    def __new__(cls, *args: Number | Operator, **kwargs) -> Number:
        match len(args):
            case 1:
                if isinstance(args[0], float) or isinstance(args[0], Operator):
                    return super().__new__(cls)
                return args[0]
            case 2:
                if args[1] == 0: raise ZeroDivisionError(
                    "分母不能为0")
                if args[0] == 0: return 0  # 0/d = 0
                return super().__new__(cls)
            case _:
                raise TypeError(f"Fraction() takes 1 or 2 positional arguments but {len(args)} were given")

    @overload
    def __init__(self, _number: Number): ...

    @overload
    def __init__(self, _numerator: Number, _denominator: Number): ...

    def __init__(self, *args: Number | Operator, **kwargs: Number) -> None:
        """
        :param _numerator: 分子
        :param _denominator: 分母
        """
        if hasattr(self, 'AREADY_INITED'): return  # 避免重复初始化
        self.AREADY_INITED = True
        self.SIMPLEST = False

        match len(args):
            case 1:
                if isinstance(args[0], float):
                    args = floatToFrac(args[0])
        self._numerator, self._denominator = args

    def __str__(self) -> str:
        return fr"\frac{{{self._numerator}}}{{{self._denominator}}}" if LATEX_OUTPUT else f"{self._numerator}/{self._denominator}"

    def __add__(self, other: Number) -> Fraction | Exponential:
        self.SIMPLEST = False
        if isinstance(other, int):
            return Fraction(self._numerator + other * self._denominator, self._denominator)
        elif isinstance(other, float):
            return self + Fraction(other)
        elif isinstance(other, Fraction):
            return Fraction(self._numerator * other.denominator + other.numerator * self._denominator, self._denominator * other.denominator)
        elif isinstance(other, Exponential):  # n/d + c * b^e = (n + d * c * b^e) / d
            return Fraction(Add(self._numerator, Exponential(other.base, other.exponent, coefficent=other.coefficent * self._denominator)), self._denominator)
        raise TypeError(f"unsupported operand type(s) for +: 'Fraction' and '{type(other).__name__}'")

    def __radd__(self, other: Number) -> Fraction | Exponential:
        self.SIMPLEST = False
        if isinstance(other, Exponential):
            return NotImplemented  # 交给Exponential的__add__处理
        return self.__add__(other)

    def __sub__(self, other: Number) -> Fraction | Exponential:
        self.SIMPLEST = False
        if isinstance(other, int):
            return Fraction(self._numerator - other * self._denominator, self._denominator)
        elif isinstance(other, float):
            return self - Fraction(other)
        elif isinstance(other, Fraction):
            return Fraction(self._numerator * other.denominator - other.numerator * self._denominator, self._denominator * other.denominator)
        elif isinstance(other, Exponential):  # n/d - c * b^e = (n - d * c * b^e) / d
            return Fraction(Sub(self._numerator, Exponential(other.base, other.exponent, coefficent=other.coefficent * self._denominator)), self._denominator)
        raise TypeError(f"unsupported operand type(s) for -: 'Fraction' and '{type(other).__name__}'")

    def __rsub__(self, other: Number) -> Fraction | Exponential:
        self.SIMPLEST = False
        if isinstance(other, Exponential):
            return NotImplemented  # 交给Exponential的__sub__处理
        return self.__sub__(other)

    def __mul__(self, other: Number) -> Fraction | Exponential:
        self.SIMPLEST = False
        if isinstance(other, int):
            return Fraction(self._numerator * other, self._denominator)
        elif isinstance(other, float):
            return self * Fraction(other)
        elif isinstance(other, Fraction):
            return Fraction(self._numerator * other.numerator, self._denominator * other.denominator)
        elif isinstance(other, Exponential):  # n/d * c * b^e = (n * c * b^e) / d or ((n * c) / d) * b^e
            return Exponential(other.base, other.exponent, coefficent=self * other.coefficent)
        raise TypeError(f"unsupported operand type(s) for *: 'Fraction' and '{type(other).__name__}'")

    def __rmul__(self, other: Number) -> Fraction | Exponential:
        self.SIMPLEST = False
        if isinstance(other, Exponential):
            return NotImplemented  # 交给Exponential的__mul__处理
        return self.__mul__(other)

    def __truediv__(self, other: Number) -> Fraction | Exponential:
        self.SIMPLEST = False
        if isinstance(other, int):
            return Fraction(self._numerator, self._denominator * other)
        elif isinstance(other, float):
            return self / Fraction(other)
        elif isinstance(other, Fraction):
            return Fraction(self._numerator * other.denominator, self._denominator * other.numerator)
        elif isinstance(other, Exponential):  # n/d / (c * b^e) = n / (d * c * b^e) or (n / (c * d)) * b^(-e)
            return Exponential(other.base, -other.exponent, coefficent=self / other.coefficent)
        raise TypeError(f"unsupported operand type(s) for /: 'Fraction' and '{type(other).__name__}'")

    def __rtruediv__(self, other: Number) -> Fraction | Exponential:
        self.SIMPLEST = False
        if isinstance(other, Exponential):
            return NotImplemented  # 交给Exponential的__truediv__处理
        return Fraction(other) / self

    def __pow__(self, power: int, modulo=None):
        self.SIMPLEST = False
        return binPow(self, power)

    def __neg__(self) -> Fraction:
        return Fraction(-self._numerator, self._denominator)

    def _reduce(self):
        div = gcd(self._numerator, self._denominator)
        self._numerator //= div
        self._denominator //= div
        self.SIMPLEST = True


class Exponential:
    _realArgs: tuple

    @property
    def base(self) -> Number:
        return self._base

    @property
    def exponent(self) -> Number:
        return self._exponent

    @property
    def coefficent(self) -> Number:
        return self._coefficent

    @property
    def value(self) -> Number:
        return self._coefficent * self._base ** self._exponent

    def __new__(cls, *args: Number, **kwargs: Number) -> Number:
        coefficent = kwargs.get('coefficent', 1)
        match len(args):
            case 1:
                if isinstance(args[0], float):
                    return Fraction(args[0]) * coefficent
                return args[0] * coefficent
            case 2:
                _base, _exponent = args
                if _base == 0: return 0  # 0^e = 0
                if _base == 1: return 1  # 1^e = 1
                if _exponent == 0: return 1  # a^0 = 1(已排除0^0)
                if _exponent == 1: return _base  # a^1 = a
                if coefficent == 0: return 0  # 0 * a^b = 0
                return super().__new__(cls)

    @overload
    def __init__(self, _number: Number): ...

    @overload
    def __init__(self, _base: Number, _exponent: Number, *, coefficent: Number = 1): ...

    def __init__(self, *args: Number, **kwargs: Number):
        if hasattr(self, 'AREADY_INITED'): return  # 避免重复初始化
        _base, _exponent = args
        coefficent = kwargs.get('coefficent', 1)
        if isinstance(_base, Fraction) and _base.numerator == 1:  # (1/d)^e = d^-e
            _base = _base.denominator
            _exponent = -_exponent

        elif isinstance(_base, Exponential):  # c_2 * (c_1 * b^e_1)^e_2 = c_2 * c_1^e_2 * b^(e_1 * e_2)
            coefficent = Exponential(_base.base, _exponent * _base.exponent, coefficent=coefficent * Exponential(_base.coefficent, _exponent, coefficent=coefficent))

        self.AREADY_INITED = True
        self.SIMPLEST = False
        self._base = _base
        self._exponent = _exponent
        self._coefficent = coefficent

    def __str__(self) -> str:
        return f"{'' if self._coefficent == 1 else f'{self._coefficent} '}{self._base}^{{{self._exponent}}}" \
            if LATEX_OUTPUT else\
            f"{'' if self._coefficent == 1 else f'{self._coefficent} * '}{self._base}^{f'{self._exponent}' if isinstance(self._exponent, int) else f'({self._exponent})'}"

    def __add__(self, other: Number) -> Add | Exponential:
        self.SIMPLEST = False
        if isinstance(other, int):
            return Add(self, other)
        elif isinstance(other, float):
            return Add(self, Fraction(other))
        elif isinstance(other, Fraction):
            return Add(self, other)
        elif isinstance(other, Exponential):
            if self.base == other.base and self.exponent == other.exponent:
                return Exponential(self.base, self.exponent, coefficent=self._coefficent + other.coefficent)
            return Add(self, other)
        raise TypeError(f"unsupported operand type(s) for +: 'Exponential' and '{type(other).__name__}'")

    def __radd__(self, other: Number) -> Add | Exponential:
        self.SIMPLEST = False
        if isinstance(other, Fraction):
            return NotImplemented  # 交给Fraction的__add__处理
        return self.__add__(other)

    def __sub__(self, other: Number) -> Sub | Exponential:
        self.SIMPLEST = False
        if isinstance(other, int):
            return Sub(self, other)
        elif isinstance(other, float):
            return Sub(self, Fraction(other))
        elif isinstance(other, Fraction):
            return Sub(self, other)
        elif isinstance(other, Exponential):
            if self.base == other.base and self.exponent == other.exponent:
                return Exponential(self.base, self.exponent, coefficent=self._coefficent - other.coefficent)
            return Sub(self, other)
        raise TypeError(f"unsupported operand type(s) for -: 'Exponential' and '{type(other).__name__}'")

    def __rsub__(self, other: Number) -> Sub | Exponential:
        self.SIMPLEST = False
        if isinstance(other, Fraction):
            return NotImplemented  # 交给Fraction的__sub__处理
        return self.__sub__(other)

    def __mul__(self, other: Number) -> Mul | Exponential:
        self.SIMPLEST = False
        if isinstance(other, int):
            return Exponential(self.base, self.exponent, coefficent=self._coefficent * other)
        elif isinstance(other, float):
            return Exponential(self.base, self.exponent, coefficent=self._coefficent * Fraction(other))
        elif isinstance(other, Fraction):
            return Exponential(self.base, self.exponent, coefficent=self._coefficent * other)
        elif isinstance(other, Exponential):
            if self.base == other.base:
                return Exponential(self.base, self.exponent + other.exponent, coefficent=self._coefficent * other.coefficent)
            return Mul(self, other)
        raise TypeError(f"unsupported operand type(s) for *: 'Exponential' and '{type(other).__name__}'")

    def __rmul__(self, other: Number) -> Mul | Exponential:
        self.SIMPLEST = False
        if isinstance(other, Fraction):
            return NotImplemented  # 交给Fraction的__mul__处理
        return self.__mul__(other)

    def __truediv__(self, other: Number) -> Div | Exponential:
        self.SIMPLEST = False
        if isinstance(other, int):
            return Exponential(self.base, self.exponent, coefficent=self._coefficent / other)
        elif isinstance(other, float):
            return Exponential(self.base, self.exponent, coefficent=self._coefficent / Fraction(other))
        elif isinstance(other, Fraction):
            return Exponential(self.base, self.exponent, coefficent=self._coefficent / other)
        elif isinstance(other, Exponential):
            if self.base == other.base:
                return Exponential(self.base, self.exponent - other.exponent, coefficent=self._coefficent / other.coefficent)
            return Div(self, other)
        raise TypeError(f"unsupported operand type(s) for /: 'Exponential' and '{type(other).__name__}'")

    def __rtruediv__(self, other: Number) -> Div | Exponential:
        self.SIMPLEST = False
        if isinstance(other, Fraction):
            return NotImplemented  # 交给Fraction的__truediv__处理
        return self.__truediv__(other)

    def __pow__(self, power: int, modulo=None):
        self.SIMPLEST = False
        return binPow(self, power)

    def __neg__(self) -> Exponential:
        return Exponential(self.base, self.exponent, coefficent=-self._coefficent)


if __name__ == '__main__':
    print("请输入四个数字，以空格分隔：")
    a, b, c, d = map(numExec, scanf(b"%s %s %s %s", 4))
    p, q, r = b / a, c / a, d / a
    sigma1, sigma2, sigma3 = -p, q, -r

    A = 2 * sigma1 ** 3 - 9 * sigma1 * sigma2 ** 2 + 27 * sigma3
    B = (sigma1 ** 2 - 3 * sigma2) ** 3

    print(A, B)
