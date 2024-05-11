#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/22 上午8:39
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from os import environ
from builtins import breakpoint
# from sys import displayhook, stdout
import sys

# breakpoint()
def custom_displayhook(value):
    if value is not None:
        print('Custom display:', value)
    else:
        print('No result to display')
sys.displayhook = custom_displayhook
environ.setdefault("PYTHONDEVMODE", "1")

