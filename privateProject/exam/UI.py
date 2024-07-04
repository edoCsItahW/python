#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/6/28 上午8:16
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt6.QtGui import QScreen
from typing import Literal
from questionType import base
from os import PathLike, path
from pandas import DataFrame, read_csv
from functools import cached_property
from win32con import DESKTOPHORZRES, DESKTOPVERTRES
from win32gui import GetDC, ReleaseDC
from win32print import GetDeviceCaps


class MainWindow(QMainWindow):
    def __init__(self, csvDirPath: str | PathLike, _app: QApplication = None):
        super().__init__()
        self._app = _app
        self._csvDirPath = csvDirPath

        if not path.exists(self._csvDirPath):
            raise FileNotFoundError(
                f"{self._csvDirPath} not found")

        if not path.isdir(self._csvDirPath):
            raise NotADirectoryError(
                f"{self._csvDirPath} is not a directory")

        self._mainWidget = QWidget(self)
        self._mainWidget.resize(self.width(), self.height())
        self.setAutoSize()
        self.statusBar()

    @property
    def app(self):
        if self._app:
            return self._app
        else:
            try:
                global app
                return app
            except NameError as e:
                raise NameError(
                    "试图找到全局变量'app',这是一个QApplication类,但我们无法找到,你需要在mainWindow的初始化方法中手动向'_app'传入该参数!") from ValueError(
                    "位置参数'_app'没有接受到参数!")

    @cached_property
    def screenList(self) -> list[QScreen]:
        return [self.app.primaryScreen()]  # if self.flagISS else self.app.screens()

    @cached_property
    def mainScreen(self) -> QScreen:
        return self.screenList[0]

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
        if any([i > 1 or i < 0 for i in (xRatio, yRatio)]):
            raise ValueError(
                "参数'XRation'或'yRatio'不能大于1!")

        self.resize(int((size := self.getSize(screen))[0] * xRatio), int(size[1] * yRatio))

    def showQuestion(self, *args: type[base]):
        for pType in args:
            if not issubclass(pType, base):
                raise TypeError(
                    f"{pType} is not a subclass of {base}")

            shower = pType()

            df = read_csv(path.join(self._csvDirPath, f"{pType.name[0] if isinstance(pType.name, list) else pType.name}.csv"), encoding="gbk")

            shower.showUI(self._mainWidget, df)
