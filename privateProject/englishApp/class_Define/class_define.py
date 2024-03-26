#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

from PyQt5.Qt import (
    QObject, QEvent, QIcon, Qt, QAction, QCompleter,
    QMainWindow,
    QLineEdit, QPushButton, QLabel,
    pyqtSignal)
from privateProject.englishApp.func_Define.func_define import \
    fastset, passshow, passcheck, checklen, FilterInstall, tolalpos
from itertools import accumulate
from functools import partial


class PremiseError(Exception):
    """
    一个自定义的错误类

    Attributes:
        message: 传入的错误信息.
    Methods:
        __str__: 改变保存的字符串返回.
    """

    def __init__(self, message: str = "No message"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class LineEdit(QLineEdit):
    """
    文本输入框

    Attributes:
        click: 添加点击信号,连接至pyqtSignal().
        lossfocus: 添加失焦,连接至pyqtSignal()
    Methods:
        mousePressEvent: 点击事件发出信号.
        focusOutEvent: 失焦事件发出信号.
    """
    click = pyqtSignal()
    lossfocus = pyqtSignal()

    def mousePressEvent(self, event):
        # emit()可以使其附加有发射信号的属性
        self.click.emit()
        super().mousePressEvent(event)

    def focusOutEvent(self, event):
        self.lossfocus.emit()
        super().focusOutEvent(event)


class EventFilter(QObject):
    """
    一个事件过滤器

    Methods:
        eventFilter: .
    """

    def eventFilter(self, obj, event):
        # 聚焦事件
        if event.type() == QEvent.FocusIn:
            pass
        # 失焦事件
        if event.type() == QEvent.FocusOut:
            pass
        return False


class PosManger:
    """
    水平方向尺寸与位置管理器.

    Attributes:
        hight: 块高.
        tosize: 每一个控件的尺寸.将返回[(元组1)第一个控件的高宽, (元组2)第二个控件的高宽, (元组3),...]
        topos: 每一个控件的位置(返回形式如上).
    """

    def __init__(self, begpos: tuple = (0, 0), totalsize: tuple = (80, 60), *, ratio: tuple = None, spacing: int = 0):
        """
        初始化函数

        :data begpos: 开始位置.(默认为(0, 0))
        :type begpos: tuple
        :data totalsize: 总的尺寸.(这些控件将占据多大的空间)(默认为(80, 60))
        :type totalsize: tuple
        :data ratio: 每一个控件的比例,且所有返回的列表都会根据该元组的顺序.
        :type ratio: tuple
        :data spacing: 每一个控件间的间隔.(暂时无法定制)
        :type spacing: int
        """
        self.hight = totalsize[1]
        self.tosize = \
            [((totalsize[0] - (len(ratio) - 1) * spacing) * i / list(accumulate(ratio))[-1], self.hight) for i in ratio]
        self.topos = [(begpos[0] + i * spacing + (list(accumulate(map(lambda x: x[0], self.tosize)))[i - 1] if i else 0)
                       , begpos[1]) for i in range(len(ratio))]


class MainWindow(QMainWindow):
    """
    登录界面

    Attributes:
        属性名: 属性值.
    Methods:
        方法名: 方法职能.
    """

    def __init__(self):
        super().__init__()
        self.statusBar()
        self.setStatusTip("登录界面")
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon(r"/Python/englishApp/素材库/软件图标.ico"))
        self.resize(640, 450)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint | Qt.MSWindowsFixedSizeDialogHint)
        # | Qt.WindowContextHelpButtonHint)
        self.begpos, self.inpos1, self.inpos2 = None, None, None
        self.btn1_1, self.inp1_1, self.inp1_2, self.labr, self.lab1_1, self.lab1_2, self.btn1_2 = (None for i in range(7))
        self.prorun()

    def inpos(self, begpos):
        self.begpos = begpos
        self.inpos1 = PosManger(self.begpos[0], (364, 30), ratio=(2, 13, 1), spacing=20)
        self.inpos2 = PosManger(self.begpos[1], (320, 30), ratio=(2, 13), spacing=20)

    # 登录按键
    def login(self):
        self.btn1_1 = QPushButton("登    录", self) if not self.btn1_1 else self.btn1_1
        fastset(self.btn1_1, {"Index": 1}, size=(320, 60), pos=(160, 350))
        self.btn1_1.setEnabled(False)

    # 账户输入框
    def accinput(self):
        self.inp1_1 = LineEdit(self) if not self.inp1_1 else self.inp1_1
        fastset(self.inp1_1, {"Index": 2}, size=self.inpos1.tosize[1], pos=self.inpos1.topos[1],
                show_time=3000, toolTip_text="11位数字号码")
        self.inp1_1.setPlaceholderText("请输入您的电话号码")
        self.inp1_1.setFocus()
        self.inp1_1.setCompleter(QCompleter(["18028763642", "18028763230"], self.inp1_1))

    # 密码输入框
    def passwinput(self):
        self.inp1_2 = LineEdit(self) if not self.inp1_2 else self.inp1_2
        fastset(self.inp1_2, {"Index": 3}, size=self.inpos2.tosize[1], pos=self.inpos2.topos[1],
                show_time=3000, toolTip_text="您的密码")
        self.inp1_2.setPlaceholderText("请输入密码")
        self.inp1_2.setClearButtonEnabled(True)
        act = QAction(QIcon(r"D:\xst_project_202212\Python\privateProject\englishApp\素材库\隐藏密码.png"), "显示密码",
                      self)
        self.inp1_2.addAction(act, QLineEdit.TrailingPosition)
        self.inp1_2.setEchoMode(QLineEdit.Password)
        act.triggered.connect(lambda: passshow(act, self.inp1_2))

    # 符合/不符合提示图标
    def iconturn(self):
        self.labr = QLabel(self) if not self.labr else self.labr
        fastset(self.labr, {"Index": 6}, size=self.inpos1.tosize[2], pos=self.inpos1.topos[2])

    # 标签: 账户
    def acclabel(self):
        self.lab1_1 = QLabel("账户:", self) if not self.lab1_1 else self.lab1_1
        fastset(self.lab1_1, {"Index": 4}, size=self.inpos1.tosize[0], pos=self.inpos1.topos[0],
                staTip_text="账户信息")

    # 标签: 密码
    def passlabel(self):
        self.lab1_2 = QLabel("密码:", self) if not self.lab1_2 else self.lab1_2
        fastset(self.lab1_2, {"Index": 5}, size=self.inpos2.tosize[0], pos=self.inpos2.topos[0],
                staTip_text="密码")

    # 注册
    def regist(self):
        self.btn1_2 = QPushButton("注册", self) if not self.btn1_2 else self.btn1_2
        fastset(self.btn1_2, {"Index": 7}, size=(60, 40), pos=(580, 410), toolTip_text="点击注册")
        self.btn1_2.setFlat(True)

    # 信号绑定
    def signt(self):
        self.inp1_1.textChanged.connect(
            lambda newtext: checklen(newtext, self.inp1_1, aimer1=self.btn1_1, aimer2=self.labr, aimer3=self.inp1_2))
        self.inp1_2.textChanged.connect(
            lambda: checklen(self.inp1_1.text(), self.inp1_1, aimer1=self.btn1_1, aimer2=self.labr, aimer3=self.inp1_2))
        self.btn1_1.pressed.connect(lambda: passcheck(self.inp1_1, self.inp1_2))
        self.btn1_2.pressed.connect(lambda: self.refresh((800, 600)))

        FilterInstall(EventFilter(), self.inp1_1, self.inp1_2)

    def prorun(self, begpos: tuple = ((160, 180), (160, 240))):
        self.inpos(begpos)
        self.login()
        self.accinput()
        self.passwinput()
        self.iconturn()
        self.acclabel()
        self.passlabel()
        self.regist()
        self.signt()

    def refresh(self, winsize: tuple):
        self.resize(winsize[0], winsize[1])
        newtolalpos = partial(tolalpos, winsize)
        self.prorun((newtolalpos((364, 30), posdrift=(0, -22)), newtolalpos((320, 30), posdrift=(0, 22))))
