#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn
WARNING_LEVEL: int


class WarnLevel:
    DEBUG: int
    INFO: int
    WARNING: int
    ERROR: int
    CRITICAL: int


def warn(level: int, message: str) -> None:
    """
    一个警告函数，用于输出警告信息。

    :param level: 警告级别
    :param message: 警告信息
    :return: None
    """


def warnColor(level: int, message: str) -> None:
    """
    一个带颜色的警告函数，用于输出带颜色的警告信息。

    :param level: 警告级别
    :param message: 警告信息
    :return: None
    """


def alert(message: str) -> None:
    """
    一个弹窗函数，用于输出弹窗信息。

    :param message: 弹窗信息
    :return: None
    """
