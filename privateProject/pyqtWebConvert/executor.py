#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/25 上午10:11
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from functools import cached_property
from typing import Callable


class funcSet:
    refs = {
        'class': []
    }

    def assign(self, var: str, value: str):
        pass

    def callFunc(self, funcName: str, *args: str, **kwargs: str):
        pass


class warpFunc:
    def __init__(self, func: Callable, *args: str, **kwargs: str):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    @property
    def func(self):
        return self._func

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    def __repr__(self):
        return f'{self.func.__name__}({", ".join(self.args)}, {", ".join(f"{k}={v}" for k, v in self.kwargs.items())})'

    def __call__(self): return lambda: self.func(*self.args, **self.kwargs)
