#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/3/4 23:16
# 当前项目名: PyPi项目源
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait as pwait
from multiprocessing import Process, cpu_count, current_process
from functools import cache, wraps
from traceback import format_exc
from logTools import ignoreErrorAndWarning
from warnings import warn
from asyncio import new_event_loop, set_event_loop, wait, AbstractEventLoop, gather, get_event_loop
from inspect import isfunction, isclass, ismethod, isbuiltin
from typing import Callable, Iterable
from os import getpid

try:
    from ANSIdefine.ansiDefine import ansiManger
except Exception:
    from ansiDefine.ansiDefine import ansiManger

__all__ = [
    "IOmanger",
    "finish",
    "running",
    "parallel",
]

color = ansiManger()


class IOmanger:
    def __init__(self, cla, taskList: list, forpart: tuple = (10, 14,)):
        self.tasksList = taskList
        self.part = forpart
        self.cla = cla()
        self.button = []

    @ignoreErrorAndWarning(False, ErrorType=(RuntimeError, AssertionError,), WarningType=(RuntimeWarning,))
    async def runAimfunc(self, mess, arg):
        res = self.cla.finDo(mess)
        self.button.append(res)

    @staticmethod
    @ignoreErrorAndWarning(False, ErrorType=(RuntimeError, AssertionError,), WarningType=(RuntimeWarning,))
    def createLoop():
        loop = new_event_loop()
        set_event_loop(loop)
        return loop

    @ignoreErrorAndWarning(False, ErrorType=(RuntimeError, AssertionError,), WarningType=(RuntimeWarning,))
    def _runTask(self, messlist, loop: AbstractEventLoop, arg):
        messlist = self.cla.taskDo(messlist, arg)

        async def inner_runtask():
            tasks = [self.runAimfunc(mess, arg) for mess in messlist] if len(messlist) != 1 else messlist
            await wait(tasks)

        loop.run_until_complete(inner_runtask())

    @ignoreErrorAndWarning(False, ErrorType=(RuntimeError, AssertionError,), WarningType=(RuntimeWarning,))
    def createThread(self, messlist, arg):
        from conFunc import splitList
        times = self.part[1]
        before = splitList(self.cla.threadDo(messlist, arg), times) if len(messlist) >= times else messlist
        loop = self.createLoop()
        with ThreadPoolExecutor(max_workers=14) as executor:
            threads = [executor.submit(self._runTask, partlist, loop, self.cla.threadarg, ) for partlist in before]
            # for athread in as_completed(threads):
            #     res = athread.result()
            #     print(res)

    @ignoreErrorAndWarning(False, ErrorType=(RuntimeError, AssertionError,), WarningType=(RuntimeWarning,))
    def createProcess(self, messList, arg):
        from conFunc import splitList
        before = splitList(self.cla.processDo(messList, arg), self.part[0])
        with ProcessPoolExecutor(max_workers=10) as executor:
            processes = [executor.submit(self.createThread, partlist, self.cla.processarg, ) for partlist in before]
            # for aprocess in as_completed(processes):
            #     res = aprocess.result()
            #     print(res)

    @ignoreErrorAndWarning(False, ErrorType=(RuntimeError, AssertionError,), WarningType=(RuntimeWarning,))
    def beginRun(self, messList):
        before = self.cla.initList(messList)
        self.createProcess(before, self.cla.initarg)


def running(cls: type, alist: list, forpart: tuple = (10, 14,)):
    woker = IOmanger(cls, alist, forpart)
    woker.beginRun(alist)


def finish(func: Callable, params: list, *, max_worker: int = 10):
    processes = []
    for param in params:
        process = Process(target=func, args=(*param,))
        processes.append(process)
        process.start()
        if len(processes) > max_worker:
            processes.pop(0).join()
    for aprocess in processes:
        aprocess.join()


def processName(): return current_process().name


def tryFunc(realTrack: bool = True):
    def getfunc(func: Callable):
        @wraps(func)
        def wapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                warn("\n" + format_exc() if realTrack else f"Traceback (most recent call last):\n"
                     f"  File \"{__file__}\", line {e.__traceback__.tb_lineno}, in <{func.__name__}>\n"
                     f"\targs: {args}\n"
                     f"\tkwargs: {kwargs}\n"
                     f"{type(e).__name__}: {e}\n", SyntaxWarning)

        return wapper

    return getfunc


class parallel:
    def __init__(self, *, test: bool = False, Try: bool = True):
        self._test = test

    def _splitList(self, __L: list, firstLayer: int = None):

        if firstLayer is None:
            firstLayer = self.cpuCount

    @staticmethod
    def _checkParam(param) -> bool: return isfunction(param) or isclass(param) or ismethod(param) or isbuiltin(param)

    @property
    @cache
    def cpuCount(self): return cpu_count()

    def P_T_IO(self, __I: Iterable, func: Callable = print):
        self.processDo(
            self.threadDo,
            [(self.createLoop, [(self.asyncDo, func, l) for l in alist]) for alist in __I]
        )

    @tryFunc()
    def processDo(self, func: Callable, __I: Iterable, *, worker: int = None):
        """
        processDo(func, __I)
        """

        if worker is None:
            worker = self.cpuCount - 4

        print(f"ProcessDo: <{processName()}: {getpid()}>\n"
              f"func: {func.__name__}\n"
              f"__I: {[arg.__name__ if self._checkParam(arg) else arg for arg in (__I[0] if len(__I[0]) and isinstance(__I[0], Iterable) else __I)]}\n\n") if self._test else None

        if not isinstance(__I[0], tuple):
            warn(f"由于参数需要传入元组以解包,而你的参数:{__I[0]}非元组,我们将该参数修改({__I[0]}, )", SyntaxWarning)
            __I = [(i, ) for i in __I]

        with ProcessPoolExecutor(max_workers=worker) as executor:
            pwait([executor.submit(func, *arg) for arg in __I])

    @tryFunc()
    def threadDo(self, func: Callable, __I: Iterable, *, worker: int = 14):
        """
        processDo(threadDo, __I[(func, __I), ...]])
        """
        print(f"ThreadDo: <{processName()}: {getpid()}>\n"
              f"func: {func.__name__}\n"
              f"__I: {[arg.__name__ if self._checkParam(arg) else arg for arg in (__I[0] if len(__I[0]) and isinstance(__I[0], Iterable) else __I)]}\n\n") if self._test else None
        with ThreadPoolExecutor(max_workers=worker) as executor:
            pwait([executor.submit(func, *arg) for arg in __I])

    @tryFunc()
    def createLoop(self, func: Callable, *args):
        """
        processDo(threadDo, __I[(createLoop, __I[(asyncDO, func, __I), ]), ...])
        """
        print(f"CreateLoop:\n"
              f"func: {func.__name__}\n"
              f"args: {[arg.__name__ if self._checkParam(arg) else arg for arg in args]}\n\n") if self._test else None
        loop = new_event_loop()
        loop.run_until_complete(func(*args))

    async def asyncDo(self, func: Callable, __I: Iterable):
        print(f"AsyncDo:\n"
              f"func: {func.__name__}\n"
              f"__I: {__I}  # __I should be like [[1, 2], [3, 4]]\n\n") if self._test else None
        return gather(*[get_event_loop().run_in_executor(None, func, *arg) for arg in __I])


if __name__ == '__main__':
    ins = parallel(test=True)
    ins.P_T_IO([
        [
            [
                ["1", "2"],
                ["3", "4"]
            ],
            [
                ["5", "6"],
                ["7", "8"]
            ]
        ],
        [
            [
                ["9", "10"],
                ["11", "12"]
            ],
            [
                ["13", "14"],
                ["15", "16"]
            ]
        ]
    ])
    pass

