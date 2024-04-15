#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/12 8:40
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from win32api import ShellExecute
from win32com.client import Dispatch, CDispatch
from win32gui import FindWindow, SetForegroundWindow, GetClassName, EnumWindows, GetWindowText, GetForegroundWindow, GetWindowLong, IsWindowVisible
from win32process import GetWindowThreadProcessId
from win32con import WS_VISIBLE, GWL_EXSTYLE
from win32event import WaitForSingleObject
from time import sleep
from subprocess import call, Popen, PIPE
from os import PathLike, path


class cmd:
    def __new__(cls, *args, cwd: str | PathLike[str] = r"C:\Window\System32", init: str = None, waitTime: int | float = 0.5):
        ins = winAuto(*args, cwd=cwd, init=init, waitTime=waitTime)
        ins.begin()
        return ins


class winAuto:
    def __init__(self, *args, cwd: str | PathLike[str] = r"C:\Window\System32", init: str = None, waitTime: int | float = 0.5):

        self._args = args

        self._cwd = cwd

        self._init = init if init else ["color 80", "cls"]

        self._shell = Dispatch("WScript.Shell")

        self._waitTime = waitTime

        self.windows = []

    @property
    def shell(self) -> CDispatch: return self._shell

    @property
    def args(self): return self._args

    def findCmd(self, *, keyword: str = "cmd"):

        self.getAllTitle()

        return FindWindow(None, [i for i in self.windows if keyword in i][0])

    def _codeBack(self, hwnd, _):
        if IsWindowVisible(hwnd) and (text := GetWindowText(hwnd)):
            self.windows.append(text)

    def getAllTitle(self):
        EnumWindows(self._codeBack, None)

    def sendInstruct(self, instruct: str, *, waitTime: int = None, enter: bool = True):
        sleep(waitTime if waitTime else self._waitTime)

        self.shell.SendKeys(instruct + ("{ENTER}" if enter else ''))

    def begin(self):
        ShellExecute(0, 'open', 'cmd.exe', '', self._cwd, 1)

        sleep(self._waitTime)

        hwnd = self.findCmd()

        try:
            SetForegroundWindow(hwnd)

            self.sendInstruct(fr"{' & '.join(self._init + list(self.args))}{{ENTER}}")

        except Exception as e:
            raise e from ConnectionError("没找到句柄?")


if __name__ == '__main__':
    ins = cmd("git status", cwd=r"D:\xst_project_202212\codeSet\Python")
    ins.sendInstruct("git add .")
