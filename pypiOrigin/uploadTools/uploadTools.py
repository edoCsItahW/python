#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/10 14:19
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from subprocess import Popen, PIPE
from functools import cached_property, partial, singledispatchmethod
from threading import Thread
from argparse import ArgumentParser
from warnings import warn
from inspect import currentframe
from typing import Literal, Callable, Any
from types import TracebackType
from json import dump, load
from time import sleep
from sys import version
from os import PathLike, path, listdir, mkdir, rename, remove
from re import findall
from datetime import datetime

__version__ = "1.1.3"

errorLog = {}

License = """Copyright (c) 2018 The Python Packaging Authority

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

pyproject = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{proName}"
version = "{version}"
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
"Homepage" = "https://github.com/edoCsItahW/python/{moduleName}"
"Bug Tracker" = "https://github.com/edoCsItahW/python/issues"
"""

CMakeLists = """cmake_policy(SET CMP0057 NEW)
cmake_minimum_required(VERSION {} FATAL_ERROR)
project({})

find_package(Python {} COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module({} {})
"""

setup = """from setuptools import setup, Extension  
from Cython.Build import cythonize  

setup(  
    ext_modules=cythonize("{}", language_level=3),  
)"""


class CMDError(Exception):
    def __init__(self, *args):
        self.args = args


class instruct:
    """
    命令行运行器

    使用方法::

        >>> ins = instruct(output=True, ignore=False, color=True)
        >>> ins("dir")
    """
    _instance = None

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, *, output: bool = True, ignore: bool = False,
                 color: bool | Literal["red", "yellow", "green", "blue"] = True, eliminate: str = None):
        """
        命令行初始器

        :keyword output: 是否运行输出结果.
        :type output: bool
        :keyword ignore: 是否将所有(原本将会抛出错误)错误(Error)降级为警告(Warning)以保证程序不中断.
        :type ignore: bool
        :keyword color: 档为布尔类型(bool)是决定输出是否带有ANSI色彩,为字符串(str)时决定输出什么颜色.
        :type color: bool
        :keyword eliminate: 是否排除某些会被误认为错误的无关紧要的警告,例如: '文件名、目录名或卷标语法不正确。'
        """
        self._flagOutput = output
        self._flagIgnore = ignore
        self._flagColor = color
        self._eleiminate = eliminate

    def __call__(self, instruction: str, *, cwd: PathLike | str = None, output: bool = None,
                 encoding: Literal["gbk", "utf-8"] = "gbk", note: str = ""):
        """
        执行器

        :param instruction: 指令
        :type instruction: str
        :keyword cwd: 设定当前路径或执行路径
        :type cwd: str
        :keyword allowOUTPUT: 是否允许打印结果
        :type allowOUTPUT: bool
        :return: cmd执行结果
        :rtype: str
        """

        correct, error = self._execute(instruction, cwd=cwd, encoding=encoding)

        tempFunc = lambda x: x.replace("\n", "").replace("\r", "").replace(" ", "")

        if self._flagIgnore:

            if flag := (self._flagOutput if output is None else output):
                outputInfo(f"{cwd if cwd else 'cmd'}>{instruction}", color="green" if self._flagColor else False,
                           flag=flag)

                print(correct) if correct else None

            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):
                warn(
                    error + note, SyntaxWarning)

            return correct

        else:

            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):

                raise CMDError(error)

            elif tempFunc(error) == tempFunc(self._eleiminate):

                warn(
                    f"你忽略了错误'{self._eleiminate}',而且没有将错误降级为警告,这导致一个错误被忽略了,带来的后果是返回了None而不是你期望的结果!")

    @staticmethod
    def _execute(instruction: str, *, cwd: PathLike | str = None, encoding: Literal["gbk", "utf-8"] = "gbk") -> tuple[
        str, str]:
        """
        执行器内核

        :param instruction: 指令
        :type instruction: str
        :param cwd: 执行环境路径
        :type cwd: PathLike | str
        :param encoding: 编码.(防止命令行输出乱码)
        :type encoding: str
        :return: 一个字典,键'C'对应正确信息,键'E'对应错误消息
        :rtype: dict
        """
        try:

            result = Popen(instruction, shell=True, stdout=PIPE, stderr=PIPE, cwd=cwd)

            return tuple(getattr(result, i).read().decode(encoding, errors='ignore') for i in ["stdout", "stderr"])

        except Exception as err:

            err.add_note("命令行执行器内核运行错误")

            raise err


class jsonFile:
    def __init__(self, jsonDict: dict):
        self._json = jsonDict

        if not isinstance(self._json, dict):
            raise TypeError(f"参数`jsonDict`必须为字典(dict)类型,你的输入类型: '{type(self._json)}'")

    @property
    def jsonData(self):
        return self._json

    @jsonData.setter
    def jsonData(self, value: dict):

        if not isinstance(self._json, dict):
            raise TypeError(f"参数`jsonDict`必须为字典(dict)类型,你的输入类型: '{type(value)}'")

    def _pairParser(self, key: Any, value: Any):
        if key in self.jsonData:

            if isinstance(self.jsonData[key], list):

                self.jsonData[key].append(value)

            else:

                self.jsonData[key] = value

        else:

            self.jsonData.update([(key, value)])

    def update(self, __m: list[tuple[Any, Any]]):

        if not isinstance(__m, list) or any([not isinstance(i, tuple) for i in __m]):
            raise ValueError(
                f"传入的位置参数`__m`必须形如'[('key': 'value')]',你的输入'{__m}'")

        for t in __m:
            self._pairParser(*t)

    def read(self):
        return self.jsonData

    def write(self, __d: dict = None):

        if __d is None:

            __d = self.jsonData

        else:

            self.jsonData = __d


class jsonOpen:
    def __init__(self, file: str | bytes | PathLike[str] | PathLike[bytes], mode: Literal["r+", "+r", "w+", "+w", "a+", "+a", "w", "a", "r"]):  # type: ignore
        """
        与open相同

        >>> with jsonOpen(file, "r") as file:
        >>>     file.read()  # type: dict

        :param file:
        :type file:
        :param mode:
        :type mode:
        """
        self._filePath = path.abspath(file)
        self._mode = mode
        self._jsonfile: jsonFile = None

        if not path.exists(self._filePath): raise FileNotFoundError(f"找不到文件: '{self._filePath}'")

    @property
    def _file(self):
        return self._jsonfile

    @_file.setter
    def _file(self, value: Any):

        self._jsonfile = value

    def __enter__(self):

        with open(self._filePath, "r") as File:
            self._file = jsonFile(load(File))

            return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):

        if any([exc_type, exc_val, exc_tb]):
            exc_tb: TracebackType
            warn(f"一个错误被捕获了: {exc_type}({exc_val}), line {exc_tb.tb_lineno}")

        if self._mode != "r":
            with open(self._filePath, self._mode) as file:
                dump(self._file.jsonData, file)


class SpawnError(Exception):
    def __init__(self, *args):
        self.args = args


def outputInfo(info: str, *, color: Literal["red", "green", "blue", "yellow"] | str | bool = "green", flag: bool = True):
    if not flag: return

    colorDict = {
        "red":    '\033[41m',
        "green":  '\033[42m',
        "yellow": '\033[43m',
        "blue":   '\033[44m',
    }

    if isinstance(color, str):
        print(f"{colorDict[color] if color in colorDict else color}{info}\033[0m")

    elif isinstance(color, bool):
        print(f"{colorDict['green']}{info}\033[0m" if color else info)

    else:
        raise TypeError(
            f"关键字参数`color`可以布尔值(bool), ANSI转义符(str)或颜色键,但你的输入'{type(color)}'")


def strToBool(text: str, *, default: bool) -> bool:
    if text.lower() == "true":
        return True
    elif text.lower() == "false":
        return False
    else:
        return default


class pathTools:
    @staticmethod
    def isFileExist(_path: str | PathLike, **kwargs) -> bool:
        """
        :param _path:
        :type _path:
        :keyword kwargs: {note: 错误原因注解, willDo: [warn, error, stop] 报错方式, fromError: ..., group: 组}
        :type kwargs:
        :return:
        :rtype:
        """
        if path.exists(_path):
            return True

        else:
            errorHandle.raiseError(FileNotFoundError, f"没有检测到文件'{_path}'!", **kwargs)

            return False

    @staticmethod
    def createIfNotExist(_path: str | PathLike[str]):
        if not path.exists(_path): mkdir(_path)


class argSet:
    def __init__(self, fileAbsPath: str | PathLike[str], *, restore: bool = True, debug: bool = False, color: bool = True, **kwargs):
        """
        /rootPath
            /dirPath = rootPath(old)
                /projectPath = dirPath(old)
            pyFile.py

        :param fileAbsPath: 文件绝对路径。
        :type fileAbsPath: str
        :keyword restore: 当出现错误时是否要还原初始状态。
        :type restore: bool
        :keyword debug: 是否开启Debug模式。
        :type debug: bool
        :keyword color: 是否运行输出信息带有色彩。
        :type color: bool
        :keyword increase: 是否运行上传完后自动向args.json中更新版本, major: 主版本号([0].0.0), minor: 副版本号(0.[0].0), patch: 补丁号(0.0.[0]), 如为False则不自增.
        :type increase: str
        :keyword kwargs: 其它关键字参数,包括: ignore, eleiminate
        :type kwargs: ...
        :raise ValueError: 如果传入的文件路径不是绝对路径。
        """
        self.compliantArg(fileAbsPath, suffix="py")

        self._filePath = fileAbsPath
        self._newPath = None

        self._color = color
        self._flagRestore = restore
        self._flagDebug = debug
        self._executor = instruct(color=color, output=debug, **kwargs)

    @property
    def filePath(self):
        return self._filePath

    @cached_property
    def rootPath(self):
        return path.dirname(self.filePath)

    @cached_property
    def fileName(self):
        return path.basename(self.filePath)

    @cached_property
    def moduleName(self):
        return path.splitext(self.fileName)[0]

    @cached_property
    def dirPath(self):
        if not path.exists(root := path.join(self.rootPath, self.moduleName)):
            mkdir(root)

        return root

    @cached_property
    def projectPath(self):

        if not path.exists(prj := path.join(self.dirPath, self.moduleName)):
            mkdir(prj)

        return prj

    @property
    def newPath(self): return self._newPath

    @newPath.setter
    def newPath(self, value): self._newPath = value

    @cached_property
    def jsonPath(self):
        return jsPath if path.exists(jsPath := path.join(self.rootPath, "args.json")) else None

    @property
    def argsDict(self):
        if self.jsonPath:
            with jsonOpen(self.jsonPath, "r") as file:
                return file.read()

    @cached_property
    def separator(self):
        return "/" if "/" in self.filePath else "\\"

    @property
    def executor(self):
        return self._executor

    @property
    def color(self):
        return self._color

    @property
    def flagRestore(self):
        return self._flagRestore

    @property
    def flagDebug(self):
        return self._flagDebug

    @cached_property
    def pyVersion(self):
        return findall(r"^\d\.\d{1,2}", version)[0]

    @cached_property
    def cmakeVersion(self):
        return findall(r"\d\.\d{1,2}", self.executor("cmake --version", output=False))[0]

    @staticmethod
    def compliantArg(_path: str | PathLike[str], *, suffix: str = Literal["py", "c"]):
        if not path.exists(_path): raise FileNotFoundError(
            f"没有找到文件'{_path}'")

        if not path.isabs(_path): raise ValueError(
            f"'{_path}'不是绝对路径,请输入绝对路径!")

        if not _path.endswith(f".{suffix}"): raise ValueError(
            f"'{path.basename(_path)}'不是`.{suffix.upper()}`后缀文件!")


class errorHandle:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, args: argSet):

        self._args: argSet = args

    @property
    def args(self):
        return self._args

    @staticmethod
    def _formatErrorGroup(*, _lastKey: list = None, _result: list = None):
        if _lastKey is not None:
            if len(_lastKey):
                firstKey = _lastKey[0]

                _result = [firstKey, errorLog[firstKey] + [ExceptionGroup(*_result)]]

                return errorHandle._formatErrorGroup(_lastKey=_lastKey[1:], _result=_result)

            else:
                return ExceptionGroup(*_result)

        else:
            firstKey, _lastKey = (keyList := list(errorLog.keys()))[0], keyList[1:]

            _result = [firstKey, errorLog[firstKey]]

            return errorHandle._formatErrorGroup(_lastKey=_lastKey, _result=_result)

    @staticmethod
    def logError(error: Exception, *, group: str = "其它") -> None:
        """
        错误记录.

        :param error: 错误
        :type error: Exception
        :param group: 分至组
        :type group: str
        :return: 操作执行函数不做返回
        :rtype: None
        """
        if group not in errorLog: errorLog.update([(group, [])])

        errorLog[group].append(error)

    @classmethod
    def raiseErrorGroup(cls):
        if errorLog:
            raise cls._formatErrorGroup()

    @staticmethod
    def raiseError(errorType: type[Exception], info: str = '', *, note: str = "",
                   willDo: Literal["warn", "error", "stop", "log"] = "error", fromError: Exception = None,
                   group: str = "其它"):
        def rerr(err, fe):
            if fe:
                raise err from fe

            else:
                raise err

        match willDo:
            case "warn":
                errStr, emptyStr = "Error", ""
                warn(f"{info}{f',NOTE: {note.replace(errStr, emptyStr)}' if note else ''}")

            case "error" | "log":
                error = errorType(info)

                if note: error.add_note(note)

                if willDo == "log":
                    try:
                        rerr(error, fromError)

                    except Exception as e:
                        errorHandle.logError(e, group=group)

                else:
                    rerr(error, fromError)

            case "stop":
                errorHandle.raiseErrorGroup()

                exit("不可忽略的错误导致强制退出!")

            case _:
                raise ValueError(  # 入参错误
                    f"关键字参数'willDo'必须是['warn', 'error', 'stop', 'log']中所有,而你的输入'{willDo}'")

    @staticmethod
    def formatFuncInfo(func: Callable, line: int):
        return f"from {func.__name__} in {line}"

    def executeWithTry(self, instruction: str, *, cwd: str | PathLike = None, note: str = "", group: str = "其它", describe: str = None, color: str = "yellow"):
        try:
            self.args.executor(instruction, cwd=cwd, note=note)

            if describe: outputInfo(describe, color=color, flag=self.args.flagDebug)

        except Exception as err:
            err.add_note(note.replace("Warning", ""))

            errorHandle.logError(err, group=group)


class actionSet:
    def __init__(self, args: argSet):
        self._args = args
        self._errorHandle = errorHandle(self.args)

        self._versionList = None

    @property
    def args(self):
        return self._args

    @property
    def eh(self):
        return self._errorHandle

    @property
    def vsList(self): return self._versionList

    @vsList.setter
    def vsList(self, value): self._versionList = value

    def _increase(self, pos: int | Literal[0, 1, 2] = 2):
        with jsonOpen(self.args.jsonPath, "w") as file:
            contentDict = file.read()

            self.vsList = versionList = list(map(int, contentDict["version"].split(".")))

            versionList[pos] += 1

            contentDict["version"] = ".".join(map(str, self.vsList))

            if "uploadLog" in contentDict:

                contentDict['uploadLog'].append({datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"): {contentDict["version"]: True}})

            else:
                contentDict.update([("uploadLog", [{datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"): {contentDict["version"]: True}}])])

            file.write(contentDict)

    @singledispatchmethod
    def _jsonIncrease(self, increase: bool | Literal["major", "minor", "patch"] = "patch"):
        raise TypeError(
            f"位置参数'increase'必须为布尔(bool)或['major', 'minor', 'patch']中的字符串(str)类型,而你的输入'{increase}'!")

    @_jsonIncrease.register(bool)
    def _(self, increase):
        if increase:
            self._increase()

    @_jsonIncrease.register(str)
    def _(self, increase):
        # match increase:
        #     case "major":
        #         self._increase(0)
        #     case "minor":
        #         self._increase(1)
        #     case "patch":
        #         self._increase(2)
        #     case _:
        #         raise ValueError(
        #             f"位置参数'increase'必须为['major', 'minor', 'patch']中的字符串,而你的输入'{increase}'!")
        _ = {"major": 0, "minor": 1, "patch": 2}
        try:
            self._increase(_[increase])

        except KeyError:
            warn(
                f"位置参数'increase'必须为['major', 'minor', 'patch']中的字符串,而你的输入'{increase}'!")

        finally:
            self._increase(2)

    def versionBack(self):
        with jsonOpen(self.args.jsonPath, "w") as file:
            argsDict = file.read()

            argsDict["version"] = ".".join(map(str, self.vsList))

            if "uploadLog" in argsDict:

                (vDict := (timeDict := argsDict["uploadLog"][-1])[list(timeDict.keys())[0]])[list(vDict.keys())[0]] = False

            file.write(argsDict)

    def _kewargs(self, file: str):
        self._jsonIncrease(self.args.argsDict["increase"])

        text = f"""[tool.poetry.scripts]
        files = ["{file}"]"""

        return {
            "proName":    _ if (_ := self.args.argsDict["proName"]) else self.args.moduleName,
            "version":    _ if (_ := self.args.argsDict["version"]) else '',
            "name":       _ if (_ := self.args.argsDict["name"]) else '',
            "email":      _ if (_ := self.args.argsDict["email"]) else '',
            "desc":       _ if (_ := self.args.argsDict["desc"]) else '',
            "addFile":       text if file else '',
            "moduleName": _ if (_ := self.args.argsDict["proName"]) else self.args.moduleName,
        }

    @property
    def _warpCmake(self):
        return partial(CMakeLists.format, self.args.cmakeVersion, self.args.moduleName, self.args.pyVersion,
                       self.args.moduleName)

    def spawnPyi(self):
        """生成pyi文件"""
        self.eh.executeWithTry(ins1 := f"stubgen {self.args.fileName}", cwd=self.args.projectPath,
                               note=f"[ErrorWarning]生成pyi文件出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}",
                               group="生成pyi", describe="spawnPyi -> 生成pyi文件.")

        pathTools.isFileExist(cacheFile := path.join(self.args.projectPath, ".mypy_cache"),
                              note=f"该文件夹由spawnPyi的'{ins1}'指令生成", willDo="warn",
                              fromError=SpawnError("生成pyi文件失败?"), group="生成pyi")

        self.eh.executeWithTry(ins2 := f"rd /s /q {cacheFile}", cwd=self.args.projectPath,
                               describe="spawnPyi -> 移除缓存文件",
                               group="生成pyi",
                               note=f"[ErrorWarning]移除pyi缓存文件夹出现问题: '{ins2}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}")

        self.eh.executeWithTry(
            ins3 := f"move {path.join(self.args.projectPath, 'out', self.args.moduleName, f'{self.args.moduleName}.pyi')} {self.args.projectPath}",
            note=f"[ErrorWarning]移动pyi文件出现问题: '{ins3}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}",
            group="生成pyi", describe="spawnPyi -> 移动pyi文件")

        pathTools.isFileExist(ins4 := path.join(self.args.projectPath, "out"),
                              note=f"该文件由spawnPyi的'{ins4}'指令生成",
                              willDo="log", fromError=SpawnError("生成pyi文件失败?"), group="生成pyi")

        self.eh.executeWithTry(ins5 := "rd /s /q out", cwd=self.args.projectPath,
                               note=f"[ErrorWarning]删除out文件夹出现问题: '{ins5}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}",
                               group="生成pyi", describe="spawnPyi -> 删除out文件夹")

        return path.join(self.args.projectPath, f"{self.args.moduleName}.pyi")

    def spawnPyc(self):
        self.eh.executeWithTry(ins1 := f"python -m py_compile {self.args.fileName}", cwd=self.args.projectPath,
                               note=f"[ErrorWarning]pyc文件编译出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnPyc, currentframe().f_lineno)}",
                               group="生成pyc", describe="spawnPyc -> 生成pyc文件")

        if pathTools.isFileExist(pycache := path.join(self.args.projectPath, "__pycache__"),
                                 note=f"该文件夹由spawnPyc的'{ins1}'指令生成", willDo="log",
                                 fromError=SpawnError("生成pyc文件失败?"), group="生成pyc"):

            if pyc := [i for i in listdir(pycache) if i.endswith(".pyc")]:

                pyc = pyc[0]

                self.eh.executeWithTry(ins2 := f"move {path.join(pycache, pyc)} {self.args.projectPath}",
                                       note=f"[ErrorWarning]移动pyc文件出现问题: '{ins2}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}",
                                       group="生成pyc", describe="spawnPyc -> 移动pyc文件")

                self.eh.executeWithTry(in3 := f"rd /s /q {pycache}",
                                       note=f"[ErrorWarning]删除缓存文件出现问题: '{in3}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}",
                                       group="生成pyc", describe="spawnPyc -> 移除缓存文件")

                self.eh.executeWithTry(
                    ins4 := f"ren {pyc} {(pycWithOut := '.'.join([(pycList := pyc.split('.'))[0], pycList[2]]))}",
                    cwd=self.args.projectPath,
                    note=f"[ErrorWarning]重命名pyc文件出现问题: '{ins4}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}",
                    group="生成pyc", describe="spawnPyc -> 重命名pyc文件")

                return path.join(self.args.projectPath, pycWithOut)

            else:
                errorHandle.raiseError(FileNotFoundError, f"列表: {pyc}中没有期望的文件.",
                                       note=f"该文件由'{ins1}'指令生成", willDo="log", group="生成pyc",
                                       fromError=SpawnError("生成pyc文件错误?"))

    def spawnHtml(self):
        self.eh.executeWithTry(ins1 := f"pdoc -d=markdown --output {self.args.dirPath} {self.args.filePath}", note=f"[ErrorWarning]生成html文档出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnHtml, currentframe().f_lineno)}", group="生成html", describe="spawnHtml -> 生成html文档")

        pathTools.isFileExist(html := path.join(self.args.dirPath, f"{self.args.moduleName}.html"), note=f"该文件由: '{ins1}'指令生成 {errorHandle.formatFuncInfo(self.spawnHtml, currentframe().f_lineno)}", willDo="log", fromError=SpawnError("生成html文档错误?"), group="生成html")

        for name in ['index.html', 'search.js']:
            self.eh.executeWithTry(ins2 := f"{'del' if '.' in name else 'rd /s /q'} {path.join(self.args.dirPath, name)}", note=f"[ErrorWarning]删除文件出现问题: '{ins2}' {errorHandle.formatFuncInfo(self.spawnHtml, currentframe().f_lineno)}", group="生成html", describe="spawnHtml -> 移除剩余文件")

        return path1 if path.exists(path1 := path.join(self.args.dirPath, f"{self.args.moduleName}.html")) else path.join(self.args.dirPath, self.args.moduleName, f"{self.args.moduleName}.html")

    def spawnREADME(self):
        htmlPath = self.spawnHtml()

        self.eh.executeWithTry(
            ins1 := f"pandoc -f html -t markdown {htmlPath} -o {(readmePath := path.join(self.args.dirPath, 'README.md'))}",
            note=f"[ErrorWarning]转换html为markdown出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnREADME, currentframe().f_lineno)}",
            group="生成README", describe="spawnREADME -> 转换html为markdown")

        self.eh.executeWithTry(ins2 := f"del {htmlPath}",
                               note=f"[ErrorWarning]删除html文件出现问题: '{htmlPath}' {errorHandle.formatFuncInfo(self.spawnREADME, currentframe().f_lineno)}",
                               group="生成README", describe="spawnREADME -> 删除html文件")

        return readmePath

    def spawnLicense(self):
        try:
            with open(path.join(self.args.dirPath, "LICENSE.txt"), "w", encoding="utf-8") as file:
                file.write(License)

        except Exception as e:
            e.add_note(f"生成LICENSE.txt失败 {errorHandle.formatFuncInfo(self.spawnLicense, currentframe().f_lineno)}")

            errorHandle.logError(e, group="生成LICENSE")

        else:
            outputInfo("spawnLicense -> 生成License.txt")

    def spawnManifest(self, suffix: Literal["pyd", "pyc"]):
        try:
            with open(path.join(self.args.dirPath, "MANIFEST.in"), "w", encoding="utf-8") as file:
                file.write(
                    f"recursive-include {self.args.moduleName} *.pyi\n"
                    f"recursive-include {self.args.moduleName} *.{suffix}"
                )

        except Exception as e:
            e.add_note(f"生成MANIFEST.in失败 {errorHandle.formatFuncInfo(self.spawnManifest, currentframe().f_lineno)}")

            errorHandle.logError(e, group="生成MANIFEST")

        else:
            outputInfo("spawnManifest -> 生成MANIFEST.in")

    def spawnInit(self):
        try:
            with open(path.join(self.args.projectPath, "__init__.py"), "w", encoding="utf-8") as file:
                file.write(f"from .{self.args.moduleName} import *\n")

        except Exception as e:
            e.add_note(f"生成__init__.py失败 {errorHandle.formatFuncInfo(self.spawnInit, currentframe().f_lineno)}")

            errorHandle.logError(e, group="生成__init__.py")

        else:
            outputInfo("spawnInit -> 生成__init__.py")

    def spawnPyproject(self, filePath: str | PathLike[str] = None):
        try:
            with open(path.join(self.args.dirPath, "pyproject.toml"), "w", encoding="utf-8") as file:
                file.write(pyproject.format(**self._kewargs(filePath.replace(self.args.separator, self.args.separator * 2) if filePath else filePath)))

        except Exception as e:
            e.add_note(f"生成pyproject失败 {errorHandle.formatFuncInfo(self.spawnPyproject, currentframe().f_lineno)}")

            errorHandle.logError(e, group="生成pyproject")

        else:
            outputInfo("spawnPyproject -> 生成pyproject.toml")

    def spawnSetup(self):
        if not path.exists(setupPath := path.join(self.args.projectPath, "setup.py")):
            with open(setupPath, "w", encoding="utf-8") as file:
                file.write(setup.format(self.args.fileName))

    def spawnC(self):
        self.eh.executeWithTry(ins1 := "python setup.py build_ext --inplace", cwd=self.args.projectPath, note=f"[ErrorWarning]C文件生成出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnPyc, currentframe().f_lineno)}", group="生成C", describe="spawnC -> 生成C文件")

        return path.join(self.args.projectPath, f"{self.args.moduleName}.c")

    def spawnPyd(self):
        self.eh.executeWithTry(ins1 := r"cmake -B build -S . -Dpybind11_DIR=F:\ProgramFiles\Anaconda3\Lib\site-packages\pybind11\share\cmake\pybind11 -Wno-dev", cwd=self.args.projectPath, note=f"[ErrorWarning]cmake build出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnPyc, currentframe().f_lineno)}", group="生成pyd", describe="spawnPyd -> cmake构建")

        tempFunc = lambda x: path.join(self.args.projectPath, x)

        rename(cPath := tempFunc(f"{self.args.moduleName}.c"), tempFunc(newName := f"{self.args.moduleName}.cpp"))

        self.CMakeLists(newName)

        self.eh.executeWithTry(ins2 := "cmake --build build --config Release", cwd=self.args.projectPath, note=f"[ErrorWarning]cmake生成pyd出现问题: '{ins2}' {errorHandle.formatFuncInfo(self.spawnPyc, currentframe().f_lineno)}", group="生成pyd", describe="spawnPyd -> 生成pyd")

        rename(path.join(self.args.projectPath, "build", "Release", f"{self.args.moduleName}.cp311-win_amd64.pyd"), finPath := path.join(self.args.projectPath, f"{self.args.moduleName}.pyd"))

        self.eh.executeWithTry(ins3 := f"rd /s /q build", cwd=self.args.projectPath, note=f"[ErrorWarning]移除cmake build文件夹出现问题: '{ins3}' {errorHandle.formatFuncInfo(self.spawnPyc, currentframe().f_lineno)}", group="生成pyd", describe="spawnPyd -> 移除残留build文件夹")

        rename(path.join(self.args.projectPath, newName), cPath)

        remove(path.join(self.args.projectPath, "CMakeLists.txt"))

        return finPath

    def CMakeLists(self, fileName: str):
        with open(path.join(self.args.projectPath, "CMakeLists.txt"), "w", encoding="utf-8") as file:
            file.write(self._warpCmake(fileName))

    def middleDo(self, *, copy: bool = False):
        self.args.newPath = path.join(self.args.projectPath, self.args.fileName)

        try:
            if copy:
                self.eh.executeWithTry(ins1 := f"copy /Y {self.args.fileName} {self.args.newPath}", cwd=self.args.rootPath, note=f"[ErrorWarning]复制py源文件出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.middleDo, currentframe().f_lineno)}", group="初始化", describe="middleDo -> 复制py文件")

            else:
                rename(self.args.filePath, self.args.newPath)

        except Exception as e:
            e.add_note(
                f"移动'{self.args.filePath}'至'{self.args.newPath}'失败 {errorHandle.formatFuncInfo(self.middleDo, currentframe().f_lineno)}")

            errorHandle.logError(e, group="构建")

        else:
            outputInfo(f"build -> 移动{self.args.fileName}")

    @staticmethod
    def checkRequestList(requestList: list):
        for p in requestList:
            if not path.exists(p): raise FileNotFoundError(
                f"缺少预设需求文件结构中的'{p}'文件!")


class upload:
    def __init__(self, fileAbsPath: str | PathLike[str], *, restore: bool = True, debug: bool = False, color: bool = True, **kwargs):
        """
        --restore=bool       当出现错误时是否要还原初始状态。
        --debug=bool         是否开启Debug模式。
        --color=bool         是否运行输出信息带有色彩。
        --ignore=bool        是否将Error降级为warn以保证程序运行。
        --eliminate          排除无关紧要的错误信息, 例如: '文件名、目录名或卷标语法不正确。'

        :param fileAbsPath: 文件绝对路径。
        :type fileAbsPath: str
        :keyword restore: 当出现错误时是否要还原初始状态。
        :type restore: bool
        :keyword debug: 是否开启Debug模式。
        :type debug: bool
        :keyword color: 是否运行输出信息带有色彩。
        :type color: bool
        :keyword kwargs: 其它关键字参数,包括: ignore, eleiminate
        :type kwargs: ...
        :raise ValueError: 如果传入的文件路径不是绝对路径。
        """
        self._args = argSet(fileAbsPath, restore=restore, debug=debug, color=color, **kwargs)
        self._actionSet = actionSet(self._args)

        self._common = [
            path.join(self.args.dirPath, "MANIFEST.in"),
            path.join(self.args.dirPath, "README.md"),
            path.join(self.args.dirPath, "pyproject.toml"),
            path.join(self.args.dirPath, "LICENSE.txt"),
            path.join(self.args.projectPath, "__init__.py"),
        ]

        self._pyd = [
            path.join(self.args.projectPath, f"{self.args.moduleName}.pyd"),
            path.join(self.args.projectPath, f"{self.args.moduleName}.pyi")
        ] + self._common

        self._pyc = [
            path.join(self.args.projectPath, f"{self.args.moduleName}.pyc"),
            path.join(self.args.projectPath, f"{self.args.moduleName}.pyi")
        ] + self._common

        self._normal = [
            path.join(self.args.projectPath, f"{self.args.moduleName}.py"),
        ] + self._common

        self.requestDict = {
            self.pyd: self._pyd,
            self.pyc: self._pyc,
            self.normal: self._normal
        }

    @property
    def args(self): return self._args

    @property
    def actionSet(self): return self._actionSet

    def tryDec(self, func: Callable, *, copy: bool = False):
        try:
            func()

            # self.actionSet.checkRequestList(self.requestDict[func])

        except Exception as e:
            None if copy else rename(self.args.newPath, self.args.filePath)

            if self.args.flagRestore:
                self.actionSet.eh.executeWithTry(ins2 := f"rd /s /q {self.args.dirPath}", note=f"[ErrorWarning]还原过程清空出现问题: '{ins2}' {errorHandle.formatFuncInfo(self._commonPart, currentframe().f_lineno)}", group="还原", describe="tryDec -> 还原文件")

                errorHandle.raiseError(e.__class__, e.args[0], note=f"[ErrorWarning]tryDec执行函数'{func.__name__}'出现问题", willDo="log", group="构建")

                if self.actionSet.vsList:
                    self.actionSet.versionBack()

        else:
            None if copy else rename(self.args.newPath, self.args.filePath)

        finally:
            if errorLog:
                errorHandle.raiseErrorGroup()

    def _successDo(self):
        if not self.args.jsonPath:
            if input("现在你可以编辑pyproject.toml,编辑完成后输入ok以继续:").lower() == "ok":
                pass

        self.args.executor("python -m build", cwd=self.args.dirPath)

        print(f"现在你可以运行`cd {self.args.dirPath}`并输入`python -m twine upload --repository testpypi dist/*`以开始上传.\n#您的token:'pypi-AgENdGVzdC5weXBpLm9yZwIkYzkwNzZjMTItOWU5OS00YWM4LWFiMWEtYWQwMzU1ZGZkYWVkAAIqWzMsIjRiNDBlZjEwLWRhMmQtNDVlMC1hYjM0LTY1MDI3YzBkYTJmMyJdAAAGILpCa7oU6b1m6k7hUMmp-dybDNN5R1bWdGghvxjjaQll'")

    def _commonPart(self):
        self.actionSet.middleDo()

        self.actionSet.spawnInit()

        self.actionSet.spawnPyi()

        self.actionSet.spawnREADME()

        self.actionSet.spawnLicense()

    def pyc(self):
        """

        """
        self._commonPart()

        pathTools.isFileExist(pyc := self.actionSet.spawnPyc(), note=f"该文件由spawnPyc生成 {errorHandle.formatFuncInfo(self._commonPart, currentframe().f_lineno)}", willDo="log", fromError=SpawnError("生成pyc文件错误!"), group="生成pyc")

        self.actionSet.spawnPyproject(pyc)

        self.actionSet.spawnManifest("pyc")

        remove(path.join(self.args.projectPath, f"{self.args.moduleName}.html"))

    def pyd(self):
        self._commonPart()

        self.actionSet.spawnManifest("pyd")

        self.actionSet.spawnSetup()

        pathTools.isFileExist(self.actionSet.spawnC(), note=f"该文件由: spawnC生成", willDo="log", fromError=SpawnError("生成C文件错误?"), group="生成C")

        self.actionSet.CMakeLists(f"{self.args.moduleName}.c")

        self.actionSet.spawnPyproject(self.actionSet.spawnPyd())

        for p in map(lambda x: path.join(self.args.projectPath, x), [f"{self.args.moduleName}.{s}" for s in ('c', 'html')] + ["setup.py"]):
            remove(p)

    def normal(self):
        self.actionSet.middleDo(copy=True)

        self.actionSet.spawnLicense()

        self.actionSet.spawnREADME()

        self.actionSet.spawnInit()

        self.actionSet.spawnPyproject()

    def build(self, Type: Literal["pyc", "pyd", "normal"] = "pyd"):
        match Type:
            case "pyc":
                self.tryDec(self.pyc)

            case "pyd":
                self.tryDec(self.pyd)

            case "normal":
                self.tryDec(self.normal, copy=True)

            case _: raise ValueError(
                f"位置参数'Type'必须是['pyc', 'pyd', 'normal']中所有,而你的输入'{Type}'")

        self._successDo()


parser = ArgumentParser(prog="PYPI软件包上传工具", description="一个用于上传python软件包的工具.", epilog="**\nfileAbsolutePath, *, restore = True, debug = False, color = True, **kwargs\n**")
parser.add_argument("file", help="你需要上传的python文件的绝对路径。")
parser.add_argument("-T", "--type", default="pyd", choices=['pyc', 'pyd', 'normal'], help="打包的模式,pyc: 通过pyc文件打包, pyd: 通过pyd文件打包, normal: 通过py文件打包.(默认值: pyd)")
parser.add_argument("-R", "--restore", default="True", choices=["True", "False"], help="当出现错误时是否要还原初始状态。(默认值: True)")
parser.add_argument("-C", "--color", default="True", choices=["True", "False"], help="是否运行输出信息带有色彩。(默认值: True)")
parser.add_argument("-D", "--debug", default="False", choices=["True", "False"], help="是否开启debug模式。(默认值: False)")
parser.add_argument("-I", "--ignore", default="True", choices=["True", "False"], help="是否将Error降级为warn以保证程序运行。(默认值: True)")
parser.add_argument("-E", "--eliminate", default=(eDef := "文件名、目录名或卷标语法不正确。"), help="排除无关紧要的错误信息, 例如: '文件名、目录名或卷标语法不正确。'(默认值: '文件名、目录名或卷标语法不正确。')")
parser.add_argument("-V", "--version", help="版本")
args = parser.parse_args()


if __name__ == '__main__':
    # pyinstaller -F uploadTools.py -n upload -i upload_1.ico

    # ins = upload(r"D:\xst_project_202212\codeSet\Python\pypiOrigin\systemTools\systemTools.py", debug=True, ignore=True, eliminate="文件名、目录名或卷标语法不正确。")
    # ins.build("pyc")

    if args.version:
        print(__version__)
    else:
        ins = upload(args.file, debug=strToBool(args.debug, default=False), ignore=strToBool(args.ignore, default=True), eliminate=args.eliminate, color=strToBool(args.color, default=True), restore=strToBool(args.restore, default=True))
        ins.build(args.type)
