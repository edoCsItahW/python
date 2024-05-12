#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/11 下午9:25
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from scatteredFile.debuger import debuger
from scatteredFile.flagParser import flagParser
from flags import *
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Literal, final



class option(ABC):
    def __init__(self, filePath: str, _flag: int):


def factory(_type: Literal['pyc', 'pyd', 'normal', 'cToPyd']) -> object:
    match _type:
        case 'pyc':
            return pyc()
        case 'pyd':
            return pyd()
        case 'normal':
            return normal()
        case 'cToPyd':
            return cToPyd()
        case _:
            raise ValueError(
                f"未知的打包类型: {_type}")


class cToPyd:
    def __init__(self):
        pass


class normal:
    def __init__(self):
        pass


class pyc:
    def __init__(self):
        pass


class pyd:
    def __init__(self):
        pass


class upload:
    def __init__(self):
        pass


def argParser() -> Namespace:
    """
    包装了argparse的命令行参数解析器,用于解析命令行参数。

    :return: 一个包含命令行参数的对象。
    :rtype: Namespace
    """

    parser = ArgumentParser(prog="PYPI软件包上传工具", description="一个用于上传python软件包的工具.", epilog="**\nfileAbsolutePath, *, restore = True, debug = False, color = True, **kwargs\n**")
    parser.add_argument("file", help="你需要上传的python文件的绝对路径,获取需要转换为pyd文件的C文件绝对路径。")
    parser.add_argument("-T", "--type", default="pyd", choices=['pyc', 'pyd', 'normal', 'cToPyd'], help="打包的模式,pyc: 通过pyc文件打包, pyd: 通过pyd文件打包, normal: 通过py文件打包, cToPyd: 将C文件转换为pyd文件.(默认值: pyd)")
    parser.add_argument("-R", "--restore", default="True", choices=["True", "False"], help="当出现错误时是否要还原初始状态。(默认值: True)")
    parser.add_argument("-C", "--color", default="True", choices=["True", "False"], help="是否运行输出信息带有色彩。(默认值: True)")
    parser.add_argument("-D", "--debug", default="False", choices=["True", "False"], help="是否开启debug模式。(默认值: False)")
    parser.add_argument("--increase", default="True", choices=["True", "False"], help="是否启用版本自增(如果py文件所在文件夹中有args.json文件的情况下)(默认值: True)")
    parser.add_argument("-A", "--auto", default="True", choices=["True", "False"], help="是否在打包并生成dist文件夹后弹出cmd调试框。(默认值: True)")
    parser.add_argument("-I", "--ignore", default="True", choices=["True", "False"], help="是否将Error降级为warn以保证程序运行。(默认值: True)")
    parser.add_argument("-E", "--eliminate", default=(eDef := "文件名、目录名或卷标语法不正确。"), help="排除无关紧要的错误信息, 例如: '文件名、目录名或卷标语法不正确。'(默认值: '文件名、目录名或卷标语法不正确。')")
    parser.add_argument("-V", "--version", help="版本")
    return parser.parse_args()
