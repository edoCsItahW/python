#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn
from typing import Callable, Any


PROCESS_QUERY_INFORMATION: int


PROCESS_VM_READ: int


MAX_PATH: int


def OpenProcess(dwDesiredAccess: int, bInheritHandle: bool, dwProcessId: int) -> int:
    """
    打开一个进程的句柄并返回句柄值

    :param dwDesiredAccess: 访问权限
    :param bInheritHandle: 是否继承句柄
    :param dwProcessId: 进程ID
    :return: 进程句柄值
    """


def CloseHandle(hObject: int) -> bool:
    """
    关闭一个进程的句柄

    :param hObject: 句柄值
    :return: 成功返回True，失败返回False
    """


def GetLastError() -> int:
    """
    获取最后一个错误代码

    :return: 错误代码
    """


def EnumWindows(lpEnumFunc: Callable, lParam: Any) -> bool:
    """
    枚举所有顶层窗口

    :param lpEnumFunc: 回调函数
    :param lParam: 回调函数参数
    :return: 成功返回True，失败返回False
    """


def GetWindowThreadProcessId(hWnd: int, lpdwProcessId: int) -> int:
    """
    获取窗口的进程ID

    :param hWnd: 窗口句柄
    :param lpdwProcessId: 进程ID指针
    :return: 线程ID
    """


def GetWindowTextLength(hWnd: int) -> int:
    """
    获取窗口标题长度

    :param hWnd: 窗口句柄
    :return: 标题长度
    """


def GetWindowText(hWnd: int, lpString: str, nMaxCount: int) -> int:
    """
    获取窗口标题

    :param hWnd: 窗口句柄
    :param lpString: 标题指针
    :param nMaxCount: 最大长度
    :return: 实际长度
    """


def GetWindowTextA(hWnd: int, lpString: str, nMaxCount: int) -> int:
    """
    获取窗口标题（ANSI版本）

    :param hWnd: 窗口句柄
    :param lpString: 标题指针
    :param nMaxCount: 最大长度
    :return: 实际长度
    """


def GetModuleBaseName(hProcess: int, hModule: int, lpBaseName: str, nSize: int) -> int:
    """
    获取模块名称

    :param hProcess: 进程句柄
    :param hModule: 模块句柄
    :param lpBaseName: 名称指针
    :param nSize: 最大长度
    :return: 实际长度
    """


def IsWindowVisible(hWnd: int) -> bool:
    """
    判断窗口是否可见

    :param hWnd: 窗口句柄
    :return: 可见返回True，不可见返回False
    """


def IsWindowEnabled(hWnd: int) -> bool:
    """
    判断窗口是否可用

    :param hWnd: 窗口句柄
    :return: 可用返回True，不可用返回False
    """


def EnumProcesses(lpidProcess: int, cb: int, lpcbNeeded: int) -> bool:
    """
    枚举所有进程

    :param lpidProcess: 进程ID指针
    :param cb: 结构体大小
    :param lpcbNeeded: 实际大小指针
    :return: 成功返回True，失败返回False
    """


def FindWindow(lpClassName: str, lpWindowName: str) -> int:
    """
    查找窗口

    :param lpClassName: 类名指针
    :param lpWindowName: 窗口名指针
    :return: 窗口句柄
    """