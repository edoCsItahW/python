#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/31 下午8:05
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from abc import ABC, abstractmethod
from typing import Callable, Any, final
from atexit import register
from time import sleep
from multiprocessing import Process, Queue as pQueue, Pipe, Lock, Manager
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, as_completed
from itertools import islice
from threading import Thread
from asyncio import run, create_task, wait as asyncwait


__all__ = [
    'ConcurrentFrame',
    'QueueError',
    'QueueEmptyError'
]


def chunkList(lst, n):
    divisor, extra = len(lst) // n, len(lst) % n

    start = 0

    for _ in range(n):
        end = start + divisor
        if extra > 0:
            end += 1
            extra -= 1
        yield list(islice(lst, start, end))
        start = end


class QueueError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class QueueEmptyError(QueueError):
    def __init__(self, *args):
        super().__init__(*args)


class ConcurrentFrame(ABC):
    @final
    def __init__(self, maxWorkers: int = 10):
        self._maxWorkers = maxWorkers
        self._inQueue = Manager().Queue()
        self._outQueue = Manager().Queue()

    @final
    @property
    def maxWorkers(self):
        return self._maxWorkers

    @final
    @property
    def inQueue(self):
        return self._inQueue

    def provide(self, data: Any):
        self.inQueue.put(data)

    @staticmethod
    def tMiddleware(data: Any, outQueue):
        outQueue.put(data)

    # @staticmethod
    # def asyncMiddleware(*args, **kwargs):
    #     return args, kwargs
    #
    # @final
    # def _runTask(self, *args, **kwargs):
    #     async def inner():
    #         await asyncwait([create_task(self.asyncMiddleware(*args, **kwargs))])
    #
    #
    # @final
    # def runTask(self, *args, **kwargs):
    #     run(self._runTask(*args, **kwargs))

    @staticmethod
    @abstractmethod
    def threadDo(threadId: int, data: Any):
        print(f"Thread-{threadId}: '{data}'")
        sleep(1)

    @final
    def _threadDo(self, threadId: int):
        def provide():
            if self._outQueue.qsize() <= 2:
                self.tMiddleware(self.inQueue.get(), self._outQueue)

        thread = Thread(target=provide)

        while True:

            # if self._outQueue.qsize() <= 2:
            #     self.tMiddleware(self.inQueue.get(), self._outQueue)
            thread.start()

            while not self._outQueue.empty():
                self.threadDo(threadId, self._outQueue.get())

    @staticmethod
    def pMiddleware(inQueue, data: Any):
        inQueue.put(data)

    @final
    def _processDo(self, datas: list = None):

        if datas is not None:
            for data in datas:
                self.pMiddleware(self.inQueue, data)

        with ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
            wait([executor.submit(self._threadDo, i) for i in range(self.maxWorkers)])

    @final
    def run(self, datas: list = None):
        if not datas and self.inQueue.empty():
            raise QueueEmptyError(
                "队列为空，请先提供数据!")

        if datas is not None:
            datas = list(chunkList(datas, self.maxWorkers))

        with ProcessPoolExecutor(max_workers=self.maxWorkers) as executor:
            wait([executor.submit(self._processDo, datas[i] or None) for i in range(self.maxWorkers)])


if __name__ == '__main__':
    # cf = ConcurrentFrame()
    # for i in range(1000):
    #     cf.provide(i)
    #
    # cf.run()
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in islice(a, 10):
        print(i)
