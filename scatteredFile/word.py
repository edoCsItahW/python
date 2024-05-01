#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/17 8:18
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from ansiDefine.ansiDefine import ansiManger
from traceback import format_exc
from traceback import extract_tb
from textTools import isChinese
from datetime import date, datetime
from requests import ConnectTimeout
from netTools import request, translate_web, translate_single, translate_mutil
from sqlTools import baseSQL
from warnings import warn
from inspect import currentframe
from random import randint, shuffle, uniform
from typing import Callable, Annotated, Literal
from math import floor
from sys import exc_info
from os import PathLike


class distinguish:
    """
    英文近义词区分类

    :ivar __call__(): 调用时区分两个词汇的字母近似程度.
    :ivar keepLong(): 将两个单词中短的单词的长度补全至长的单词长度.
    """
    def __init__(self):
        self.letterList = list("abcdefghijklmnopqrstuvwxyz")
        self._test = False

    def __call__(self, word1: str, word2: str, *, rate: float = 0.6, debug: bool = False):
        self._test = debug
        if self._test: print(f"word: ({word1}, {word2})")
        word1, word2 = word1.lower(), word2.lower()

        lenDict = self.keepLong(word1, word2) if len(word1) != len(word2) else {"max": list(word1), "min": list(word2)}

        if self._test: print(f"lenDict: {lenDict}")

        compareList = self.compare(*lenDict.values())

        return self.determine(compareList, rate=rate if len(lenDict["min"]) / len(lenDict["max"]) > rate else 1)

    @staticmethod
    def keepLong(word1: str, word2: str):
        lenDirt = {len(word1): list(word1), len(word2): list(word2)}

        maxLen, minLen = max(lenDirt.keys()), min(lenDirt.keys())

        minList = [lenDirt[minLen][i] if i < minLen else "无" for i in range(maxLen)]

        return {"max": lenDirt[maxLen], "min": minList}

    @staticmethod
    def compare(wordList1: list, wordList2: list): return [a == b for a, b in zip(wordList1, wordList2)]

    @staticmethod
    def determine(compareList: list, *, rate: float = 0.7):
        if rate <= 0 or rate >= 1: raise ValueError("检测个数必须属于(0, 1)")

        boolDict = {True: False, False: True}

        unCompareList = [boolDict[i] for i in compareList]  # 反转bool值.

        if any(unCompareList[:floor(rate * len(unCompareList))]):
            return False
        else:
            return True


distinguish = distinguish()


def spilt(text: str, *args):
    for s in args:
        text = text.replace(s, "|")

    return text.split("|")


errorList = []


def errorLog(part: str, message: str = None, *, note: str = "", line: int = None, warnType=SyntaxWarning, _format: str = False, additional: str = ""):
    def getFunc(func: Callable):
        def warp(*args, **kwargs):
            nonlocal line, message
            try:
                return func(*args, **kwargs)
            except Exception as e:
                e.add_note(note)
                errorList.append(e)
                tb = extract_tb(exc_info()[2])

                for filename, lineon, funcname, code in tb:
                    if funcname == func.__name__:
                        message = code if message is None else message
                        line = lineon if line is None else line
                word.warn(part, message, func=func, line=line, warnType=SyntaxWarning, _format=_format, additional=additional)

        return warp

    return getFunc


class word:
    """
    单词背诵软件.

    :ivar sql: 数据库链接.
    :ivar color: 颜色管理器.
    :ivar logfile: 记录文件.
    :ivar allowColor: 是否允许输出颜色.
    :ivar cfile: 错误记录文件.
    :ivar _cn: 是否允许输出中文.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instancesSDS

    def __init__(self, dataBase: str = "userdata", tableName: str = "englishword", *,
                 logfile: str | PathLike = r"C:\Users\Lenovo\Desktop\文档集\txt\num.txt", correctFile: str | PathLike = r"C:\Users\Lenovo\Desktop\文档集\txt\incorrect_word.txt", allowColor: bool = True, CN: bool = True):
        """
        :param dataBase: 数据库名.
        :type dataBase: str
        :param tableName: 数据表名.
        :type tableName: str
        :keyword logfile: 最后页数记录文件.
        :type logfile: PathLike
        :keyword correctFile: 回答错误记录日志.
        :type correctFile: PathLike
        :keyword allowColor: 是否允许输出颜色字符.
        :type allowColor: bool
        :keyword CN: 是否为中文.
        :type CN: bool
        """
        self.sql = baseSQL("root", "135246qq", database=dataBase, tableName=tableName)
        self.color = ansiManger()
        self.logfile = logfile
        self.allowColor = allowColor
        self.cfile = correctFile
        self._cn = CN

    @property
    def _textDict(self) -> dict:
        """
        中英对照表.

        :return: 对应语言的字典
        :rtype: dict
        """

        textdict = {
                1:  ("Network not connected!: [network status]: {}", "网络未连接!: [网络状态]: {}"),
                2:  ("Frequent errors", "常错"),
                3:  ("Leve", "级别"),
                4:  ("Multiple errors", "较多错"),
                5:  ("Make fewer mistakes", "少错"),
                6:  ("Basic mastery", "基本掌握"),
                7:  ("The answer should be<{}>,Your answer<don't know>\n", "答案应为<{}>,你的答案为<不会>\n"),
                8:  ("Correct answer.\n", "答案正确.\n"),
                9:  ("The answer should be<{}>,Your answer<{}>\n", "答案应为<{}>,你的答案为<{}>\n"),
                10: ("(Review)", "(复习)"),
                11: ("{Review}{times}.Please write the corresponding translation of word<{w}>(quit to exit):", "{Review}{times}.请写出单词<{w}>对应的译意(quit退出):"),
                12: ("Leve: {}, accuracy: {:.2f}%", "级别: {}, 正确率: {:.2f}%"),
                13: ('Please enter the correct answer:{}', "请输入正确答案:{}"),
                14: ("Incorrect input'{}'.", "错误的输入'{}'."),
                15: ("Maybe you need to check your network.", "也许你需要检测你的网络."),
                16: ("check network", "检查网络"),
                17: ("UNKNOW!", "未知!")
            }

        return {k: v[1] for k, v in textdict.items()} if self._cn else {k: v[0] for k, v in textdict.items()}

    @staticmethod
    def warn(part: str, message: str = "UNKNOW!", *, func: Callable, line: int, warnType=SyntaxWarning, _format: bool | str = False, additional: str = ""):
        warn(f"\nLine: {line}, in <{func.__name__}>: {message.format(_format) if _format else message} <ADDITIONAL>: {additional}", warnType)

    def netWorkCheck(self):
        response = (instance := request("https://baidu.com")).getRuninfo()
        if instance.statusCode != 200:
            e = ConnectTimeout(self._textDict[1])
            e.add_note(tempText := self._textDict[15].format(instance.statusCode))
            errorList.append(e)
            self.warn(self._textDict[16], self._textDict[1], func=self.netWorkCheck, line=currentframe().f_lineno, additional=tempText)

    @errorLog("颜色开关")
    def colorSwitch(self, func: Callable, text: str, *, RGB: tuple | bool = None, ANSI: bool = ""):
        if not self.allowColor:
            return text

        return func(text, _ANSI=ANSI) if RGB is False else func(text, RGB=RGB)

    @errorLog("Id获取")
    def nowId(self, mode: Literal["R", "W"] = "R", *, num: int = 1):
        with open(self.logfile, "w" if mode == "W" else "r", encoding="utf-8") as file:
            if mode == "R":
                return int(file.read())
            else:
                file.write(str(num + 1))

    @errorLog("随机弹出")
    def randomPop(self, *, condition: str = "where id = index", begin: int = 1):
        """
        随机弹出单词.

        :param condition:
        :type condition:
        :param begin:
        :type begin:
        :return:
        :rtype:
        """
        try:
            logset = set()
            reslist = []

            while not reslist:
                index = randint(begin, self.sql.tableLen)

                if index not in logset:
                    logset.add(index)
                else:
                    continue

                if "index" in condition:
                    condition = condition.replace("index", str(index))

                reslist.append(res) if (
                    res := self.sql.selectColumn(columns=("*",), condition=condition, show=False)[0]) else None

            return reslist[0]

        except Exception as e:
            self.errorList.append(e)
            self.warn("pop word", func=self.randomPop, line=currentframe().f_lineno)

    @errorLog("抽取逻辑")
    def reviewPop(self, *, test: bool = False):
        """
        定义抽取逻辑.

        :param test: 测试模式
        :type test: bool
        :return:
        :rtype:
        """
        level = self._textDict[3]
        condition = None
        optionlist = []

        while not optionlist:
            randomNum = uniform(1, 10)

            if randomNum < 5.2:

                condition, level = "where riTimes / reTimes < 0.5", self.colorSwitch(self.color.f_red, self._textDict[2], RGB=False)

            elif 5.2 <= randomNum < 7.8:

                condition, level = "where riTimes / reTimes >= 0.5 AND riTimes / reTimes < 0.7", self.colorSwitch(self.color.f_otherColor, self._textDict[4], RGB=self.color.orange)

            elif 7.8 <= randomNum < 9.5:

                condition, level = "where riTimes / reTimes >= 0.7 AND riTimes / reTimes < 0.85", self.colorSwitch(self.color.f_yellow, self._textDict[5], RGB=False)

            elif 9.5 <= randomNum <= 10:

                condition, level = "where riTimes / reTimes >= 0.95 AND riTimes / reTimes < 1", self.colorSwitch(self.color.f_green, self._textDict[6], RGB=False)

            content = self.sql.randomChoice(condition=condition)

            if content:
                content = content[0]

                level = (level, content[-2] / content[-3])

                optionlist.append(content)

        return optionlist[0] + level

    @errorLog("顺序弹出")
    def orderPop(self):
        return self.sql.selectColumn(columns=("*",), condition=f"where id = {self.nowId()}", show=False)[0]

    @errorLog("更新数据")
    def updataInfo(self, aimword: str, *, right: bool = False, reView: bool = False):
        reTimes, riTimes, review = \
            self.sql.selectColumn(columns=("reTimes", "riTimes", "review"), condition=f"where word = '{aimword}'",
                                  show=False)[0]

        reTimes += 1
        riTimes += (1 if right else 0)
        review += (1 if reView else 0)

        self.sql.update(condition=f"where word = '{aimword}'", show=False, check=False, reTimes=reTimes,
                        riTimes=riTimes)

    @errorLog("结合选项")
    def combineOp(self, method: dict[Callable, int] = None):
        if method is None:
            method = {self.randomPop: 3, self.orderPop: 1}

        contentlist = sum([[f() for idx in range(i)] for f, i in method.items()], start=[])

        shuffle(contentlist)

        return contentlist

    def checkInput(self, text: str):
        pass

    @errorLog("检查答案")
    def checkAnswer(self, inp: str, answer: Annotated[tuple[str, str], "aimword: trans"], review: bool = False, *, test: bool = False):
        """TODO: 修缮无头浏览器模式"""
        aimword, tans = answer

        tranlist = [i for i in sum([spilt(i.lower(), ";", " ") for i in translate_single(inp)], start=[]) if i and i.isalpha() and i != " "]

        if not tranlist:
            tranlist = translate_web(inp, mutil=True)
            if not tranlist:
                tranlist = [translate_web, inp]

        print(f"{self.colorSwitch(self.color.f_otherColor, 'test', RGB=self.color.gold)}:\n\ttranList: {'n -> 不会' if inp.lower() == 'n' else tranlist}\n\tdetermineList: {(dList := [(aimword in i) or (distinguish(aimword, i)) for i in tranlist if i])}\n\ttranslate: {tans}") if test and inp.lower() != "quit" else None

        if inp.lower() == "quit":
            return None

        elif inp.lower() == "n":
            print(self.colorSwitch(self.color.f_systemRED, self._textDict[7].format(tans), RGB=False))

            try:
                with open(self.cfile, "a", encoding="utf-8") as file:
                    file.write(f"{aimword}: {tans}\n\t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} --- 你答错为:{inp}\n\n")
            except Exception as e:
                warn(format_exc(), SyntaxWarning)

            self.updataInfo(aimword, right=False, reView=review)

            return False

        elif inp in tans.replace("…", "") or aimword in tranlist or any(dList):
            print(self.colorSwitch(self.color.f_green, self._textDict[8], RGB=False))

            self.updataInfo(aimword, right=True, reView=review)

            return True

        else:
            print(self.colorSwitch(self.color.f_systemRED, self._textDict[9].format(tans, inp), RGB=False))

            try:
                with open(self.cfile, "a", encoding="utf-8") as file:
                    file.write(f"{aimword}: {tans}\n\t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} --- 你答错为:{inp}\n\n")
            except Exception as e:
                warn(format_exc(), SyntaxWarning)

            self.updataInfo(aimword, right=False, reView=review)

            return False

    def choice_CN(self):
        pass

    def choice_EN(self):
        pass

    @errorLog("文字输出")
    def write_CN(self, times: int, *, order: bool = True, review: bool = True, test: bool = False):
        content = self.orderPop() if order else self.randomPop()

        if review:
            content = self.reviewPop(test=test)

        idx, aimword, trans, level, rate = content[0], content[1], content[2], content[-2], content[-1]

        print(self._textDict[11].format(
            Review=self.colorSwitch(self.color.f_purple, self._textDict[10], RGB=False) if review else '',
            times=self.colorSwitch(self.color.f_otherColor, times, RGB=self.color.sandybrown),
            w=self.colorSwitch(self.color.f_systemBULE, aimword, RGB=False, ANSI=self.color.b_wide)
        ))
        print(self._textDict[12].format(level, rate * 100)) if test and review else None

        while (not (inp := input(self._textDict[13].format(self.color.hotpink if self.allowColor else ""))) or any(
                [not isChinese(i) for i in inp])) and inp.lower() != "quit" and inp.lower() != "n":
            print(self.colorSwitch(self.color.f_yellow, self._textDict[14].format(inp), RGB=False))

        print(self.color.end, end="") if self.allowColor else None

        res = self.checkAnswer(inp, (aimword, trans), review=review, test=test)

        if order and res is not None and not review:
            self.nowId(mode="W", num=idx)

        return (aimword, trans) if res is False else res

    def write_EN(self):
        pass

    @errorLog("主程序")
    def main(self, mode: Literal["WCN"] = "WCN", *, order: bool = True, review: bool = True, test: bool = False):
        self.netWorkCheck()

        logdict = {}
        times = self.nowId()

        while True:
            # 复习数量定义处
            res = self.write_CN(times, order=order, review=review if (times // 5) % 5 == 0 else False, test=test)

            if res is None:
                break
            elif isinstance(res, tuple):
                logdict.update([res])

            times += 1

        for k, v in logdict.items():
            print(f"{k}:\t{v}\n")

        print(" Bye ")

        if errorList:
            raise ExceptionGroup("结尾记录", errorList)


if __name__ == '__main__':
    ins = word(allowColor=input("allowColor?:") in ("y", "Y", ""), CN=input("CN?:") in ("y", "Y", ""))
    ins.main(test=input("test?:") in ("y", "Y", ""))
    input("any key to quit.")
    # executor.sql.to_csv(r"C:\Users\Lenovo\Desktop\cWordLog.csv", "englishword", condition="where reTimes > riTimes")
    # executor.sql.selectColumn(columns=('*',), condition="where word = 'communicate'")
    # ins.sql.update(condition="where word = 'CE'", tran="abbr.基督纪元,公元(表示日期时用法同AD);英国国教会;英格兰圣公会")
