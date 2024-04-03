#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/11/1 10:53
# 当前项目名: Python
# 编码模式: utf-8
# 注释:
# -------------------------<Lenovo>----------------------------
from subprocess import Popen, PIPE
from os import path, listdir, mkdir, rename, remove
from pkgutil import iter_modules
from warnings import warn
from typing import Literal, Callable
from inspect import currentframe

License = """
Copyright (c) 2018 The Python Packaging Authority

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

pyproject = """
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = ""
version = ""
authors = [
  {{ name="", email="" }},
]
description = ""
readme = ""
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[tool.poetry.scripts]
files = ["{}"]

[project.urls]
"Homepage" = ""
"Bug Tracker" = ""

"""


class CMDError(Exception):
    def __init__(self, *args):
        self.args = args


class instruct:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *, allowOUTPUT: bool = True, ignore: bool = False):
        self._OUT = allowOUTPUT
        self._ignore = ignore

    def __call__(self, instruction: str, *, cwd: str = None, allowOUTPUT: bool = True):

        if self._OUT is False:
            allowOUTPUT = self._OUT

        result = self._execute(instruction, cwd=cwd)

        right = result["R"]
        error = result["E"]

        if not self._ignore and error: raise CMDError(error)

        if allowOUTPUT:
            print(f"{cwd if cwd else 'cmd'}>{instruction}")
            if right: print(right)
            warn(  # 命令行错误警告
                error[:-1] if error[-1] == "\n" else error, SyntaxWarning)

        return right

    def nowPath(self, *, cwd: str = None):
        return self._execute("cd", cwd=cwd)["R"].replace("\n", "")

    @staticmethod
    def _execute(instruction: str, *, cwd: str = None) -> dict[str, str]:
        result = Popen(instruction, shell=True, stdout=PIPE, stderr=PIPE, cwd=cwd)

        right = result.stdout.read().decode("gbk", errors='ignore')
        error = result.stderr.read().decode('gbk', errors='ignore')

        return {"R": right, "E": error}


class upload:
    def __init__(self, FileAbsolutePath: str, rootPath: str = None, *, onlyFile: bool = False, clear: bool = True):
        self.separator = "/" if "/" in FileAbsolutePath else "\\"
        self.executor = instruct(ignore=True)
        self.orgPath = FileAbsolutePath
        self._filePath = FileAbsolutePath  # py文件绝对路径
        self.fileName = path.basename(self.filePath)  # py文件名
        self.moduleName = self.fileName.replace(".py", "")  # 无py后缀文件名
        self._clear = clear

        # 单文件模式
        if onlyFile:
            self.rootPath = self.filePath.replace(".py", "")
            self.dirPath = path.join(self.rootPath, self.moduleName)  # py文件所属文件夹路径

        # 文件夹模式
        else:
            self.rootPath = rootPath if rootPath else self.separator.join(self.pathList[:-3])  # 项目根目录
            self.dirPath = self.separator.join(self.pathList[:-1])  # py文件所属文件夹路径

        self.projectName = self.rootPath.split(self.separator)[-1]  # 项目名称

    @property
    def filePath(self):
        """py文件绝对路径"""
        return self._filePath

    @property
    def pathList(self):
        return self.filePath.split(self.separator)  # 文件分割列表

    @filePath.setter
    def filePath(self, value: str):
        self.notExistsRaise(value)
        if not value.endswith(".py"): raise ValueError(
            "The file path you entered is not a py type file") from FileNotFoundError
        self._filePath = value

    @staticmethod
    def notExistsRaise(anyPath: str):
        if not path.exists(anyPath): raise ValueError(
            "The file path you entered does not exist") from FileNotFoundError(
            f"[Errno 2] No such file or directory: '{anyPath}'")

    def buildDir(self):
        pass

    def _fileNotFound(self, anyPath: str, *, errorLog: tuple[Callable, int] = None):
        raise FileNotFoundError(
            f"[Errno 2] No such file or directory: '{anyPath}'{'' if errorLog is None else f' from {errorLog[0].__name__} in {errorLog[1]}'}")  # 执行报错

    def _existDo(self, instruction: str, filename: str = None, *, dirName: str = None, fileReplace: bool = False,
                 cwd: str = None, errorLog: tuple[Callable, int] = None):
        """
        当存在文件或文件夹时执行.

        :param instruction: 指令,当指令中含有PATH关键字时且fileReplace为True时将会被替换为`dirName+filename`
        :type instruction:
        :param filename: 带后缀文件名,可为空
        :type filename:
        :param dirName:
        :type dirName:
        :param fileReplace:
        :type fileReplace:
        :return:
        :rtype:
        """
        filename = path.join(dirName, filename) if dirName is not None else filename
        if path.exists(filename):
            self.executor(instruction.replace("PATH", filename) if fileReplace else instruction, cwd=cwd)
        else:
            self._fileNotFound(filename,
                               errorLog=(self._existDo, currentframe().f_lineno) if errorLog is None else errorLog)

    @staticmethod
    def createIfNotExist(anyPath: str):
        if not path.exists(anyPath):
            mkdir(anyPath)

    def pyi(self):
        """
        生成pyi文件

        :param FileAbsolutePath:
        :type FileAbsolutePath:
        :return:
        :rtype:
        """
        currentPath = self.dirPath

        self.executor(f"stubgen {self.fileName}", cwd=currentPath)  # 生成pyi文件

        self._existDo("rd /s /q PATH", ".mypy_cache", dirName=self.dirPath, fileReplace=True, cwd=currentPath,
                      errorLog=(self.pyi, currentframe().f_lineno))  # 移除缓存文件

        self._existDo(f"move PATH {self.dirPath}", f"{self.moduleName}.pyi",
                      dirName=path.join(self.dirPath, f"out{self.separator}{self.moduleName}"), fileReplace=True,
                      errorLog=(self.pyi, currentframe().f_lineno))  # 移动.pyi文件

        self.executor("rd /s /q out", cwd=currentPath)

        return path.join(self.dirPath, f"{self.moduleName}.pyi")

    def pyc(self):
        """
        生成pyc文件

        :param FileAbolutePath:
        :type FileAbolutePath:
        :return:
        :rtype:
        """
        currentPath = self.dirPath

        self.executor(f"python -m py_compile {self.fileName}", cwd=currentPath)  # 编译py文件

        pycache = path.join(self.dirPath, "__pycache__")  # 缓存文件

        if "__pycache__" in listdir(self.dirPath):
            fileList = listdir(pycache)
            if pyc := [i for i in fileList if i.endswith(".pyc")]:
                pyc = pyc[0]
                self.executor(f"move {path.join(pycache, pyc)} {currentPath}")  # 移动pyc文件

                self.executor(f"rd /s /q {pycache}")  # 删除缓存文件

                pycWithOut = ".".join([(pycList := pyc.split("."))[0], pycList[2]])

                self.executor(f"ren {pyc} {pycWithOut}", cwd=currentPath)

                return path.join(self.dirPath, pycWithOut)
            else:
                self._fileNotFound(".pyc", errorLog=(self.pyc, currentframe().f_lineno))
        else:
            self._fileNotFound(pycache, errorLog=(self.pyc, currentframe().f_lineno))

    def html(self):
        self.executor(f"pdoc --output {self.rootPath} {self.filePath}")

        html = path.join(self.dirPath, self.moduleName + ".html")

        if path.exists(html):
            self.executor(f"move {html} {self.rootPath}")

            for name in ["index.html", "search.js"]:
                self.executor(f"{'del' if '.' in name else 'rd /s /q'} {path.join(self.rootPath, name)}")

        else:
            self._fileNotFound(html, errorLog=(self.html, currentframe().f_lineno))

        return path.join(self.rootPath, f"{self.moduleName}.html")

    def README(self, mode: Literal["markdown", "rst"] = "markdown"):

        assert mode in ["markdown", "rst"], f"{mode} not in ('markdown', 'rst')"

        html = self.html()

        readme = path.join(self.rootPath, 'README' + ('.rst' if mode == 'rst' else '.md'))

        self.executor(f"pandoc -f html -t {mode} {html} -o {readme}")

        self.executor(f"del {html}")

        return readme

    def license(self):
        with open(path.join(self.rootPath, "LICENSE.txt"), "w", encoding="utf-8") as file:
            file.write(License)

    def manifest(self):
        with open(path.join(self.rootPath, "MANIFEST.in"), "w", encoding="utf-8") as file:
            file.write(
                f"recursive-include {self.projectName} *.pyi\n"
                f"recursive-include {self.projectName} *.pyc"
            )

    def findImport(self):
        module = None
        mp = self.filePath[:-3].replace(self.separator, ".").split('.')
        times = -1

        while not module:
            moudlePath = ".".join(mp[times:])

            try:
                module = __import__(moudlePath)
            except ModuleNotFoundError:
                times -= 1
            else:
                module = __import__(moudlePath, fromlist=[""])

        for i in iter_modules(module):
            print(i)

    def init(self):
        with open(path.join(self.dirPath, "__init__.py"), "w", encoding="utf-8") as file:
            file.write(
                f"from .{self.moduleName} import *\n"
            )

    def pyproject(self):
        text = pyproject.format(self.pyc().replace(self.separator, self.separator * 2))

        with open(path.join(self.rootPath, "pyproject.toml"), "w", encoding="utf-8") as File:
            File.write(text)

    def build(self):
        """
        TODO:

        从文件生成项目:
            1. 从.py文件所在目录下创建项目根文件夹
            2. 在项目根文件夹中创建同名软件包
            3. 将.py文件移至软件包
            4. 在软件包中创建__init__.py文件
            5. 在项目根目录生成pyproject.toml(pyc文件已生成)
            6. 在项目根目录生成pyi文件
            7. 在项目根目录生成README
            8. 在项目根目录生成LICENSE.txt
            9. 在项目根目录生成MANIFEST.in
            10. 打包,上传
        """
        try:
            self.createIfNotExist(self.rootPath)

            self.createIfNotExist(self.dirPath)

            print(self.separator.join(self.pathList[:-1]), self.dirPath)

            if self.separator.join(self.pathList[:-1]) != self.dirPath:
                rename(self.filePath, (newPath := path.join(self.dirPath, self.fileName)))

                self.filePath = newPath

            self.init()

            self.pyproject()

            self.pyi()

            self.README("markdown")

            self.license()

            self.manifest()

            self._existDo(f"rd /s /q PATH", "__pycache__", dirName=self.dirPath, fileReplace=True,
                          errorLog=(self.build, currentframe().f_lineno))

            if input("现在你可以编辑pyproject.toml,编辑完成后输入ok以继续:").lower() == "ok":
                self.executor("python -m build", cwd=self.rootPath)

                # self.executor("python -m twine upload --repository testpypi dist/*", cwd=self.rootPath)
        except Exception as e:
            if self._clear:
                rename(self.filePath, self.orgPath)
                self.executor(f"rd /s /q {self.rootPath}")
                e.add_note("清空")
            raise e


if __name__ == '__main__':
    ins = upload(r"D:\xst_project_202212\Python\test.py", onlyFile=True)
    ins.build()
    # ins.checkDir()
    # ins.findImport()
