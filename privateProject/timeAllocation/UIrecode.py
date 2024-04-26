#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/22 下午7:39
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from sys import argv
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QHBoxLayout, QDialog, QVBoxLayout, QLineEdit, QTimeEdit
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QCloseEvent, QMouseEvent, QResizeEvent, QIcon, QScreen, QEnterEvent
from functools import cached_property
from typing import Callable, Literal, Any
from types import FunctionType
from win32print import GetDeviceCaps
from win32con import DESKTOPHORZRES, DESKTOPVERTRES
from win32gui import GetDC, ReleaseDC
from traceback import format_exc


class funcSet:
    @staticmethod
    def create(parent, _type, objectName: str = None, styleSheet: str = None):
        pass

    @staticmethod
    def createWidget(parent, *, objectName: str = None, styleSheet: str = None) -> QWidget:
        widget = QWidget(parent)

        if objectName:
            widget.setObjectName(objectName)

        if styleSheet:
            widget.setStyleSheet(styleSheet)

        return widget

    @staticmethod
    def getSize(screen: QScreen, *, mode: Literal["phy", "dpi", "rel"] = "phy"):
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

    @staticmethod
    def setAutoSize(screen: QScreen, aimWidget: QWidget, *, xRatio: float = 0.8, yRatio: float = 0.8):
        if any([i > 1 or i < 0 for i in (xRatio, yRatio)]):
            raise ValueError(
                "参数'XRation'或'yRatio'不能大于1!")

        aimWidget.resize(int((size := funcSet.getSize(screen))[0] * xRatio), int(size[1] * yRatio))


class posOptons:
    commonFlag = []

    def __init__(self):
        self._eventList = []

    @property
    def eventList(self):
        return self._eventList

    @eventList.setter
    def eventList(self, value):
        self._eventList = value

    @staticmethod
    def warpFunc(func: Callable, *args, **kwargs):
        return lambda: func(*args, **kwargs)

    def setVCenter(self, widget: QWidget, eventList: list = None, *, keep: bool = True):
        if eventList is None: eventList = self.eventList

        func = lambda _widget: _widget.move(_widget.pos().x(), int((_widget.parent().size().height() - _widget.size().height()) / 2))

        if keep: eventList.append(self.warpFunc(func, widget))

        func(widget)

    def setHCenter(self, widget: QWidget, eventList: list = None, *, keep: bool = True):
        if eventList is None: eventList = self.eventList

        func = lambda _widget: _widget.move(int((_widget.parent().size().width() - _widget.size().width()) / 2), _widget.pos().y())

        if keep: eventList.append(self.warpFunc(func, widget))

        func(widget)

    def setVPercentageSize(self, widget: QWidget, eventList: list = None, *, vertical: float = 0.8, keep: bool = True):
        if eventList is None: eventList = self.eventList

        def func(_widget: QWidget, *, _vertical: float):
            sizeX = widget.size().width()

            sizeY_f = widget.parent().size().height()

            widget.resize(sizeX, int(sizeY_f * vertical))

        eventList.append(self.warpFunc(func, widget, _vertical=vertical))

        func(widget, _vertical=vertical)

    def setHPercentageSize(self, widget: QWidget, eventList: list = None, *, horizontal: float = 0.8, keep: bool = True):
        if eventList is None: eventList = self.eventList

        def func(_widget: QWidget, *, _horizontal: float):
            sizeY = widget.size().height()

            sizeX_f = widget.parent().size().width()

            widget.resize(int(sizeX_f * horizontal), sizeY)

        eventList.append(self.warpFunc(func, widget, _horizontal=horizontal))

        func(widget, _horizontal=horizontal)

    def setPercentageSize(self, widget: QWidget, eventList: list = None, *, vertical: float = 0.8, horizontal: float = 0.8, keep: bool = True):
        if eventList is None: eventList = self.eventList

        self.setVPercentageSize(widget, vertical=vertical, keep=keep)
        self.setHPercentageSize(widget, horizontal=horizontal, keep=keep)

    def setCenter(self, widget: QWidget, eventList: list = None, *, keep: bool = True):
        if eventList is None: eventList = self.eventList

        self.setHCenter(widget, keep=keep)
        self.setVCenter(widget, keep=keep)

    def fullPerent(self, widget: QWidget, eventList: list = None, keep: bool = True):
        if eventList is None: eventList = self.eventList

        def func(_widget: QWidget):
            _widget.resize((size := _widget.parent().size()).width(), size.height())

        if keep: eventList.append(self.warpFunc(func, widget))

        func(widget)

    @staticmethod
    def hLayout(parent: QWidget, widgets: dict[QWidget, int]) -> QWidget:
        hlayout = QHBoxLayout(widget := funcSet.createWidget(parent))

        for w, s in widgets.items():
            hlayout.addWidget(w, stretch=s)

        widget.setLayout(hlayout)

        return widget

    @staticmethod
    def vLayout(parent: QWidget, widgets: dict[QWidget, int]) -> QWidget:
        hlayout = QVBoxLayout(widget := funcSet.createWidget(parent))

        for w, s in widgets.items():
            hlayout.addWidget(w, stretch=s)

        return widget

    @staticmethod
    def PFvLayout(parent: QWidget, widgets: dict[FunctionType, int]) -> tuple[QWidget, list]:
        hlayout = QVBoxLayout(widget := funcSet.createWidget(parent))

        widgetList = []

        for func, s in widgets.items():
            hlayout.addWidget(w := func(widget), stretch=s)
            widgetList.append(w)

        return widget, *widgetList

    @staticmethod
    def PFhLayout(parent: QWidget, widgets: dict[int, FunctionType]):

        hlayout = QHBoxLayout(widget := funcSet.createWidget(parent))

        widgetList = []

        for s, func in widgets.items():
            hlayout.addWidget(w := func(widget), stretch=s)
            widgetList.append(w)

        return widget, *widgetList


class mainWindow(QMainWindow):
    def __init__(self, _app: QApplication = None, *, styleSheet: str = None):
        self._app = _app
        self._styleSheet = styleSheet
        self._posOpt = posOptons()

        super().__init__()

        self.attrsInit()
        self.conponentInit()

        self.show()

    @property
    def app(self) -> QApplication:
        """
        获取QApplication实例

        :return: QApplication实例
        :rtype: QApplication
        """
        if self._app: return self._app
        else:
            try:
                global app
                return app
            except NameError as e:
                raise NameError(
                    "试图找到全局变量'app',这是一个QApplication类,但我们无法找到,你需要在mainWindow的初始化方法中手动向'_app'传入该参数!") from ValueError(
                    "位置参数'_app'没有接受到参数!")

    @cached_property
    def body(self):
        body = funcSet.createWidget(self, objectName='body', styleSheet='background-color: rgba(38, 38, 38, 0.56);')

        body.resize((size := self.size()).width(), size.height())

        self.setCentralWidget(body)

        return body

    @property
    def styleSheet(self):
        if self._styleSheet:
            with open(self._styleSheet, "r", encoding="utf-8") as file:
                return file.read()

        return self._styleSheet

    @property
    def posOpt(self):
        return self._posOpt

    def attrsInit(self):
        self.statusBar()

        self.setWindowIcon(QIcon(r"./static/imgs/timeA.ico"))

        self.setStyleSheet(self.styleSheet)

        self.setStatusTip("TM")
        self.setWindowTitle("TM")
        funcSet.setAutoSize(self.app.primaryScreen(), self)
        self.setWindowFlags(
            # Qt.WindowType.WindowCloseButtonHint |  # 只保留关闭按钮
            Qt.WindowType.WindowStaysOnTopHint
            # | Qt.WindowType.MSWindowsFixedSizeDialogHint  # 禁止伸缩页面
            # | Qt.WindowType.WindowContextHelpButtonHint  # 帮助按钮
        )

    def conponentInit(self):
        dayTable = funcSet.createWidget(self.body, objectName='dayTable')

        self.posOpt.setPercentageSize(dayTable, vertical=0.95, horizontal=0.95, keep=True)
        self.posOpt.setCenter(dayTable, keep=True)

        layout = QHBoxLayout(dayTable)

        for name, bar in self.spawnDayBar(dayTable).items():
            # layout.addWidget(bar)
            nameLabel = QLabel(name, dayTable)

            nameLabel.setStyleSheet("color: #cccccc; font-size: 40px; border: 2px solid #cccccc; border-radius: 5px;")

            nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout.addWidget(self.posOpt.vLayout(dayTable, {nameLabel: 1, bar: 14}))

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        for func in self.posOpt.eventList:
            func()

    def spawnDayBar(self, parent: QWidget) -> {str: QWidget}:
        dayDict = {obj: DayBar(parent, objectName=obj, styleSheet=self.styleSheet) for obj in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']}

        return dayDict


class DayBar(QWidget):
    def __init__(self, parent: QWidget = None, *, objectName: str = None, styleSheet: str = None):
        super().__init__(parent)

        self._objectName = objectName
        self._styleSheet = styleSheet
        self._posOpt = posOptons()

        self.attrsInit()
        self.conponentInit()

    @property
    def objectName(self):
        return self._objectName

    @property
    def styleSheet(self):
        return self._styleSheet

    @property
    def posOpt(self):
        return self._posOpt

    @property
    def body(self):
        body = funcSet.createWidget(self, objectName="body", styleSheet="""
        background-image: url(./static/imgs/add.ico); 
        background-repeat: no-repeat; 
        background-position: center;
        """)

        self.posOpt.fullPerent(body, keep=True)

        return body

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

        if "dialog" not in posOptons.commonFlag:
            dialog = TaskOption(self.body, objectName="taskOption")

            posOptons.commonFlag.append("dialog")

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        for func in self.posOpt.eventList:
            func()

    def attrsInit(self):
        if self.objectName:
            self.setObjectName(self.objectName)

        if self.styleSheet:
            self.setStyleSheet(self.styleSheet)

    def conponentInit(self):
        self.body

    def enterEvent(self, event: QEnterEvent):
        super().enterEvent(event)

        if "dialog" not in posOptons.commonFlag:
            self.setStyleSheet("background-color: #cccccc;")

    def leaveEvent(self, event: QEvent):
        super().leaveEvent(event)

        self.setStyleSheet("background-color: #8b8b8b;")


class TaskOption(QDialog):
    def __init__(self, parent: QWidget = None, *, objectName: str = None, styleSheet: str = None):
        super().__init__(parent)

        self._objectName = objectName
        self._styleSheet = styleSheet
        self._posOpt = posOptons()

        self.attrsInit()
        self.conponentInit()

        self.show()

    @property
    def objectName(self):
        return self._objectName

    @property
    def styleSheet(self):
        return self._styleSheet

    @property
    def posOpt(self):
        return self._posOpt

    @property
    def body(self):
        body = funcSet.createWidget(self, objectName="body", styleSheet="background-color: transparent;")

        self.posOpt.fullPerent(body, keep=True)

        return body

    def attrsInit(self):
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.MSWindowsFixedSizeDialogHint | Qt.WindowType.WindowCloseButtonHint)

        if self.objectName:
            self.setObjectName(self.objectName)

        self.setStyleSheet("background-image: url(); background-color: transparent; background-color: #818181;")

        if self.styleSheet:
            self.setStyleSheet(self.styleSheet)

        self.resize(600, 400)

    def addConponent(self, parent: QWidget, funcDict: dict[int: dict[QWidget, tuple]], *, otherAttr: dict[int: dict[str: Any]] = None, execFunc: dict[int: dict[str: Any]] = None):

        def _(d: dict[int: dict[QWidget, tuple]]):
            key, value = (k := list(d.keys())[0]), d[k]

            return lambda _widget: key(*value, _widget) if value and value[0] is not None else key(_widget)

        widgetDict = {i: _(d) for i, d in funcDict.items()}

        result = self.posOpt.PFhLayout(parent, widgetDict)

        if otherAttr:
            for i, d in otherAttr.items():
                for k, v in d.items():
                    setattr(result[i], k, v)

        if execFunc:
            for i, d in execFunc.items():
                for k, v in d.items():
                    try:
                        getattr(result[i], k)(v)
                    except Exception as e:
                        print(k, v, e, result)

        return result

    def conponentInit(self):

        vlayout = QVBoxLayout(self.body)

        widget1, label1, lineEdit1 = self.addConponent(self.body, {1: {QLabel: ("任务名", )}, 4: {QLineEdit: (None, )}}, execFunc={1: {"setStyleSheet": "color: #cccccc; font-weight: bold; font-size: 20px;"}, 2: {"setPlaceholderText": "...", "setStyleSheet": "background-color: #595959; font-size: 20px;"}})

        vlayout.addWidget(widget1)

        widget2, label2, timeEdit1 = self.addConponent(self.body, {1: {QLabel: ("开始时间", )}, 4: {QTimeEdit: (None, )}}, execFunc={1: {"setStyleSheet": "color: #cccccc; font-weight: bold; font-size: 20px;"}, 2: {"setDisplayFormat": "hh:mm"}})

        vlayout.addWidget(widget2)

        widget3, label3, timeEdit2 = self.addConponent(self.body, {1: {QLabel: ("结束时间",)}, 4: {QTimeEdit: (None,)}}, execFunc={1: { "setStyleSheet": "color: #cccccc; font-weight: bold; font-size: 20px;"}, 2: {"setDisplayFormat": "hh:mm"}})

        vlayout.addWidget(widget3)

    def closeEvent(self, event: QCloseEvent):
        super().closeEvent(event)

        if "dialog" in posOptons.commonFlag:
            posOptons.commonFlag.remove("dialog")

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

        for func in self.posOpt.eventList:
            func()


if __name__ == '__main__':
    app = QApplication(argv)

    main = mainWindow(styleSheet='./static/qss/style.qss')

    exit(app.exec())

