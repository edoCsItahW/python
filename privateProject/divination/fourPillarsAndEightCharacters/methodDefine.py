#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/1/13 2:09
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
class dict1:
    def __init__(self, _I: list, _T: list):
        self._I, self._T = _I, _T

        self._set = set()

        self._check()

    def _check(self):
        tLen = None
        for i in (self._I, self._T):
            if not isinstance(i, list):
                raise TypeError(
                    f"参数应为列表(list)"
                )

            if tLen is None:
                tLen = len(i)
            else:
                if len(i) != tLen: raise ValueError(
                    f"参数长度异常"
                )

            for k in i:
                if k in self._set:
                    raise ValueError(
                        f"元素`{k}`重复"
                    )
                else:
                    self._set.add(k)

    def __getitem__(self, item: ...):
        if item in self._I:
            return {k: v for k, v in zip(self._I, self._T)}[item]
        elif item in self._T:
            return {k: v for k, v in zip(self._T, self._I)}[item]
        else:
            raise KeyError(
                f"键`{item}`不存在"
            )

    def __repr__(self): return f"<{''.join([f'({i}, {j}), ' for i, j in zip(self._I, self._T)])}>"


class dict2:
    def __init__(self, **kwargs: list | dict):
        self._kwargs = kwargs

        self._set = set()

        self._check()

    def __getitem__(self, index: ...):
        return self._kwargs[index]

    def _check(self):
        tLen = None
        for i in self._kwargs:
            for k in self._kwargs[i]:
                if k in self._set:
                    raise ValueError(
                        f"关键字参数`{i}`中元素`{k}`重复."
                    )
                else:
                    self._set.add(k)

        for i in self._kwargs:
            if not isinstance(content := self._kwargs[i], (list, dict)):
                raise TypeError(
                    f"关键字参数`{i}`类型异常"
                )

            if tLen:
                if len(self._kwargs[i]) != tLen:
                    raise ValueError(
                        f"关键字参数`{i}`中的元素个数异常."
                    )
            else:
                tLen = len(self._kwargs[i])


if __name__ == '__main__':
    ins = dict1([1, 2, 3, 4, 5], ["a", "b", "c", "d", "e"])
    print(ins["a"])


