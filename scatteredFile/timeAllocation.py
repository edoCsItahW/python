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
from pypiOrigin.conFunc.confunc import sequence
from pandas import DataFrame
from numpy import array


class visualize:
    def __init__(self):
        pass

    @staticmethod
    def stackedColumn(*args: list, reverse: bool = False):
        bottom = array([0] * len(args[0]))

        for i, l in enumerate(reversed(args) if reverse else args):

            bar(sequence(l, start=0), l, bottom=bottom)

            bottom += array(l)

        show()


if __name__ == '__main__':
    freeTimeDict = {
        "mon": [85, 50, 60, 60, 60],
        "Tue": [0, 0, 60, 60, 60],
        "Wen": [85, 75, 50, 60, 60],
        "Thu": [75, 70, 60, 60, 60],
        "Fri": [0, 0, 0, 0, 210],
        "Sat": [0, 0, 0, 0, 450],
        "Sun": [0, 0, 0, 0, 270]
    }
    taskTimeDict = {
        "A": 0
    }
    visualize.stackedColumn(*DataFrame(freeTimeDict).values, reverse=True)
