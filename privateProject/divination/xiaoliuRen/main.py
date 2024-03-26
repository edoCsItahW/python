#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/1/13 23:25
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from pandas import DataFrame
from privateProject.divination.xiaoliuRen.elementDefine import ebList, sixPalace, sixGodLead, ebLead
from matplotlib.pyplot import subplots, tight_layout, show, rcParams


class board:
    _board = DataFrame({k: (ebList[v * 2:] + ebList[:v * 2]) for v, k in enumerate(sixPalace)})

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __getitem__(self, index: int):
        if index <= 0:
            raise ValueError(
                f"索引只能大于0"
            )

        row, column = index // 6, index % 6
        return self._board.loc[row if column else row - 1][column - 1], sixPalace[column - 1]

    def row(self, index: int, *, loc: bool = False):
        if loc:
            return list(self._board.iloc[index])

        row, column = index // 6, index % 6
        return list(self._board.loc[row if column else row - 1])

    def column(self, index: int, *, loc: bool = False):
        if loc:
            return list(self._board.iloc[:, index])

        row, column = index // 6, index % 6
        return list(self._board.iloc[:, column - 1])


class engine:
    def __init__(self):
        self._board = board()
        self._ke = {"六神": None, "五星": None, "六宫": None, "地支": None, "六亲": None, "时日": ""}
        self.keList = {}

    def sortBoard(self, dayNum: int, time: int):
        sixPrentDict = {"相同": "兄弟", "我克": "妻财", "我生": "子孙", "克我": "官鬼", "生我": "父母"}

        dayEB, dayPalace = self._board[dayNum]
        dayPidx = sixPalace.index(dayPalace)
        startDict = {k: v for k, v in zip(sixPalace[dayPidx:] + sixPalace[:dayPidx], ["木星", "火星", "土星", "金星", "水星", "天空"])}

        timeEB, timePalace = self._board[dayNum + time - 1]

        timeOEB = self._board.row(self._board.column(dayNum + time - 1).index(ebList[time - 1]), loc=True)

        for eb, palace in zip(timeOEB, sixPalace):
            self.keList.update([(eb, {"六神": sixGodLead()[eb], "五星": startDict[palace], "六宫": palace, "六亲": '自身' if eb == ebList[time - 1] else sixPrentDict[ebLead()[ebList[time - 1]].relation(ebLead()[eb])], "时日": "日" if eb == dayEB else "时" if eb == ebList[time - 1] else ""})])

    def showBoard(self):
        fig, axs = subplots(2, 3, figsize=(8, 8))

        rcParams['font.sans-serif'] = ['Microsoft YaHei']

        kList = list(self.keList.keys())

        for i in range(2):
            for j in range(3):
                ax = axs[i, j]
                ax.set_xlim(0, 10)
                ax.set_ylim(0, 10)
                ax.set_xticks([])
                ax.set_yticks([])

                infoDict = self.keList[kList[i * 3 + j]]

                ax.text(1, 1, f'{infoDict["时日"]}', ha='left', va='bottom', fontsize=20)
                ax.text(1, 9, f'{infoDict["六神"]}', ha='left', va='top', fontsize=20)
                ax.text(9, 4.5, f'{infoDict["六亲"]}', ha='right', va='center', fontsize=20)
                ax.text(1, 4.5, f'{kList[i * 3 + j]}', ha='left', va='center', fontsize=20)
                ax.text(9, 1, f'{infoDict["六宫"]}', ha='right', va='bottom', fontsize=20)
                ax.text(9, 9, f'{infoDict["五星"]}', ha='right', va='top', fontsize=20)

        tight_layout(pad=0)
        show()


if __name__ == '__main__':
    ins = engine()
    ins.sortBoard(28, 6)
    ins.showBoard()
