#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/3/24 14:30
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from subprocess import Popen, PIPE
from functools import cached_property, partial
from threading import Thread
from argparse import ArgumentParser
from warnings import warn
from inspect import currentframe
from typing import Literal, Callable
from time import sleep
from sys import version
from os import PathLike, path, listdir, mkdir, rename, remove
from re import findall

__vision__ = "0.1.3"

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
name = ""
version = ""
authors = [
  {{ name="Xiao Songtao", email="2257699870@qq.com" }},
]
description = ""
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[tool.poetry.scripts]
files = ["{}"]

[project.urls]
"Homepage" = "https://github.com/edoCsItahW/python"
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

extensions = [  
    Extension("{}", ["{}"])  
]  

setup(  
    name="{}",  
    version="",  
    description="",  
    ext_modules=cythonize(extensions),  
)"""


def outputInfo(info: str, *, color: Literal["red", "green", "blue", "yellow"] | str | bool = "green", flag: bool = True):
    if not flag: return

    colorDict = {
        "red": '\033[41m',
        "green": '\033[42m',
        "yellow": '\033[43m',
        "blue": '\033[44m',
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


class errorHandle:
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
        if group not in errorLog:
            errorLog.update([(group, [])])

        errorLog[group].append(error)

    @classmethod
    def raiseErrorGroup(cls):
        if errorLog:
            raise cls._formatErrorGroup()

    @staticmethod
    def raiseError(errorType: type[Exception], info: str = '', *, note: str = "", willDo: Literal["warn", "error", "stop", "log"] = "error", fromError: Exception = None, group: str = "其它"):
        def rerr(err, fe):
            if fe:
                raise err from fe

            else:
                raise err

        if willDo in ["warn", "error", "stop"]:
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

    @staticmethod
    def formatFuncInfo(func: Callable, line: int):
        return f"from {func.__name__} in {line}"


class CMDError(Exception):
    def __init__(self, *args):
        self.args = args


class SpawnError(Exception):
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

    def __init__(self, *, output: bool = True, ignore: bool = False, color: bool | Literal["red", "yellow", "green", "blue"] = True, eliminate: str = None):
        """
        :keyword output: 是否运行指令执行完成后输出标志信息.
        :type output: bool
        :keyword ignore: 是否将Error降级为Warning以保证程序不会终止.
        :type ignore: bool
        :keyword color: 是否运行输出的字符带有色彩
        :type color: bool
        """
        self._flagOutput = output
        self._flagIgnore = ignore
        self._flagColor = color
        self._eleiminate = eliminate

    def __call__(self, instruction: str, *, cwd: PathLike | str = None, output: bool = None, encoding: Literal["gbk", "utf-8"] = "gbk", note: str = ""):
        """
        :param instruction:
        :type instruction:
        :param cwd:
        :type cwd:
        :param output:
        :type output:
        :param encoding:
        :type encoding:
        :return:
        :rtype:
        """
        correct, error = self._execute(instruction, cwd=cwd, encoding=encoding)

        tempFunc = lambda x: x.replace("\n", "").replace("\r", "").replace(" ", "")

        if self._flagIgnore:
            if flag := (self._flagOutput if output is None else output):
                outputInfo(f"{cwd if cwd else 'cmd'}>{instruction}", color="green" if self._flagColor else False, flag=flag)

                print(correct) if correct else None

            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):
                warn(  # 命令运行器Error降级警告
                    f"{error}\n{note.replace('Error', '')}", SyntaxWarning)

            return correct
        else:
            if self._eleiminate is None or (tempFunc(error) != tempFunc(self._eleiminate)):
                raise CMDError(error)

    @staticmethod
    def _execute(instruction: str, *, cwd: PathLike | str = None, encoding: Literal["gbk", "utf-8"] = "gbk") -> tuple[str, str]:
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

            errorHandle.logError(err, group="命令行")


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


class pyd:
    def __init__(self, absPath: str | PathLike[str], projectName: str = None):
        self.compliantArg(absPath)

        self._filePath = absPath

        self._projectName = projectName if projectName else self.moudleName

        self.executor = instruct(ignore=True, eliminate="文件名、目录名或卷标语法不正确。")

    @property
    def filePath(self): return self._filePath

    @cached_property
    def dirPath(self): return path.dirname(self.filePath)

    @cached_property
    def fileName(self): return path.basename(self.filePath)

    @cached_property
    def moudleName(self): return path.splitext(self.fileName)[0]

    @cached_property
    def pythonVersion(self): return findall(r"^\d\.\d{1,2}", version)[0]

    @cached_property
    def cmakeVersion(self): return findall(r"\d\.\d{1,2}", self.executor("cmake --version", output=False))[0]

    def _cmakeTxt(self): return partial(CMakeLists.format, self.cmakeVersion, self._projectName, self.pythonVersion, self._projectName)

    @staticmethod
    def compliantArg(_path: str | PathLike[str]):
        if not path.exists(_path): raise FileNotFoundError(
            f"没有找到文件'{_path}'")

        if not path.isabs(_path): raise ValueError(
            f"'{_path}'不是绝对路径,请输入绝对路径!")

        if not _path.endswith(".c"): raise ValueError(
            f"'{path.basename(_path)}'不是C后缀文件!")

    def CMakeLists(self, fileName: str):
        with open(path.join(self.dirPath, "CMakeLists.txt"), "w", encoding="utf-8") as file:

            file.write(self._cmakeTxt()(fileName))

    def build(self):
        self.CMakeLists(self.fileName)

        self.executor(r"cmake -B build -S . -Dpybind11_DIR=F:\ProgramFiles\Anaconda3\Lib\site-packages\pybind11\share\cmake\pybind11 -Wno-dev", cwd=self.dirPath)

        rename(self.filePath, path.join(self.dirPath, (newName := f"{self.moudleName}.cpp")))

        self.CMakeLists(newName)

        self.executor(r"cmake --build build --config Release", cwd=self.dirPath)

        rename(path.join(self.dirPath, "build", "Release", f"{self.moudleName}.cp311-win_amd64.pyd"), finPath := path.join(self.dirPath, f"{self.moudleName}.pyd"))

        self.executor(rf"rd /s /q {path.join(self.dirPath, 'build')}")

        rename(path.join(self.dirPath, newName), self.filePath)

        remove(path.join(self.dirPath, "CMakeLists.txt"))

        return finPath


class pyToC:
    def __init__(self, absPath: str | PathLike[str], projectName: str = None):
        self.compliantArg(absPath)

        self._filePath = absPath

        self._projectName = projectName if projectName else self.moudleName

        self.executor = instruct(ignore=True, eliminate="文件名、目录名或卷标语法不正确。")

    @property
    def filePath(self): return self._filePath

    @cached_property
    def dirPath(self): return path.dirname(self.filePath)

    @cached_property
    def fileName(self): return path.basename(self.filePath)

    @cached_property
    def moudleName(self): return path.splitext(self.fileName)[0]

    @staticmethod
    def compliantArg(_path: str | PathLike[str]):
        if not path.exists(_path): raise FileNotFoundError(
            f"没有找到文件'{_path}'")

        if not path.isabs(_path): raise ValueError(
            f"'{_path}'不是绝对路径,请输入绝对路径!")

        if not _path.endswith(".py"): raise ValueError(
            f"'{path.basename(_path)}'不是py后缀文件!")

    def setup(self):
        if not path.exists(setupPath := path.join(self.dirPath, "setup.py")):

            with open(setupPath, "w", encoding="utf-8") as file:

                file.write(setup.format(self.moudleName, self.fileName, self.moudleName))

    def build(self):
        self.setup()

        if input(f"请填写位于'{self.dirPath}'的setup.py文件,填写完成后保存并输入ok以继续: ").lower() == 'ok':

            self.executor("python setup.py build_ext --inplace", cwd=self.dirPath)

        else:
            exit()


class upload:
    def __init__(self, fileAbsolutePath: str | PathLike, *, restore: bool = True, debug: bool = False, color: bool = True, **kwargs):
        """
        --restore=bool       当出现错误时是否要还原初始状态。
        --debug=bool         是否开启Debug模式。
        --color=bool         是否运行输出信息带有色彩。
        --ignore=bool        是否将Error降级为warn以保证程序运行。
        --eliminate          排除无关紧要的错误信息, 例如: '文件名、目录名或卷标语法不正确。'

        :param fileAbsolutePath: 文件绝对路径。
        :type fileAbsolutePath: str
        :keyword restore: 当出现错误时是否要还原初始状态。
        :type restore: bool
        :keyword debug: 是否开启Debug模式。
        :type debug: bool
        :keyword color: 是否运行输出信息带有色彩。
        :type color: bool
        :keyword kwargs: 其它关键字参数,包括: ignore, eleiminate
        :type kwargs: ...
        :raise SyntaxError: 如果传入的文件路径不是绝对路径。
        """
        self._filePath = fileAbsolutePath
        self._color = color
        self._flagRestore = restore
        self._flagDebug = debug
        self.orgPath = fileAbsolutePath
        self.executor = instruct(color=color, output=debug, **kwargs)

        if not path.isabs(self._filePath):
            raise SyntaxError("文件路径必须是绝对路径!!!")

            input("任意键结束")

            exit()

        # self.flagDict = {"root": True, "dir": False, "create": False, "middle": False}
        # self.threadList = []

    @property
    def filePath(self): return self._filePath

    @filePath.setter
    def filePath(self, value):
        assert isinstance(value, str), "filePath必须为字符串类型(str)!"

        self._filePath = value

    @cached_property
    def fileName(self): return path.basename(self._filePath)

    @cached_property
    def rootPath(self): return self._filePath.replace(".py", "")

    @cached_property
    def dirPath(self): return path.join(self.rootPath, self.moduleName)

    @cached_property
    def moduleName(self): return str(self.fileName).replace(".py", "")

    @cached_property
    def separator(self): return "/" if "/" in self._filePath else "\\"

    def executeWithTry(self, instruction: str, *, cwd: str | PathLike = None, note: str = "", group: str = "其它", describe: str = None, color: str = "yellow"):
        try:
            self.executor(instruction, cwd=cwd, note=note)

            if describe: outputInfo(describe, color=color, flag=self._flagDebug)

        except Exception as err:
            err.add_note(note.replace("Warning", ""))

            errorHandle.logError(err, group=group)

    @staticmethod
    def createIfNotExist(_path: str | PathLike[str]):
        if not path.exists(_path):
            mkdir(_path)

    def threadProcessor(self, func: Callable, flag: dict, key: str, args: tuple = (), *, time: int = 0.5, kewargs: dict = None, outFlag: dict = None, outKey: str = None, outValue: bool | str = True):
        def middleware(func: Callable, flag: dict, key: str, args: tuple = (), *, time: int = 0.5, kewargs: dict = None, outFlag: dict = None, outKey: str = None, outValue: bool | str = True):
            if kewargs is None: kewargs = {}

            while not flag[key]:
                sleep(time)

            result = func(*args, **kewargs)

            if outKey:
                if outFlag:
                    outFlag[outKey] = outValue

                else:
                    flag[outKey] = outValue

            return result

        if bool(outFlag) is not bool(outKey) and not outKey:
            errorHandle.raiseError(ValueError, f"outFlag与outKey应同时填写或不填写,输入outFlag: '{outFlag}', outKey: '{outKey}'", willDo="log", note=f"{func.__name__}的线程处理器参数错误!")

        self.threadList.append(thread := Thread(target=middleware, args=(func, flag, key, args), kwargs={"time": time, "kewargs": kewargs, "outFlag": outFlag, "outKey": outKey, "outValue": outValue}))

        thread.start()

    def spawnPyi(self):
        """生成pyi文件"""
        self.executeWithTry(ins1 := f"stubgen {self.fileName}", cwd=self.dirPath, note=f"[ErrorWarning]生成pyi文件出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}", group="生成pyi", describe="spawnPyi -> 生成pyi文件.")

        pathTools.isFileExist(cacheFile := path.join(self.dirPath, ".mypy_cache"), note=f"该文件夹由spawnPyi的'{ins1}'指令生成", willDo="warn", fromError=SpawnError("生成pyi文件失败?"), group="生成pyi")

        self.executeWithTry(ins2 := f"rd /s /q {cacheFile}", cwd=self.dirPath, describe="spawnPyi -> 移除缓存文件", group="生成pyi", note=f"[ErrorWarning]移除pyi缓存文件夹出现问题: '{ins2}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}")

        self.executeWithTry(ins3 := f"move {path.join(self.dirPath, 'out', self.moduleName, f'{self.moduleName}.pyi')} {self.dirPath}", note=f"[ErrorWarning]移动pyi文件出现问题: '{ins3}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}", group="生成pyi", describe="spawnPyi -> 移动pyi文件")

        pathTools.isFileExist(ins4 := path.join(self.dirPath, "out"), note=f"该文件由spawnPyi的'{ins4}'指令生成", willDo="log", fromError=SpawnError("生成pyi文件失败?"), group="生成pyi")

        self.executeWithTry(ins5 := "rd /s /q out", cwd=self.dirPath, note=f"[ErrorWarning]删除out文件夹出现问题: '{ins5}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}", group="生成pyi", describe="spawnPyi -> 删除out文件夹")

        return path.join(self.dirPath, f"{self.moduleName}.pyi")

    def spawnPyc(self):
        self.executeWithTry(ins1 := f"python -m py_compile {self.fileName}", cwd=self.dirPath, note=f"[ErrorWarning]pyc文件编译出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnPyc, currentframe().f_lineno)}", group="生成pyc", describe="spawnPyc -> 生成pyc文件")

        if pathTools.isFileExist(pycache := path.join(self.dirPath, "__pycache__"), note=f"该文件夹由spawnPyc的'{ins1}'指令生成", willDo="log", fromError=SpawnError("生成pyc文件失败?"), group="生成pyc"):

            if pyc := [i for i in listdir(pycache) if i.endswith(".pyc")]:

                pyc = pyc[0]

                self.executeWithTry(ins2 := f"move {path.join(pycache, pyc)} {self.dirPath}", note=f"[ErrorWarning]移动pyc文件出现问题: '{ins2}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}", group="生成pyc", describe="spawnPyc -> 移动pyc文件")

                self.executeWithTry(in3 := f"rd /s /q {pycache}", note=f"[ErrorWarning]删除缓存文件出现问题: '{in3}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}", group="生成pyc", describe="spawnPyc -> 移除缓存文件")

                self.executeWithTry(ins4 := f"ren {pyc} {(pycWithOut := '.'.join([(pycList := pyc.split('.'))[0], pycList[2]]))}", cwd=self.dirPath, note=f"[ErrorWarning]重命名pyc文件出现问题: '{ins4}' {errorHandle.formatFuncInfo(self.spawnPyi, currentframe().f_lineno)}", group="生成pyc", describe="spawnPyc -> 重命名pyc文件")

                return path.join(self.dirPath, pycWithOut)

            else:
                errorHandle.raiseError(FileNotFoundError, f"列表: {pyc}中没有期望的文件.", note=f"该文件由'{ins1}'指令生成", willDo="log", group="生成pyc", fromError=SpawnError("生成pyc文件错误?"))

    def spawnHtml(self):
        self.executeWithTry(ins1 := f"pdoc -d=markdown --output {self.rootPath} {self.filePath}", note=f"[ErrorWarning]生成html文档出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnHtml, currentframe().f_lineno)}", group="生成html", describe="spawnHtml -> 生成html文档")

        pathTools.isFileExist(html := path.join(self.dirPath, f"{self.moduleName}.html"), note=f"该文件由: '{ins1}'指令生成", willDo="log", fromError=SpawnError("生成html文档错误?"), group="生成html")

        for name in ['index.html', 'search.js']:
            self.executeWithTry(ins2 := f"{'del' if '.' in name else 'rd /s /q'} {path.join(self.rootPath, name)}", note=f"[ErrorWarning]删除文件出现问题: '{ins2}' {errorHandle.formatFuncInfo(self.spawnHtml, currentframe().f_lineno)}", group="生成html", describe="spawnHtml -> 移除剩余文件")

        return path1 if path.exists(path1 := path.join(self.rootPath, f"{self.moduleName}.html")) else path.join(self.rootPath, self.moduleName, f"{self.moduleName}.html")

    def spawnREADME(self):
        htmlPath = self.spawnHtml()

        self.executeWithTry(ins1 := f"pandoc -f html -t markdown {htmlPath} -o {(readmePath := path.join(self.rootPath, 'README.md'))}", note=f"[ErrorWarning]转换html为markdown出现问题: '{ins1}' {errorHandle.formatFuncInfo(self.spawnREADME, currentframe().f_lineno)}", group="生成README", describe="spawnREADME -> 转换html为markdown")

        self.executeWithTry(ins2 := f"del {htmlPath}", note=f"[ErrorWarning]删除html文件出现问题: '{htmlPath}' {errorHandle.formatFuncInfo(self.spawnREADME, currentframe().f_lineno)}", group="生成README", describe="spawnREADME -> 删除html文件")

        return readmePath

    def spawnLicense(self):
        try:
            with open(path.join(self.rootPath, "LICENSE.txt"), "w", encoding="utf-8") as file:
                file.write(License)

        except Exception as e:
            e.add_note(f"生成LICENSE.txt失败 {errorHandle.formatFuncInfo(self.spawnLicense, currentframe().f_lineno)}")

            errorHandle.logError(e, group="生成LICENSE")

        else:
            outputInfo("spawnLicense -> 生成License.txt")

    def spawnManifest(self):
        try:
            with open(path.join(self.rootPath, "MANIFEST.in"), "w", encoding="utf-8") as file:
                file.write(
                    f"recursive-include {self.moduleName} *.pyi\n"
                    f"recursive-include {self.moduleName} *.pyc"
                )

        except Exception as e:
            e.add_note(f"生成MANIFEST.in失败 {errorHandle.formatFuncInfo(self.spawnManifest, currentframe().f_lineno)}")

            errorHandle.logError(e, group="生成MANIFEST")

        else:
            outputInfo("spawnManifest -> 生成MANIFEST.in")

    def spawnInit(self):
        try:
            with open(path.join(self.dirPath, "__init__.py"), "w", encoding="utf-8") as file:
                file.write(f"from .{self.moduleName} import *\n")

        except Exception as e:
            e.add_note(f"生成__init__.py失败 {errorHandle.formatFuncInfo(self.spawnInit, currentframe().f_lineno)}")

            errorHandle.logError(e, group="生成__init__.py")

        else:
            outputInfo("spawnInit -> 生成__init__.py")

    def spawnPyproject(self):
        try:
            text = pyproject.format(self.spawnPyc().replace(self.separator, self.separator * 2))

            with open(path.join(self.rootPath, "pyproject.toml"), "w", encoding="utf-8") as file:
                file.write(text)

        except Exception as e:
            e.add_note(f"生成pyproject失败 {errorHandle.formatFuncInfo(self.spawnPyproject, currentframe().f_lineno)}")

            errorHandle.logError(e, group="生成pyproject")

        else:
            outputInfo("spawnPyproject -> 生成pyproject.toml")

    def build(self):
        def middleDo():
            newPath = path.join(self.dirPath, self.fileName)

            try:
                rename(self.filePath, newPath)

                self.filePath = newPath

            except Exception as e:
                e.add_note(f"移动'{self.filePath}'至'{newPath}'失败 {errorHandle.formatFuncInfo(self.build, currentframe().f_lineno)}")

                errorHandle.logError(e, group="构建")

            else:
                outputInfo(f"build -> 移动{self.fileName}")

        try:
            self.createIfNotExist(self.rootPath)
            # self.threadProcessor(self.createIfNotExist, self.flagDict, "root", args=(self.rootPath, ), outKey="dir")

            self.createIfNotExist(self.dirPath)
            # self.threadProcessor(self.createIfNotExist, self.flagDict, "dir", args=(self.dirPath, ), outKey="create")

            middleDo()
            # self.threadProcessor(middleDo, self.flagDict, "middle")

            self.spawnInit()
            # self.threadProcessor(self.spawnInit, self.flagDict, "create")

            self.spawnPyproject()
            # self.threadProcessor(self.spawnPyproject, self.flagDict, "create")

            self.spawnPyi()
            # self.threadProcessor(self.spawnPyi, self.flagDict, "create")

            self.spawnREADME()
            # self.threadProcessor(self.spawnREADME, self.flagDict, "create")

            self.spawnLicense()
            # self.threadProcessor(self.spawnLicense, self.flagDict, "create")

            self.spawnManifest()
            # self.threadProcessor(self.spawnManifest, self.flagDict, "create")

            # for thread in self.threadList:
            #     thread.join()

            pathTools.isFileExist(pycache := path.join(self.dirPath, "__pycache__"), note=f"该文件夹应由spawnPyc生成 {errorHandle.formatFuncInfo(self.build, currentframe().f_lineno)}", willDo="log", fromError=SpawnError("生成pyc错误?"), group="构建")

            self.executeWithTry(ins1 := f"rd /s /q {pycache}", note=f"[ErrorWarning]移除__pycache__出现问题: {ins1} {errorHandle.formatFuncInfo(self.build, currentframe().f_lineno)}", group="构建", describe="build -> 移除__pycache__")

        except Exception as e:
            if self._flagRestore:
                rename(self.filePath, self.orgPath)

                self.executeWithTry(ins2 := f"rd /s /q {self.rootPath}", note=f"[ErrorWarning]还原过程清空出现问题: '{ins2}' {errorHandle.formatFuncInfo(self.build, currentframe().f_lineno)}", group="还原", describe="build -> 还原文件")

        else:
            rename(self.filePath, self.orgPath)

        finally:
            if errorLog:
                errorHandle.raiseErrorGroup()

        if input("现在你可以编辑pyproject.toml,编辑完成后输入ok以继续:").lower() == "ok":
            self.executor("python -m build", cwd=self.rootPath)

        print(f"现在你可以运行`cd {self.rootPath}`并输入`python -m twine upload --repository testpypi dist/*`以开始上传.\n#您的token:'pypi-AgENdGVzdC5weXBpLm9yZwIkYzkwNzZjMTItOWU5OS00YWM4LWFiMWEtYWQwMzU1ZGZkYWVkAAIqWzMsIjRiNDBlZjEwLWRhMmQtNDVlMC1hYjM0LTY1MDI3YzBkYTJmMyJdAAAGILpCa7oU6b1m6k7hUMmp-dybDNN5R1bWdGghvxjjaQll'")


parser = ArgumentParser(prog="PYPI软件包上传工具", description="用于上传一个python软件包", epilog="__init__(self, fileAbsolutePath: str | PathLike, *, restore: bool = True, debug: bool = False, color: bool = True, **kwargs)")
parser.add_argument("file", help="你需要上传的python文件的绝对路径。")
parser.add_argument("-R", "--restore", default="True", choices=["True", "False"], help="当出现错误时是否要还原初始状态。(默认值: True)")
parser.add_argument("-C", "--color", default="True", choices=["True", "False"], help="是否运行输出信息带有色彩。(默认值: True)")
parser.add_argument("-D", "--debug", default="False", choices=["True", "False"], help="是否开启debug模式。(默认值: False)")
parser.add_argument("-I", "--ignore", default="True", choices=["True", "False"], help="是否将Error降级为warn以保证程序运行。(默认值: True)")
parser.add_argument("-E", "--eliminate", default=(eDef := "文件名、目录名或卷标语法不正确。"), help="排除无关紧要的错误信息, 例如: '文件名、目录名或卷标语法不正确。'(默认值: '文件名、目录名或卷标语法不正确。')")
parser.add_argument("-V", "--vision", help="版本")
args = parser.parse_args()


if __name__ == '__main__':
    # pyinstaller -F uploadTools.py -n upload -i upload_1.ico

    # ins = upload(r"D:\xst_project_202212\codeSet\Python\test.py", debug=True, ignore=False, eliminate="文件名、目录名或卷标语法不正确。")
    # ins.build()

    # print(args.file, args.restore, args.color, args.debug, args.eliminate)

    if args.vision:
        print(__vision__)
    else:
        ins = upload(args.file, debug=strToBool(args.debug, default=False), ignore=strToBool(args.ignore, default=True), eliminate=args.eliminate, color=strToBool(args.color, default=True), restore=strToBool(args.restore, default=True))
        ins.build()
