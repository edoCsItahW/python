#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/7/26 23:48
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
from asyncio import new_event_loop, set_event_loop, wait
from threading import Thread
from asyncio.windows_events import ProactorEventLoop
from multiprocessing import freeze_support, Process
from confunc import splitList
from netTools.netTools import request
from logTools import *
import csv

logset()


class conCurrener:
    globals()['fin'] = []

    def __init__(self, aimlist: list, part: int):
        self.aimlist = aimlist
        self.part = part

    def run(self):
        self.createProcess(self.aimlist, self.part)

    @staticmethod
    @ignoreErrorAndWarning
    @errorLogger
    async def createAfunc(*, target=None, args=None):
        res = target(*args)
        with open(r"D:\xst_project_202212\Python\scatteredFile\test.csv", "a", encoding='gbk', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(res)
            # file.write(f"{str(res)}\n")
        print(res)

    @staticmethod
    @ignoreErrorAndWarning
    @errorLogger
    def createLoop():
        loop = new_event_loop()
        set_event_loop(loop)
        return loop

    @staticmethod
    @ignoreErrorAndWarning
    @errorLogger
    def runtask(aimlist: list, part: int, loop: ProactorEventLoop):
        async def inner_runtask():
            tasks = []
            for i in aimlist:
                tasks.append(conCurrener.createAfunc(target=gettan, args=(i,)))
            await wait(tasks)

        loop.run_until_complete(inner_runtask())

    @staticmethod
    @ignoreErrorAndWarning
    @errorLogger
    def createThread(aimlist: list, part: int):
        threads = []
        loop = conCurrener.createLoop()
        for i in splitList(aimlist, part):
            thread = Thread(target=conCurrener.runtask, args=(aimlist, part, loop,))
            threads.append(thread)
            thread.start()
        for athread in threads:
            athread.join()

    @staticmethod
    @ignoreErrorAndWarning
    @errorLogger
    def createProcess(aimlist: list, part: int):
        processes = []
        for i in splitList(aimlist, part):
            process = Process(target=conCurrener.createThread, args=(i, part,))
            processes.append(process)
            process.start()
        for aprocess in processes:
            aprocess.join()


@ignoreErrorAndWarning
@errorLogger
def gettan(word: str):
    backlist = [i['v'] for i in request(r"https://fanyi.baidu.com/sug", data={"kw": word}).getPostinfo().json['data'] if
                "人名" not in i['v']]
    backlist = backlist if backlist else ["无译意"]
    return [word] + backlist


if __name__ == '__main__':
    with open(r"C:\Users\Lenovo\Desktop\作业\哈利波特英文原著\哈利波特英文原著\set8.txt", 'r',
              encoding='utf-8') as text:
        telist = eval(text.read())
        freeze_support()
        con = conCurrener(telist, 10)
        con.run()
