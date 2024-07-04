#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn


def getHandleByPid(pid: int) -> int:
    """
    通过进程ID获取窗口句柄

    :param pid: 进程ID
    :return: 窗口句柄
    """


def getHwndByPid(pid: int) -> int:
    """
    通过进程ID获取窗口句柄

    :param pid: 进程ID
    :return: 窗口句柄
    """


def getPidByHandle(handle: int) -> int:
    """
    通过窗口句柄获取进程ID

    :param handle: 窗口句柄
    :return: 进程ID
    """


def getPidByHwnd(hwnd: int) -> int:
    """
    通过窗口句柄获取进程ID

    :param hwnd: 窗口句柄
    :return: 进程ID
    """


def getProcessName(pid: int) -> str:
    """
    获取进程名

    :param pid: 进程ID
    :return: 进程名
    """


def getWindowTitleByHandle(handle: int) -> str:
    """
    通过窗口句柄获取窗口标题

    :param handle: 窗口句柄
    :return: 窗口标题
    """


def getWindowTitleByHwnd(hwnd: int) -> str:
    """
    通过窗口句柄获取窗口标题

    :param hwnd: 窗口句柄
    :return: 窗口标题
    """


def getWindowTitle(pid: int) -> str:
    """
    获取窗口标题

    :param pid: 进程ID
    :return: 窗口标题
    """


class Process:
    def __init__(self, pid: int):
        self._pid = pid
        self.hwnd: int
        self.handle: int
        self.processName: str
        self.windowTitle: str

    @property
    def pid(self) -> int:
        raise self._pid


class ProcessList:
    def __init__(self):
        self._processList: list[Process]

    @property
    def processList(self) -> list[Process]:
        return self._processList


def getProcessListFromEnum() -> ProcessList:
    """
    获取进程列表

    :return: 进程列表
    """


def enumWindows() -> ProcessList:
    """
    获取窗口列表

    :return: 窗口列表
    """


def findProcessByTitle(title: str) -> Process:
    """
    通过窗口标题查找进程

    :param title: 窗口标题
    :return: 进程
    """


def getFoucsWindow() -> Process:
    """
    获取焦点窗口

    :return: 进程
    """


