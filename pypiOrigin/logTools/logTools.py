#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/20 21:03
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from functools import wraps
from traceback import format_exc
from warnings import warn, catch_warnings, simplefilter
from inspect import getmodule
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, basicConfig, debug, info, warning, error, critical
from inspect import currentframe
from typing import Callable, Literal
from re import sub, findall


__version__ = "0.0.4"


try:
    from ANSIdefine.ansiDefine import ansiManger
except Exception:
    from ansiDefine.ansiDefine import ansiManger

__all__ = [
    "errorLogger",
    "ignoreErrorAndWarning",
    "logError",
    "logset",
    "returnback",
    "tranTBack"
]


def logset(logfilepath: str = Literal[r"like: C:\you\path\file.txt"] | str, leve: int = 2):
    """
    日志输出初始化方法.

    :param logfilepath: 目标日志文件路径.
    :type logfilepath: str
    :param leve: 输出级别
    :type leve: int
    :return: 操作执行函数不做返回.
    """
    try:
        errdict = {1: DEBUG, 2: INFO, 3: WARNING, 4: ERROR, 5: CRITICAL}
        basicConfig(filename=logfilepath,
                    format=f'\n%(asctime)s [监查反馈(错误级别:%(levelname)s): 行号: %(lineno)s -> 执行错误文件:<{__file__}>, '
                           f'源错误文件:<%(filename)s>]\n'
                           '"""信息上报:\n%(message)s\n"""\n',
                    datefmt='%Y-%m-%d %H:%M:%S', level=errdict[leve], encoding="utf-8", force=True)
    except KeyError as message:
        raise KeyError(f"{message}(不应为1-5之外的数字)")


def returnback() -> str: return format_exc().replace("Traceback (most recent call last):\n", '')


# 剔除错误输出中的Traceback (most recent call last):


def tranTBack(errorinfo: str, tranfin: bool = False) -> str:
    from textTools import toEnglish
    from netTools import translate_mutil
    color = ansiManger()
    text = errorinfo.replace("Traceback (most recent call last)", "错误回溯 (最后一次调用)")
    text = sub(r"\bFile\b", "含错文件:", text)
    text = sub(r"\bline\b", "行号:", text)
    for i in findall(r'(?<=\b含错文件:\s")(.*)(?=",\s\b)', text):
        i = i.replace("\\", r"\\")
        text = sub(i, color.f_systemBULE(f"{i}", _ANSI=color.b_under_line) + color.systemRED, text)
    rep = findall(r"(?<=in\s)\w+", text)
    for i, v in enumerate(findall(r"\bin\s+\w+", text)):
        text = sub(v, f"在<{rep[i]}>中", text)
    if tranfin:
        errorm = text.split("\n")[-2]
        finm = translate_mutil(errorm)
        text = text[:-1] + f'\n参考翻译:"{toEnglish(finm)}"' if finm else ""
    return text


def logError(leve: int = 3, allowprint: bool = True, reserve: bool = False, translate: bool = True,
             tranfin: bool = False, *, mess: str = None):
    """
    断点错误定向(PS:需调用logset方法初始化日志文件路径).

    :param leve: 错误级别(级别从低到高)
                 1.``debug``
                 2.``info``
                 3.``warning``
                 4.``error``
                 5.``critical``
    :type leve: int
    :param allowprint: 是否允许输出至控制台.(默认:True)
    :type allowprint: bool
    :param reserve: 是否保留前缀`Traceback (most recent call last):`.(默认:False)
    :type reserve: bool
    :param translate: 开启关键字翻译.(默认为True)
    :type translate: bool
    :param tranfin: 是否运行提供最后一句话的参考翻译.(默认为True)
    :type tranfin: bool
    :param mess: 额外的信息
    :type mess: str
    :return: 操作执行函数不做返回.
    :retype: None
    """

    if not isinstance(mess, str):
        warn("mess参数只接收字符串")

    errorinfo = format_exc()[:-2] if reserve else returnback()[:-2]
    errorinfo = "\n".join([mess] + errorinfo.split("\n")) if mess else errorinfo
    if leve == 1:
        debug(errorinfo)
    elif leve == 2:
        info(errorinfo)
    elif leve == 3:
        warning(errorinfo)
    elif leve == 4:
        error(errorinfo)
    elif leve == 5:
        critical(errorinfo)
    else:
        raise ValueError("不应为1-5之外的数字")

    if allowprint:
        print(ansiManger().f_otherColor(tranTBack(format_exc(), tranfin), RGB=ansiManger().systemRED) if translate else format_exc())


def errorLogger(leve: int = 4, allowprint: bool = True, reserve: bool = False, translate: bool = True,
                tranfin: bool = True, *, mess: str = None):
    """
    用来记录错误信息的装饰器.

    :param leve: 错误级别(级别从低到高)
                 1.``debug``
                 2.``info``
                 3.``warning``
                 4.``error``
                 5.``critical``
    :type leve: int
    :param allowprint: 是否允许输出至控制台.(默认:True)
    :type allowprint: bool
    :param reserve: 是否保留前缀`Traceback (most recent call last):`.(默认:False)
    :type reserve: bool
    :param translate: 开启关键字翻译.(默认为True)
    :type translate: bool
    :param tranfin: 是否开启详细错误信息翻译.(默认为False)PS.时间开销极大
    :type tranfin: bool
    :return: 返回经装饰的原函数.
    :retype: Callable
    """
    def loggergetfunc(func):

        nonlocal mess
        mess = mess if mess else f"记录到错误 -> 位于文件:<{getmodule(func).__file__}>中的函数:<{func.__name__}>"

        @wraps(func)
        def loggerwrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)  # 错误记录装饰器errorLogger接收到错误
            except Exception:
                logError(leve, allowprint, reserve, translate, tranfin,
                         mess=mess)

        return loggerwrapper

    return loggergetfunc


def ignoreErrorAndWarning(allowLog: bool = True, leve: int = 3, allowprint: bool = True, reserve: bool = False,
                          translate: bool = True,
                          tranfin: bool = True,
                          ErrorType: tuple = None,
                          WarningType: tuple = None) -> Callable:
    """
    用来拦截错误和警告,包括记录错误信息的装饰器.

    :param allowLog: 是否运行记录错误到错误日志
    :type allowLog: bool
    :param leve: 错误级别(级别从低到高)
                 1.``debug``
                 2.``info``
                 3.``warning``
                 4.``error``
                 5.``critical``
    :type leve: int
    :param allowprint: 是否允许输出至控制台.(默认:True)
    :type allowprint: bool
    :param reserve: 是否保留前缀`Traceback (most recent call last):`.(默认:False)
    :type reserve: bool
    :param translate: 开启关键字翻译.(默认为True)
    :type translate: bool
    :param tranfin: 是否开启详细错误信息翻译.(默认为False)PS.时间开销极大
    :type tranfin: bool
    :param ErrorType: 拦截的错误类型,元组
    :type ErrorType: tuple[type[Exception]]
    :param WarningType: 拦截的警告类型,元组
    :type WarningType: tuple[type[Warning]]
    :return: 返回经装饰的原函数.
    :retype: Callable
    """

    def ignoregetfunc(func):
        @wraps(func)
        def ignorewrapper(*args, **kwargs):
            nonlocal ErrorType, WarningType
            ErrorType = ErrorType if ErrorType else ZeroDivisionError
            with catch_warnings(record=True) as warnings:
                simplefilter("ignore") if Warning in WarningType else None
                try:
                    return func(*args, **kwargs)  # 错误拦截器ignoreErrorAndWarning检测到错误
                except ErrorType:
                    pass
                if WarningType:
                    for awarn in warnings:
                        if awarn.category not in WarningType:
                            warn(awarn.message, awarn.category)

        if allowLog:
            ignorewrapper = errorLogger(leve, allowprint, reserve, translate, tranfin,
                                        mess=f"截取到错误 -> 位于文件:<{getmodule(func).__file__}>中的函数:<{func.__name__}>")(
                ignorewrapper)

        return ignorewrapper

    return ignoregetfunc


def debugInfo():
    fb = currentframe().f_back
    print(f"File {fb.f_code.co_filename}, line {fb.f_lineno}, in <{fb.f_code.co_name}>")


if __name__ == '__main__':
    pass
