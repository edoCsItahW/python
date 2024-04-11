#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/20 22:48
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from subprocess import PIPE, Popen
from traceback import format_exc
from warnings import warn
from inspect import signature, getmembers, getmodule, stack, isfunction, getdoc, isclass
from typing import Literal, Callable, Annotated, Any
from pandas import set_option, Series
from types import TracebackType
from types import ModuleType
from json import load, dump
from copy import copy
from os import listdir, path, remove, rmdir, walk, PathLike
from re import findall, sub

__version__ = "0.0.12"

try:
    from ANSIdefine.ansiDefine import ansiManger
except Exception:
    from ansiDefine.ansiDefine import ansiManger  # type: ignore

__all__ = [
    "FileTree",
    "PYI_spawnTools",
    "clearfolder",
    "fullpath",
    "get_function_docs_in_file",
    "localattr",
    "runInCMD",
    "to_EXE",
    "updateAllPackage",
    "varname",
    "CMDError",
    "instruct",
    "jsonOpen"
]

color = ansiManger()


def clearfolder(folder_path):
    """
    用于清空文件夹

    :param folder_path: 文件夹路径
    :type folder_path: str
    :return: 操作执行函数不做返回
    :retype: None
    """
    # 遍历文件夹中的所有文件和子文件夹
    for filename in listdir(folder_path):
        file_path = path.join(folder_path, filename)
        # 判断是否为文件
        if path.isfile(file_path):
            # 删除文件
            remove(file_path)
        # 判断是否为文件夹
        elif path.isdir(file_path):
            # 递归清空子文件夹
            clearfolder(file_path)
            # 删除子文件夹
            rmdir(file_path)


def FileTree() -> None:
    """
    打印树状目录
    """
    inp = int(input('输入模式\n1.打印文件夹和文件\t2.打印文件夹\n:'))
    filepath = input('输入文件路径\n(1.默认):')
    filepath = 'E:\\数学' if filepath == '1' else filepath

    # 定义计算文件夹大小的函数
    def get_folder_size(folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in walk(folder_path):
            for f in filenames:
                fp = path.join(dirpath, f)
                try:
                    total_size += path.getsize(fp)
                except PermissionError:
                    print("Permission denied: ", fp)
        return total_size

    if inp == 1:

        def print_tree(dir_path: str, *, prefix: str = '', folder_level: int = 0) -> None:
            files = listdir(dir_path)
            folder_level += 1
            for i, file in enumerate(sorted(files)):
                path_ws = path.join(dir_path, file)
                if path.isdir(path_ws):
                    folder_size = get_folder_size(path_ws)
                    inside = f"{folder_size}Byte" if folder_size <= 1024 else \
                        f"{folder_size // 1024}KB" if 1024 < folder_size <= 1024 ** 2 else \
                            f"{folder_size // 1024 ** 2}MB" if 1024 ** 2 < folder_size <= 1024 ** 3 else \
                                f"{folder_size // 1024 ** 3}G"
                    folder_info = f'大小:{inside}({len(listdir(path_ws))}个文件)'
                    if i == len(files) - 1:
                        print(
                            prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
                        print_tree(path_ws, prefix=prefix + '    ', folder_level=folder_level)
                    else:
                        print(
                            prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
                        print_tree(path_ws, prefix=prefix + '│   ', folder_level=folder_level)
                else:
                    file_size = path.getsize(path_ws)
                    inside = f"{file_size}Byte" if file_size <= 1024 else \
                        f"{file_size // 1024}KB" if 1024 < file_size <= 1024 ** 2 else \
                            f"{file_size // 1024 ** 2}MB" if 1024 ** 2 < file_size <= 1024 ** 3 else \
                                f"{file_size // 1024 ** 3}G"
                    file = "".join(file.split(".")[:-1]) + "." + color.f_under_line(file.split(".")[-1],
                                                                                    _ANSI=color.b_wide)
                    if i == len(files) - 1:
                        print(prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({inside})')
                    else:
                        print(prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({inside})')

        print_tree(filepath)

    elif inp == 2:

        def print_tree_nf(dir_path, *, prefix = '', folder_level = 0):
            files = listdir(dir_path)
            folder_level += 1
            for i, file in enumerate(sorted(files)):
                path_ws = path.join(dir_path, file)

                if path.isdir(path_ws):
                    folder_size = get_folder_size(path_ws)
                    inside = f"{folder_size}Byte" if folder_size <= 1024 else \
                        f"{folder_size // 1024}KB" if 1024 < folder_size <= 1024 ** 2 else \
                            f"{folder_size // 1024 ** 2}MB" if 1024 ** 2 < folder_size <= 1024 ** 3 else \
                                f"{folder_size // 1024 ** 3}G"
                    folder_info = f'大小:{inside}({len(listdir(path_ws))}个文件)'
                    if i == len(files) - 1:
                        print(
                            prefix + '└── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
                        print_tree_nf(path_ws, prefix=prefix + '    ', folder_level=folder_level)
                    else:
                        print(
                            prefix + '├── ' + f'\033[3{folder_level}m{file}\033[0m({folder_level}级文件夹)({folder_info})')
                        print_tree_nf(path_ws, prefix=prefix + '│   ', folder_level=folder_level)

        print_tree_nf(filepath)


def runInCMD(*args: str, allowRIGHT: bool = True, allowERROR: bool = True, returnR: bool = False, returnE: bool = False,
             mod: Literal["utf-8", "gbk", "latin-1"] = "gbk"):
    result = ""
    for arg in args:
        result = Popen(arg, shell=True, stdout=PIPE, stderr=PIPE)

    right = result.stdout.read().decode(mod, errors='ignore') if allowRIGHT else None
    error = color.f_otherColor(f"提示符回溯:\n\t{result.stderr.read().decode('gbk', errors='ignore')}", r=247, g=84,
                               b=100) if allowERROR else None

    if allowRIGHT or allowERROR:
        print(f"结果:\n{right}\n{error}")

    if returnR and returnE:
        return right, error
    elif returnR:
        return right
    elif returnE:
        return error


def varname(variable: object):
    module = getmodule(stack()[1][0])
    # 找到在跨包级的命名空间里是class_name类的实例
    instances = [name for name, obj in getmembers(module) if obj is variable]
    return instances[0]


def localattr(func: Callable): return list(signature(func).parameters.keys())


def fullpath(dirpath: str): return [path.join(dirpath, filename) for filename in listdir(dirpath)]


def to_EXE(pyPath: str, mutliPath: list = None, figPath: list[tuple] = None, console: bool = True):
    """
    如果有多个文件相关联,那么在a的第一个数字中加入文件路径即可.
    有静态文件及配置文件则将元组(源路径, 打包后在包中的路径)填入datas数组中即可.
    如需关闭控制台在则设置console设置为False
    注意:如果该文件或多文件中的主文件运行后不执行任何交换,则不会正确的打包.
    pyinstaller --icon=path/to/icon.ico your_script.py
    """
    from confunc import waiter
    from textTools import isChinese
    if any(isChinese(word) for word in pyPath):
        raise ValueError("不支持中文文件名")
    print("以下是仅是第一次信息,请等待第二次信息,打包过程可能较长.")
    res = runInCMD(f"pyi-makespec {pyPath}", returnR=True)
    filepath = findall(r"(?<=Wrote\s)[^.]*\.[^.]*", res)[0]
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()
    text = text.replace(f"['{pyPath}']".replace("\\", r"\\"), str([pyPath] + mutliPath)) \
        if isinstance(mutliPath, list) else text
    text = text.replace("datas=[]", f"datas={str(figPath)}") if \
        isinstance(figPath, list) and all(isinstance(t, tuple) for t in figPath) else text
    text = text.replace("console=True", "console=False") if console is False else text
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text)
    if input(
            f"现在你可以手动运行代码:\n\t{color.f_yellow('pyinstaller')} {filepath}\n这样可以看到具体进程.\n\t需要继续吗(Y:继续,N:停止).").lower() == "y":
        print("以下是第二次信息,打包即将开始.")
        wait = waiter(20)
        wait.begin_wait()
        runInCMD(f"pyinstaller {filepath}")
        wait.end_wait()
    else:
        print("已停止.")


def updateAllPackage():
    packages = runInCMD("pip list", returnR=True)
    for package in (l := findall(r"(?<=\s)[a-zA-Z].*?(?=\s)", packages))[l.index("numba"):]:
        runInCMD(f"pip install --upgrade {package}")


def spawn_package__all__(packageName: Annotated[str, "like constantPackage.con_func"]):
    if packageName[-3:] == ".py" and ("\\" in packageName or "/" in packageName):
        packageName = ".".join(packageName[:-3].split("\\" if "\\" in packageName else "/"))

    tools = PYI_spawnTools(packageName)
    content = tools.content

    mode = __import__(packageName, fromlist=[""])

    impList = sum([i.split(", ") for i in findall(r"(?<=import\s).*", content)], start=[])

    # funclist = [_ for _ in dir(mode) if not _.startswith("__")]
    text = "__all__ = [\n"

    for name, member in filter(lambda x: not x[0].endswith("__"), getmembers(mode)):
        if (p := getmodule(member)) is None:
            if name not in impList:
                text += f"    \"{name}\",\n"
        else:
            if p.__name__ == packageName:
                text += f"    \"{name}\",\n"

    print(text[:-2] + "\n]")


def get_function_docs_in_file(modeName: str | ModuleType = None, *, otherMagic: bool = False) -> Series | list:
    """
    这是用来显示func_Define这个python文件里的所有函数和对应的简要提示的.

    :param modeName: 模块名或.py文件名.
    :type modeName: str
    :keyword otherMagic: 是否运行结果中出现未显示定义的魔法变量,如: __str__, ...
    :type otherMagic: bool
    :return: 将包含函数和简要提示的Series.
    :rtype: Series
    """
    if isinstance(modeName, ModuleType):
        modeName = modeName.__name__

    if not otherMagic:
        tools = PYI_spawnTools(modeName)
        logdict, _ = tools.rmMagicV

    set_option("display.max_rows", None)
    set_option("display.max_columns", None)

    # 过滤出所有函数并构造名称和文档字符串的字典
    functions_dict = {}
    try:
        for name, member in globals().items() if modeName is None else getmembers(
                mode := __import__(modeName, fromlist=[""])):
            if (isfunction(member) or isclass(member)) and getmodule(member).__name__ == modeName:
                docs = getdoc(member)  # 文档字符串
                # 将函数名称及其文档字符串添加到字典中

                functions_dict[f"<{name}>" if isclass(member) else name] = docs.split("\n\n")[0] if docs else \
                    f"(这个{'函数' if isfunction(member) else '变量'}没有简要提示.)"

                if isclass(member) and getmodule(member).__name__ == modeName:

                    for n, m in filter(lambda x: hasattr(member, x[0]), getmembers(getattr(mode, member.__name__))):

                        if not otherMagic and name in logdict and n in logdict[name]:
                            functions_dict[
                                f"{name}.{n}"] = f"(这个{'函数' if isfunction(m) else '变量'}没有简要提示.)" if (
                                                                                                                    docs := getdoc(
                                                                                                                        m)) is None else \
                                docs.split("\n\n")[0]

                        if otherMagic:
                            functions_dict[
                                f"{name}.{n}"] = f"(这个{'函数' if isfunction(m) else '变量'}没有简要提示.)" if (
                                                                                                                    docs := getdoc(
                                                                                                                        m)) is None else \
                                docs.split("\n\n")[0]

    except AttributeError:
        warn(format_exc(), SyntaxWarning)

    return Series(functions_dict)


class PYI_spawnTools:
    """从.py文件中生成.pyi存根文件"""

    def __init__(self, pyFileName: Annotated[str, "like constantPackage.con_func"] | ModuleType, *, autoFile: str = "",
                 test: bool = False):
        self._test = test

        errorList = []

        try:
            if pyFileName[-3:] == ".py" or "/" in pyFileName or "\\" in pyFileName:
                pyFileName = ".".join(pyFileName[:-3].split("/" if "/" in pyFileName else "\\"))

            if self._test: print(f"初始文件名: {pyFileName}")

            self.dirPath = path.join(autoFile, f"{pyFileName.split('.')[-1]}.pyi") if autoFile is not None else None

            if self._test: print(f"目标pyi文件: {self.dirPath}")

            self.mode = pyFileName if isinstance(pyFileName, ModuleType) else __import__(pyFileName, fromlist=[""])

            if self._test: print(f"实际导入包: {self.mode}")

            if self._test: print(f"类列表: {self._classList}")

            self.__funcOfClass = {}

            for cls in self._classList:
                try:
                    self.__funcOfClass.update([(cls, dir(getattr(self.mode, cls.split("(")[0])))])
                except Exception:
                    warn(format_exc(), SyntaxWarning)

            # self.__funcOfClass = {cls: dir(getattr(self.mode, cls.split("(")[0])) for cls in self._classList}

            if self._test: print(f"包中的类: {self.__funcOfClass}")

        except Exception as e:
            errorList.append(e)

        if errorList: raise ExceptionGroup("初始化错误组: ", errorList)

    # 文件中的所有代码内容
    @property
    def content(self):
        with open(self.mode.__file__, "r", encoding="utf-8") as file:
            text = file.read()

        pset = set()
        if "def" not in text:

            plist = findall(r"(?<=from\s)(.*?)\simport\s(.*)\b", text)

            for p in plist:
                pset.add(p[0])

            pset.add(self.mode.__file__)

            warn(
                f"\n文件<{self.mode.__file__}>也许不是源定义文件,你可能需要到以下文件中寻找:\n\t{pset}.")

        return text

    # 提取出的函数定义列表
    @property
    def _sentenceList(self):
        return [sub(r"/n\s*", " ", word) if "/n" in word else word for word in
                findall(r"def\s.*?:(?=/)", self.content.replace("\n", "/n"))]

    # 提取出的所有类
    @property
    def _classList(self):
        return list(filter(lambda x: all([i not in x for i in ("{", ",", "}", "/", "\\", ":", "\"")]),
                           findall(r"(?<=class\s).*?(?=:)", self.content)))

    # 键为类,值为类对应的方法的字典
    @property
    def funcOfClass(self):
        return self.__funcOfClass

    @funcOfClass.setter
    def funcOfClass(self, value: dict | tuple[str, list]):
        if isinstance(value, dict):
            self.__funcOfClass = value
        elif isinstance(value, tuple):
            self.__funcOfClass[value[0]] = value[1]

    def _checkSenList(self, sentencelist):
        # type: (list) -> tuple[dict, dict]
        """
        对语句列表进行检查,排除不正确的提取.

        @param sentencelist: 语句列表.
        @type sentencelist: list
        @return: 对每个类的魔术方法的记录字典,以及出现问题的以索引值为键,修正后的列表为值的字典.
        @retype: tuple[dict, dict]
        """
        logdict = {cls: set() for cls in self._classList}

        errordict = {}

        for i, word in enumerate(sentencelist):
            funcName = findall(r"(?<=def\s)\w+?(?=\()", word)

            if len(funcName) > 1:
                errordict.update([(i, funcName)])
            else:
                if funcName[0].endswith("__"):
                    for key in self._classList:
                        if funcName[0] in self.funcOfClass[key]:
                            logdict[key].add(funcName[0])

        return logdict, errordict

    def findImport(self):
        return findall(r"from\s.*?import\s.*\b", self.content)

    @property
    def rmMagicV(self):
        senList = copy(self._sentenceList)

        logdict, errordict = self._checkSenList(self._sentenceList)

        for i in errordict.keys():
            senList = senList[:i] + [findall(fr"def\s{errordict[i][idx]}\(.*?\).*?:", w)[0] for idx, w in
                                     enumerate([f"def{i}" for i in senList[i].split("def") if i])] + senList[i + 1:]

        funcDict = {findall(r"(?<=def\s)\w+?(?=\()", word)[0]: word for word in senList}

        for key in self._classList:
            self.funcOfClass = (key, [i for i in self.funcOfClass[key] if not i.endswith("__") or i in logdict[key]])

        return self.funcOfClass, funcDict

    def getAllFunc(self):
        s = "\n"

        self.funcOfClass, funcDict = self.rmMagicV

        finddict = {}

        for key in funcDict.keys():
            if any((clist := [(i if key in self.funcOfClass[i] else False) for i in self.funcOfClass.keys()])):
                finddict.update([(className, f"class {className}:")]) if (className := [i for i in clist if i][
                    0]) not in finddict.keys() else None
                finddict.update(
                    [(key, f"{'' if 'self' in funcDict[key] else f'    @staticmethod{s}'}    {funcDict[key]} ...")])
            else:
                finddict.update([(key, f"{funcDict[key]} ...")])

        return finddict

    def toPYI(self, filePath: str = None):
        if filePath is None:
            filePath = self.dirPath
        with open(filePath, "w", encoding="utf-8") as file:
            file.write("\n".join(self.findImport()) + "\n" + "\n".join(self.getAllFunc().values()))


def docToMd(filePath: str, Class: object) -> None:
    from netTools import translate_mutil
    """将一个模块中的__doc__转换为文档"""
    sy, r, l = "\n", "{", "}"

    iters = list(filter(lambda x: not x.endswith("__"), dir(Class)))

    with open(filePath, "w", encoding="utf-8") as file:
        file.write(f"# {Class.__name__}\n\n")

        for title in iters:
            file.write(f"## [{title}](#{title}-{title})\n")

        for attr in iters:
            file.write(
                f"\n方法名:\n#### {attr} {r}#{attr}{l}\n:\'{(doc := getattr(Class, attr).__doc__)}\': \n翻译:\'{doc if doc is None else translate_mutil(doc.replace(sy, ''))}\'\n\n")
            print(attr)


def outputInfo(info: str, *, color: Literal["red", "green", "blue", "yellow"] | str | bool = "green",
               flag: bool = True):
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


if __name__ == '__main__':
    # executor = instruct(output=True, ignore=True)
    # print(executor("nslookup www.baidu.com"))
    pass
