#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

from PyQt5.Qt import *
from constantPackage.sqlTools.sqlTools import sqlManger


def setattribute(Object: QObject, dict_property: dict) -> None:
    """
    简化属性的设置过程.

    :data Object: 将要被设置的目标控件.
    :type Object: QObject
    :data dict_property: 添加的属性,以字典形式接收.
    :type dict_property: dict
    :return: 操作执行函数不做返回.
    :retype: None
    """
    for i in dict_property.keys():
        Object.setProperty(i, dict_property[i])


def fastset(aim_Object: QObject, pro_dict: dict, *,
            size: tuple = (0, 0), pos: tuple = (0, 0),
            show_time: int = None,
            text: str = "", staTip_text: str = "", toolTip_text: str = ""):
    """
    简化控件基本设置,包括(
        1.属性
        2.尺寸
        3.位置
        4.鼠标提示条展示的延迟时间
        5.控件内文本
        6.控件对应在状态栏的提示信息
        7.控件对应在鼠标停留其上时展示的提示
    )

    :data aim_Object: 将要被设置的目标控件.
    :type aim_Object: QObject
    :data pro_dict: 属性字典
    :type pro_dict: dict
    :data size: 尺寸.(默认值:(0, 0))
    :type size: tuple
    :data pos: 位置.(默认值:(0, 0))
    :type pos: tuple
    :data show_time: 鼠标提示条展示的延迟时间.
    :type show_time: int.(单位毫秒,一般以1000为步长设置)
    :data text: 控件内文本.
    :type text: str
    :data staTip_text: 控件对应在状态栏的提示信息.
    :type staTip_text: str
    :data toolTip_text: 控件对应在鼠标停留其上时展示的提示 .
    :type toolTip_text: str
    :return: 操作执行函数不做返回.
    :retype: None
    """
    aim_Object.resize(int(size[0]), int(size[1]))
    aim_Object.move(int(pos[0]), int(pos[1]))
    if not aim_Object.text():
        aim_Object.setText(text)

    # 添加属性
    if pro_dict:
        setattribute(aim_Object, pro_dict)

    # 判断与抛错
    # if (staTip_text or toolTip_text) and isinstance(aim_Object, QWidget):
    #     aim_Object.statusBar()
    if show_time and not toolTip_text:
        from privateProject.englishApp.class_Define import PremiseError
        raise PremiseError("show_time 应定义在 toolTip_text 之前.")

    # 其它设置
    if staTip_text:
        aim_Object.setStatusTip(staTip_text)
    if toolTip_text:
        aim_Object.setToolTip(toolTip_text)


def FilterInstall(aimfilter, *args: QObject):
    """
    事件过滤器安装器.

    :data aimfilter: 将要被安装的事件过滤器.
    :type aimfilter: EventFilter
    :data args: 需要安装此过滤器的多个目标控件.
    :type args: QObject
    :return: 操作执行函数不做返回.
    :retype: None
    """
    for obj in args:
        obj.installEventFilter(aimfilter)


def checklen(insign: str, conter: QObject, *,
             aimer1: QAbstractButton = False,
             aimer2: QAbstractButton = False,
             aimer3: QAbstractButton = False):
    """
    信号考核.

    :data insign: 传入信号的文本.
    :type insign: str
    :data conter: 信号传出者.
    :type conter: QObject
    :data aimer1: 受影响的控件.
    :type aimer1: QAbstractButton
    :data aimer2: 受影响的控件.
    :type aimer2: QAbstractButton
    :data aimer3: 受影响的控件.
    :type aimer3: QAbstractButton
    :return: 返回什么.
    :retype: 返回值的类型
    """
    if conter.property("Index") == 2 and len(insign) == 11 and insign.isdigit():
        aimer2.setPixmap(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton).pixmap(24, 24))
        aimer2.setVisible(True)
        if aimer3.text():
            aimer1.setEnabled(True)
            aimer1.setStyleSheet(
                "background-color: lightblue;"
                "color: black;"
                "font-size: 16pt;"
            )
        else:
            aimer1.setEnabled(False)
            aimer1.setStyleSheet(
                "background-color: gray;"
                "color: black;"
                "font-size: 16pt;"
            )
    else:
        if conter.property("Index") == 2 and insign and insign != "数字账户/用户名":
            aimer2.setPixmap(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton).pixmap(24, 24))
            aimer2.setVisible(True)
        else:
            aimer2.setVisible(False)
        aimer1.setEnabled(False)
        aimer1.setStyleSheet(
            "background-color: gray;"
            "color: black;"
            "font-size: 16pt;"
        )


def passcheck(accountobj: QAbstractButton, passwordobj: QAbstractButton):
    """
    账户密码校验.
    注:账户和密码将会被提交到数据库进行核对和检验

    :data accountobj: 输入账户信息的控件.
    :type accountobj: QAbstractButton
    :data passwordobj: 输入密码的控件.
    :type passwordobj: QAbstractButton
    :return: 操作执行函数不做返回.
    :retype: None
    """
    with sqlManger() as man:
        if man.popinfo("accountinfo", accountobj.text()):
            if man.checkinfo("accountinfo", accountobj.text(), passwordobj.text()):
                print("登录成功")
            else:
                passwordobj.setText("")
                passwordobj.setFocus(True)
        else:
            accountobj.setText("")
            passwordobj.setText("")


def passshow(objself: QAction, aimobj: QAbstractButton):
    """
    通过链接图标来控制密码是否可见

    :data objself: 被作用的事件.
    :type objself: QAction
    :data aimobj: 随之变得的目标控件.
    :type aimobj: QAbstractButton
    :return: 操作执行函数不做返回.
    :retype: None
    """
    if aimobj.echoMode() == QLineEdit.Password:
        objself.setIcon(QIcon(r"D:\xst_project_202212\Python\privateProject\englishApp\素材库\明示密码.png"))
        aimobj.setEchoMode(QLineEdit.Normal)
    else:
        objself.setIcon(QIcon(r"D:\xst_project_202212\Python\privateProject\englishApp\素材库\隐藏密码.png"))
        aimobj.setEchoMode(QLineEdit.Password)


def tolalpos(preantsize: tuple, aimobjsize: tuple, centerpos: tuple = None, posdrift: tuple = (0, 0)):
    newcenter: tuple = (preantsize[0] / 2, preantsize[1] / 2)
    return (centerpos[0] - (aimobjsize[0] / 2) + posdrift[0], centerpos[1] - (aimobjsize[1] / 2) + posdrift[1]) \
        if centerpos else (newcenter[0] - (aimobjsize[0] / 2) + posdrift[0], newcenter[1] - (aimobjsize[1] / 2) + posdrift[1])

