#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/15 8:38
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon, QScreen
from PyQt6.QtCore import Qt
from win32print import GetDeviceCaps
from functools import cached_property
from win32con import DESKTOPHORZRES, DESKTOPVERTRES
from win32api import EnumDisplayMonitors
from win32gui import GetDC, ReleaseDC
from typing import Literal
from sys import argv, exit


r"""
class Options:  
    OPTION_A = 1 << 0  # 二进制：0001  
    OPTION_B = 1 << 1  # 二进制：0010  
    OPTION_C = 1 << 2  # 二进制：0100  
    # 可以继续添加更多选项...  
  
def combine_options(*args):  
    组合多个选项
    result = 0  
    for option in args:  
        result |= option  # 使用管道符组合选项  
    return result  
  
# 使用示例  
combined = combine_options(Options.OPTION_A, Options.OPTION_C)  
print(bin(combined))  # 输出应该是类似 '0b1001'，表示选项A和选项C被设置了  
  
# 检查某个选项是否被设置  
def has_option(combined, option):  
    检查组合中是否包含某个选项 
    return (combined & option) == option  
  
# 检查示例  
print(has_option(combined, Options.OPTION_A))  # 应该输出 True  
print(has_option(combined, Options.OPTION_B))  # 应该输出 False
"""


class mainWindow(QMainWindow):
    def __init__(self, _app: QApplication = None, *, ignoreSecondaryScreen: bool = False):
        self._app = _app
        self._flagISS = ignoreSecondaryScreen

        super().__init__()
        self.conponentInit()

        # self.setWindowIcon(QIcon(""))

    @property
    def app(self):
        if self._app: return self._app
        else:
            try:
                global app
                return app
            except NameError as e:
                raise NameError(
                    "试图找到全局变量'app',这是一个QApplication类,但我们无法找到,你需要在mainWindow的初始化方法中手动向'_app'传入该参数!") from ValueError(
                    "位置参数'_app'没有接受到参数!")

    @property
    def flagISS(self): return self._flagISS

    @cached_property
    def screenList(self) -> list[QScreen]: return [self.app.primaryScreen()]  # if self.flagISS else self.app.screens()

    @cached_property
    def mainScreen(self) -> QScreen: return self.screenList[0]

    def getSize(self, screen: QScreen = None, *, mode: Literal["phy", "dpi", "rel"] = "phy"):
        if screen is None: screen = self.mainScreen

        match mode:
            case "phy":
                return (size := screen.size()).width(), size.height()
            case "dpi":
                return screen.physicalDotsPerInchX(), screen.physicalDotsPerInchY()
            case "rel":
                # hdc = EnumDisplayMonitors(None, None)[self.screenList.index(screen)]
                hdc = GetDC(None)
                width, height = GetDeviceCaps(hdc, DESKTOPHORZRES), GetDeviceCaps(hdc, DESKTOPVERTRES)
                ReleaseDC(None, hdc)
                return width, height
            case _:
                raise ValueError(
                    f"位置参数'mode'被传入了一个非期望的值'{mode}'!")

    def setAutoSize(self, screen: QScreen = None, *, xRatio: float = 0.8, yRatio: float = 0.8):
        if any([xRatio > 1, yRatio > 1]):
            raise ValueError(
                "参数'XRation'或'yRatio'不能大于1!")

        self.resize(int((size := self.getSize(screen))[0] * xRatio), int(size[1] * yRatio))

    def conponentInit(self):
        self.statusBar()
        self.setStatusTip("TM")
        self.setWindowTitle("TM")
        self.setAutoSize()
        self.setWindowFlags(
            # Qt.WindowType.WindowCloseButtonHint |  # 只保留关闭按钮
            Qt.WindowType.WindowStaysOnTopHint
            # | Qt.WindowType.MSWindowsFixedSizeDialogHint  # 禁止伸缩页面
            # | Qt.WindowType.WindowContextHelpButtonHint  # 帮助按钮
        )


if __name__ == '__main__':
    app = QApplication(argv)

    main = mainWindow(ignoreSecondaryScreen=True)
    main.show()

    exit(app.exec())