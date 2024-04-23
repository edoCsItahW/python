#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
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
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QGraphicsScene, QGraphicsPixmapItem, QDialog,
                             QPushButton, QVBoxLayout, QBoxLayout, QSizePolicy, QSpacerItem, QLabel)
from PyQt6.QtGui import QIcon, QResizeEvent, QScreen, QPixmap, QPalette, QBrush, QPaintEvent, QMouseEvent
from PyQt6.QtCore import Qt
from win32print import GetDeviceCaps
from functools import cached_property, partial, cache
from win32con import DESKTOPHORZRES, DESKTOPVERTRES
from win32api import EnumDisplayMonitors
from win32gui import GetDC, ReleaseDC
from typing import Literal, Callable
from sys import argv, exit
from typing import overload


ignoreSecondaryScreen: int = 1 << 0
# TODO: 将widget和setOption独立为类


class mainWindow(QMainWindow):
    flagDict = {
        ignoreSecondaryScreen: "ignoreSecondaryScreen"
    }

    def __init__(self, _app: QApplication = None, *, flags: int):
        self._app = _app
        self._flag = flags
        self._eventDoList = []

        super().__init__()
        self.attrsInit()
        self.conponentInit()

        # self.setWindowIcon(QIcon(""))

    # 参转私有
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
    def flag(self): return self._flag

    @property
    def eventDoList(self): return self._eventDoList

    @eventDoList.setter
    def eventDoList(self, value): self._eventDoList = value

    # 私有
    @cached_property
    def body(self):
        body = QWidget(self)

        body.setObjectName("body")

        body.resize((size := self.size()).width(), size.height())

        self.setCentralWidget(body)

        return body

    @cached_property
    def screenList(self) -> list[QScreen]: return [self.app.primaryScreen()]  # if self.flagISS else self.app.screens()

    @cached_property
    def mainScreen(self) -> QScreen: return self.screenList[0]

    @cache
    def dayBarDict(self, parent):

        dayDict = {obj: self.createWidget(parent, objectName=obj) for obj in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}

        for day in dayDict.values():

            self.dayBarInit(day)

        return dayDict

    # 普通方法
    def _flagsParser(self):
        return {name: (self.flag & flag) == flag for flag, name in self.flagDict.items()}

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

    def setVCenter(self, widget: QWidget, *, keep: bool = True):
        func = lambda _widget: _widget.move(_widget.pos().x(), int((_widget.parent().size().height() - _widget.size().height()) / 2))

        if keep: self._eventDoList.append(self.warpFunc(func, widget))

        func(widget)

    def setHCenter(self, widget: QWidget, *, keep: bool = True):
        func = lambda _widget: _widget.move(int((_widget.parent().size().width() - _widget.size().width()) / 2), _widget.pos().y())

        if keep: self._eventDoList.append(self.warpFunc(func, widget))

        func(widget)

    def setVPercentageSize(self, widget: QWidget, *, vertical: float = 0.8, keep: bool = True):
        def func(_widget: QWidget, *, _vertical: float):
            sizeX = widget.size().width()

            sizeY_f = widget.parent().size().height()

            widget.resize(sizeX, int(sizeY_f * vertical))

        self.eventDoList.append(self.warpFunc(func, widget, _vertical=vertical))

        func(widget, _vertical=vertical)

    def setHPercentageSize(self, widget: QWidget, *, horizontal: float = 0.8, keep: bool = True):
        def func(_widget: QWidget, *, _horizontal: float):
            sizeY = widget.size().height()

            sizeX_f = widget.parent().size().width()

            widget.resize(int(sizeX_f * horizontal), sizeY)

        self.eventDoList.append(self.warpFunc(func, widget, _horizontal=horizontal))

        func(widget, _horizontal=horizontal)

    def setPercentageSize(self, widget: QWidget, *, vertical: float = 0.8, horizontal: float = 0.8, keep: bool = True):
        self.setVPercentageSize(widget, vertical=vertical, keep=keep)
        self.setHPercentageSize(widget, horizontal=horizontal, keep=keep)

    def setCenter(self, widget: QWidget, *, keep: bool = True):
        self.setHCenter(widget, keep=keep)
        self.setVCenter(widget, keep=keep)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        for func in self.eventDoList:
            func()

    @staticmethod
    def createWidget(parent, *, objectName: str = ""):
        widget = QWidget(parent)
        if objectName: widget.setObjectName(objectName)

        return widget

    @staticmethod
    def warpFunc(func: Callable, *args, **kwargs):
        return lambda: func(*args, **kwargs)

    @staticmethod
    def _valueLimit(value: int | float):
        if value < 0 or value > 1:
            raise ValueError(
                "参数'vertical'或'horizontal'中的值不能大于1!")

    def _checkValue(self, valueList: list[int | float]):
        for value in valueList:
            self._valueLimit(value)

    def attrsInit(self):
        self.statusBar()

        self.setWindowIcon(QIcon(r"./static/imgs/timeA.ico"))

        self.setStatusTip("TM")
        self.setWindowTitle("TM")
        self.setAutoSize()
        self.setWindowFlags(
            # Qt.WindowType.WindowCloseButtonHint |  # 只保留关闭按钮
            Qt.WindowType.WindowStaysOnTopHint
            # | Qt.WindowType.MSWindowsFixedSizeDialogHint  # 禁止伸缩页面
            # | Qt.WindowType.WindowContextHelpButtonHint  # 帮助按钮
        )

    def conponentInit(self):

        dayTable = self.createWidget(self.body, objectName="dayTable")

        self.setPercentageSize(dayTable, vertical=0.95, horizontal=0.95, keep=True)

        self.setCenter(dayTable, keep=True)

        layout = QHBoxLayout(dayTable)

        for bar in self.dayBarDict(dayTable).values():
            layout.addWidget(bar)

    def dayBarInit(self, day: QWidget):
        day.setStyleSheet("background-image: url(./static/imgs/add.ico); background-position: center; background-repeat: no-repeat;")

        def func(event: QMouseEvent):
            widget = QDialog(self)
            # TODO: 完善Dialog

            widget.setStyleSheet("background-color: red;")

            widget.resize(600, 400)

            layout = QVBoxLayout(widget)

            layout.addWidget(QLabel("test", widget))

            widget.show()

        day.mousePressEvent = func


if __name__ == '__main__':
    app = QApplication(argv)

    with open(r"./static/qss/style.qss", "r", encoding="utf-8") as file:
        style = file.read()

    main = mainWindow(flags=ignoreSecondaryScreen)
    main.setStyleSheet(style)
    main.show()

    exit(app.exec())
