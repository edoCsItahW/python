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
from scatteredFile.flagParser import flagParser, flag
from pypiOrigin.systemTools.systemTools import jsonOpen, instruct
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Literal, final
from os import path, PathLike, mkdir
from functools import cached_property, singledispatchmethod, cache
from re import findall
from sys import version


__version__ = "2.3.7"

License = """Copyright (c) 2024 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

token = "pypi-AgENdGVzdC5weXBpLm9yZwIkYzkwNzZjMTItOWU5OS00YWM4LWFiMWEtYWQwMzU1ZGZkYWVkAAIqWzMsIjRiNDBlZjEwLWRhMmQtNDVlMC1hYjM0LTY1MDI3YzBkYTJmMyJdAAAGILpCa7oU6b1m6k7hUMmp-dybDNN5R1bWdGghvxjjaQll"


@cache
def pyVersion(self) -> str | None:
    """
    python版本号.

    :return: python版本号
    :rtype: str
    """
    return findall(r"^\d\.\d{1,2}", version)[0]


@cache
def cmakeVersion(self) -> str | None:
    """
    CMake版本号.

    :return: CMake版本号
    :rtype: str
    """
    return findall(r"\d\.\d{1,2}", self.executor("cmake --version", output=False))[0]


class CMDError(Exception):
    """
    CMD错误类
    """
    def __init__(self, *args):
        self.args = args


class SpawnError(Exception):
    """
    子进程错误类
    """
    def __init__(self, *args):
        self.args = args


RESTORE, DEBUG, COLOR, AUTO, INCREASE, IGNORE, CREATE = flag("restore"), flag("debug"), flag("color"), flag("auto"), flag("increase"), flag("ignore"), flag("create")


def pyproject(projectName: str, _version: str, name: str, email: str, desc: str, moduleName: str, addFile: str):
    return f"""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{projectName}"
version = "{_version}"
authors = [
  {{ name="{name}", email="{email}" }},
]
description = "{desc}"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

{addFile}

[project.urls]
"Homepage" = "https://github.com/edoCsItahW/python/pypiOrigin/{moduleName}"
"Bug Tracker" = "https://github.com/edoCsItahW/python/issues"
"""


def CMakeLists(cmakeVision: str, projectName: str, _pyVersion: str, moduleName: str, addFile: str):
    return f"""cmake_policy(SET CMP0057 NEW)
cmake_minimum_required(VERSION {cmakeVision} FATAL_ERROR)
project({projectName})

find_package(Python {_pyVersion} COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module({moduleName} {addFile})
"""


def setup(fileName: str):
    #     return f"""from setuptools import setup, Extension
    # from Cython.Build import cythonize
    #
    # setup(
    #     ext_modules=cythonize("{}", language_level=3),
    # )"""
    return f"""from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("{fileName}")
)"""


class option(ABC):
    def __init__(self, filePath: str, _flag: int, *, eliminate: bool | str = None, suffix: Literal["py", "c", "cpp"] | list[str] = "py"):
        self.compliantArg(filePath, suffix=suffix)

        self._filePath = filePath
        self._suffix = suffix
        self._parser = flagParser(IGNORE, RESTORE, DEBUG, COLOR, AUTO, INCREASE, CREATE)
        self._parser.parse(_flag)
        self._splistList = path.splitext(self.fileName)
        self._eliminate = eliminate if eliminate else "文件名、目录名或卷标语法不正确。"

    @final
    @property
    def filePath(self) -> str | PathLike[str]:
        return self._filePath

    @final
    @cached_property
    def rootPath(self) -> str | PathLike[str]:
        return path.dirname(self.filePath)

    @final
    @cached_property
    def dirPath(self) -> str | PathLike[str]:
        dp = path.join(self.rootPath, self.moduleName)

        if self.flagDict["create"] and not path.exists(dp):
            mkdir(dp)

        return dp

    @final
    @cached_property
    def projectName(self) -> str:
        prj = path.join(self.dirPath, self.moduleName)

        if self.flagDict["create"] and not path.exists(prj):
            mkdir(prj)

        return prj

    @final
    @cached_property
    def jsonPath(self) -> str | PathLike[str]:
        return jsPath if path.exists(jsPath := path.join(self.rootPath, "args.json")) else None

    @final
    @property
    def argsDict(self):
        if self.jsonPath:
            with jsonOpen(self.jsonPath, "r") as file:
                return file.read()

    @final
    @cached_property
    def separator(self) -> str:
        return "/" if "/" in self.filePath else "\\"

    @final
    @cached_property
    def executor(self) -> instruct:
        return instruct(color=self.flagDict["color"], output=self.flagDict["debug"], ignore=self.flagDict["ignore"], eliminate=self._eliminate)

    @final
    @cached_property
    def fileName(self) -> str:
        return path.basename(self.filePath)

    @final
    @cached_property
    def moduleName(self) -> str:
        return self._splistList[0]

    @final
    @cached_property
    def fileSuffix(self) -> str:
        return self._splistList[1][1:]

    @final
    @property
    def flagDict(self) -> dict[str, bool]:
        return self._parser.resDict()

    @final
    @property
    def suffix(self) -> str | list[str]:
        return self._suffix.lower() if isinstance(self._suffix, str) else [s.lower() for s in self._suffix]

    @final
    @singledispatchmethod
    def _checkSuffix(self, suffix: str | list[str]) -> bool:
        """
        检查文件后缀是否合规.

        :param suffix: 文件后缀
        :type suffix: str | list[str]
        :return: 是否合规
        :rtype: bool
        :raise NotImplementedError: 类型不支持.
        """
        raise NotImplementedError(
            f"类型不支持: {type(suffix)}")

    @final
    @_checkSuffix.register(str)
    def _(self, suffix: str) -> bool:
        pass

    @final
    @_checkSuffix.register(list)
    def _(self, suffix: list[str]) -> bool:
        pass

    @staticmethod
    @final
    def compliantArg(_path: str | PathLike[str], *, suffix: Literal["py", "c", "cpp"] | list[str] = "py"):
        """
        路径合规性检查.

        :param _path: 文件路径
        :type _path: str | PathLike[str]
        :param suffix: 文件后缀
        :type suffix: str | list[str]
        :raise ValueError: 后缀不合规.
        """
        if not path.exists(_path): raise FileNotFoundError(
            f"没有找到文件'{_path}'")

        if not path.isabs(_path): raise ValueError(
            f"'{_path}'不是绝对路径,请输入绝对路径!")

        if isinstance(suffix, str):
            if not _path.endswith(f".{suffix}"): raise ValueError(
                f"'{path.basename(_path)}'不是`.{suffix.upper()}`后缀文件!")

        elif isinstance(suffix, list):
            if not any(_path.endswith(f".{s}") for s in suffix): raise ValueError(
                f"'{path.basename(_path)}'不是{suffix}中的后缀文件!")

    @abstractmethod
    def build(self):
        pass


def factory(_type: Literal['pyc', 'pyd', 'normal', 'cToPyd'], filePath: str | PathLike[str]) -> object:
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
