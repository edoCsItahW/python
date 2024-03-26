#! /usr/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/11 15:13
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
from netTools.netTools import translate_single  # , request
# from time import sleep
from functools import cached_property
from random import choices, randint
# from pandas import DataFrame
from typing import Literal  # , Callable
from time import sleep


# from csv import writer, reader

r"""
    def checkTB(self):
        res = self.sql.showTableContent(show=False)

        with open(r"C:\Users\Lenovo\Desktop\numlog.txt", "r", encoding="utf-8") as file:
            start = int(file.read())

        for L in res[start:]:
            print(f"{L[0]}.单词{L[1]}:")
            for i, v in enumerate(reallist := list(filter(lambda x: True if x else False, L[2:-2])), 1):
                print(f"\t{i}.{v}")

            while True:
                checklist = []
                inp = input("选择保留(保留全部all,quit退出):")
                if inp.lower() == "all" or inp.lower() == "quit":
                    break
                for w in inp.split(","):
                    if w not in ["1", "2", "3", "4", "5"][:len(reallist)]:
                        None if checklist else print(f_yellow(f"错误的输入'{inp}'"))
                        checklist.append(1)

                if len(checklist) == 0:
                    break

            if inp.lower() == "quit":
                exit("用户手动退出.")
            elif inp.lower() == "all":
                start += 1
            else:
                updatadict = {f"tran{i}": None for i in range(1, 6)}
                for i, w in enumerate(inp.split(","), 1):
                    updatadict[f"tran{i}"] = toEnglish(reallist[int(w) - 1].replace(" ", ""))

                self.sql.update(condition=f"where id = {L[0]}", show=False, check=False, **updatadict)

                start += 1

            with open(r"C:\Users\Lenovo\Desktop\numlog.txt", "w", encoding="utf-8") as file:
                file.write(str(start))
"""
r"""
    def writeIn(self, wordlist: list, *, reTimes: int = None, riTimes: int = None):
        if reTimes is None:
            reTimes = 0
        if riTimes is None:
            riTimes = 0

        keylist = ["word", "tran"]

        if len(wordlist) < len(keylist):
            warn("输入的长度不符合预期长度,缺失处将以NULL填充.", SyntaxWarning)

            wordlist += [""] * (len(keylist) - len(wordlist))

        else:
            raise ValueError("输入的长度超过预期长度.")

        keydict = {k: v for k, v in zip(keylist, wordlist)}
        keydict.update([("reTimes", reTimes), ("riTimes", riTimes)])

        self.sql.insert(**keydict)
"""
r"""
    def addWord(self, **kwargs):
        loglist = []
        wordlist = self.sql.showTableContent(show=False)
        lastlist = wordlist[-1]
        times = lastlist[0]

        def getword(Times: int = times, *, mod: int = 1):
            while True:
                if mod == 1:
                    Inp = input(
                        f"{Times + 1}.上一个单词是<{loglist[-1] if loglist else lastlist[1]}>,请输入下一个输入单词(quit退出,mod修改):")
                else:
                    Inp = input(f"你在修改第{Times}个,请输入单词:")

                if any([w and (w.isdigit() or isChinese(w)) for w in Inp]):
                    print(f_yellow(f"输入的单词格式不正确,你的输入{Inp}"))
                    continue
                else:
                    return Inp, Times

        while True:
            inp, times = getword(times)
            wordtran = untran(inp)

            if inp.lower() == "quit":
                return
            elif inp.lower() == "mod":
                if (i := input("输入last修改上一个,输入数字以选择修改:")) == "last":
                    last = self.sql.selectColumn(columns=("word", "tran"), condition=f"where id = {times}", show=False)
                    if input(f_yellow(f"第{times}个是{last[0]},你确定修改吗(Y/N)")).lower() == "y":
                        word, _ = getword(times, mod=2)
                        self.sql.update(condition=f"where id = {times}", show=False, check=False, word=word,
                                        tran=toEnglish(untran(word)[0]).replace(" ", ""))
                        loglist[-1] = word
                    continue
                elif i.isdigit():
                    last = self.sql.selectColumn(columns=("word", "tran"), condition=f"where id = {int(i)}", show=False)
                    if input(f_yellow(f"第{times}个是{last[0]},你确定修改吗(Y/N)")).lower() == "y":
                        word, _ = getword(times, mod=2)
                        self.sql.update(condition=f"where id = {times}", show=False, check=False, word=word,
                                        tran=toEnglish(untran(word)[0]).replace(" ", ""))
                    continue

            if not wordtran:
                print(f_yellow("你的上一个单词翻译失败,是否重新输入(Y/N):"), end="")
                sleep(0.5)
                if input().lower() == "y":
                    continue

            times += 1
            self.sql.insert(show=False, word=inp, tran=toEnglish(wordtran[0]).replace(" ", ""))
            loglist.append(inp)
"""


class Tran:
    """
    单词辅助背诵工具.

    Attributes:
        dbName: 数据库名.
        tbName: 数据表名.
        sql: 高层数据库接口.

    Methods:
        ramdomPop(): 方法职能.
    """
    def __init__(self, dbName: str, tbName: str):
        self.dbName = dbName
        self.tbName = tbName
        self.sql = baseSQL(database=dbName, tableName=tbName)

    @cached_property
    def tbLen(self):
        return len(self.sql.showTableContent(show=False))

    # 主模块部件
    def randomPop(self, *, firstNum: int = 1) -> list[tuple[int, str, str, int, int, int, int]]:
        """
        随机弹出一条数据

        :param firstNum: 开头索引(由于数据库的自增键索引没有0,所有该值通常为1).
        :type firstNum: int
        :return: 一条数据
        :retype: list[tuple[]]
        :raises ValueError: 当firstNum<=0时会主动抛出ValueError.
        """

        if firstNum <= 0: raise ValueError(f"firstNum通常为大于0的整数,而你的输入'{firstNum}'")

        return self.sql.selectColumn(columns=("*",), condition=f"where id = {randint(firstNum, self.tbLen)}", show=False)

    # 主模块部件
    def checkPop(self, *, firstNum: int = 1, onlyE: bool = False):
        while True:
            poplist = self.randomPop(firstNum=firstNum)[0]

            ratedict = {0: 10, 1: 6, 2: 3, 3: 1, 4: 0}

            r = randint(1, 10)

            keynum = poplist[-2]

            if keynum != 0 and poplist[-1] / poplist[-2] >= 0.8:
                if keynum in ratedict and r <= ratedict[keynum]:
                    if onlyE:
                        if poplist[-2] > poplist[-1]:
                            return poplist
                    return poplist
            else:
                if onlyE:
                    if poplist[-2] > poplist[-1]:
                        return poplist
                return poplist

    # 主模块部件
    def updataInfo(self, word: str, *, right: bool = False):
        reTimes, riTimes = self.sql.selectColumn(columns=("reTimes", "riTimes"), condition=f"where word = '{word}'",
                                                 show=False)[0]

        reTimes += 1
        riTimes += 1 if right else 0

        self.sql.update(condition=f"where word = '{word}'", show=False, check=False, reTimes=reTimes, riTimes=riTimes)

    # 主模块部件
    def structure_option_dict(self, *, onlyE: bool = False):
        optionlist = []

        while len(optionlist) < 4:
            optionlist.append(
                option if (option := self.checkPop(onlyE=onlyE)) not in optionlist else self.checkPop(onlyE=onlyE)
            )

        return {k: v for k, v in zip(["A", "B", "C", "D"], optionlist)}

    # 主模块部件
    @staticmethod
    def obtain_now_number(fileName: str):
        with open(fileName, "r") as file:
            return int(file.read())

    # 主模块部件
    @staticmethod
    def checkInput(mode: str, text: str):
        if mode == "W" or mode == "RE":

            while (((not (inp := input(text + '请输入正确答案:')) or
                     any([(i not in letterlist_l + [" "]) if mode == "W" else (not isChinese(i)) for i in inp])))
                   and inp.lower() != "quit" and inp.lower() != "n"):
                print(f_yellow(f"错误的输入'{inp}'."))

        else:

            while (inp := input(text + '请输入正确答案:')).upper() not in ["A", "B", "C", "D", "N", "QUIT"]:
                print(f_yellow(f"错误的输入'{inp}'."))

        return inp

    # 主模块部件
    @staticmethod
    def textMode(mode: str, optiondict: dict, times: int, param: tuple[str, str]):
        aimword, trans = param

        if mode == "EN":

            text = f"{times}.单词{f_systemBULE(aimword, _ANSI=b_wide)}的译意是(quit退出):\n"

            for t in optiondict:
                text += f"\t{f_green(t)}.{optiondict[t][2]}\n"

        elif mode == "W":

            text = f"{times}.请写出译意<{f_systemBULE(trans, _ANSI=b_wide)}>对应的单词(quit退出):\n"

        elif mode == "RE":

            text = f"{times}.请写出单词<{f_systemBULE(aimword, _ANSI=b_wide)}>对应的译意(quit退出):\n"

        else:

            text = f"{times}.译意<{f_systemBULE(trans, _ANSI=b_wide)}>对应的单词是(quit退出):\n"

            for t in optiondict:
                text += f"\t{f_green(t)}.{optiondict[t][1]}\n "

        return text

    def checkAnswer(self, inp: str, mode: str, param: tuple, optiondict: dict, otherParam: tuple, *, reWrite: bool):
        rightKey, aimword, trans = param
        incorrectlist, rightnum = otherParam

        if inp.lower() == "quit":
            return incorrectlist, rightnum, False

        elif inp.lower() == "n":

            temPrint(f"正确答案为:{f_yellow(aimword)}") if reWrite and mode == "W" else print(f_systemRED(
                f"正确答案为:{aimword}" if mode == "W" else f"正确答案为[{aimword}: -> {rightKey}.{trans}]"))

            self.updataInfo(aimword)

            incorrectlist.append([{aimword: trans}, "不会"] if mode == "W" or mode == "RE" else [{aimword: trans}, {"N": "不会"}])

            if reWrite and mode == "W":
                sleep(5)
                temPrint("")

                print(
                    f_green("第二次回答正确") if input("请再此输入:") == aimword else f_systemRED("第二次回答错误"))

        elif inp.upper() == rightKey or (mode == "W" and inp.lower() == aimword) or (
                mode == "RE" and (
                aimword in (tranlist := translate_single(inp)) or any([aimword in i for i in tranlist if i]) or inp in trans)
        ):

            print(f_green("答案正确."))

            self.updataInfo(aimword, right=True)

            rightnum += 1

        else:

            temPrint(f"正确答案为:{f_yellow(aimword)}") if reWrite and mode == "W" else print(f_systemRED(
                f"正确答案为:{aimword if mode == 'W' else trans}"
                if mode == "W" or mode == "RE" else
                f"答案错误,正确答案为[{aimword}: -> {rightKey}.{trans}],你的答案为{inp.upper()}"))

            self.updataInfo(aimword)

            intrans = None if mode == "W" or mode == "RE" else optiondict[inp.upper()]

            incorrectlist.append(
                [{aimword: trans}, inp.lower() if mode == "RE" else inp]
                if mode == "W" or mode == "RE" else [{aimword: trans}, {intrans[1]: intrans[2]}]
            )

            if reWrite and mode == "W":
                sleep(5)
                temPrint("")

                print(f_green("第二次回答正确") if input("请再此输入:") == aimword else f_systemRED("第二次回答错误"))

        return incorrectlist, rightnum, True

    def learn(self, *, mod: Literal["CN", "EN", "RE", "W"] = "EN", order: bool = False, reWrite: bool = True,
              onlyE: bool = False) -> None:
        """
        主方法,运行以开始学习.

        :param mod: 学习模式,{
            **CN: 根据中文翻译选择英文.
            EN: 根据英文选择中文.
            RE: 在没有任何提示的情况下写出单词的中文译意.
            W: 根据中文译意写出单词.**}
        :type mod: str
        :param order: 是否按照顺序开始学习.
        :type order: bool
        :param reWrite: 是否运行写错后再次根据提示再次回答. *(PS.仅在`RE` , `W`模式下)*
        :type reWrite: bool
        :param onlyE: 是否只抽取答错错过的单词.
        :type onlyE: bool
        :return: 操作执行函数不做返回.
        :rtype: None
        :raise ValueError: 当模式为`CN`或`EN`且检测到reWrite的值为 **True** 时抛出ValueError错误.
        """

        times = 1  # 答题次数
        rightnum = 0  # 回答正确次数
        incorrectlist = []  # 错误列表

        num = 0

        while True:

            optiondict = self.structure_option_dict(onlyE=onlyE)

            rightKey = choices(list(optiondict.keys()))[0]  # 正确选项

            if order:
                num = self.obtain_now_number(r"C:\Users\Lenovo\Desktop\num.txt")  # 获取当前学习到的序号

                optiondict[rightKey] = list(optiondict[rightKey])  # 格式化选项的

                # 将选项列表中的正确项的内容更改为正确的内容.
                optiondict[rightKey][1], optiondict[rightKey][2] = self.sql.selectColumn(columns=("word", "tran"), condition=f"where id = {num}", show=False)[0]

            aimword, trans = optiondict[rightKey][1], optiondict[rightKey][2]  # 正确的选项对应的单词和翻译

            text = self.textMode(mod, optiondict, times, (aimword, trans))  # 获取题目开头的文本

            inp = self.checkInput(mod, text)  # 通过逻辑检查获取输入的选项或单词

            incorrectlist, rightnum, flags = self.checkAnswer(inp, mod, (rightKey, aimword, trans), optiondict, (incorrectlist, rightnum), reWrite=reWrite)

            if not flags: break

            times += 1

            if order:
                with open(r"C:\Users\Lenovo\Desktop\num.txt", "w") as file:
                    file.write(str(num + 1))

        print(f"正确率:{0 if times == 1 else (rightnum / (times - 1) * 100):.2f}%.")

        if incorrectlist:

            print("答错的单词有:")

            for word in incorrectlist:
                print(f"{word[0]}\n你答错为:{f_systemRED(word[1])}")
        else:
            print("全部正确.")
#: todo: (10.14) add a review mueddle


if __name__ == '__main__':
    app = Tran("userdata", "englishword")
    app.learn(mod="RE", order=True, reWrite=True, onlyE=False)
    # sql.update(reTimes=0, riTimes=0)
    # res = app.sql.showTableContent()
    # app.sql.selectColumn(columns=("*",), condition="where riTimes < reTimes")
    # sql.to_csv(r"C:\Users\Lenovo\Desktop\文档集\sorceRecord.csv", "englishword")
