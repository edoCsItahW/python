#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/2/13 14:07
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from random import randint
from matplotlib.pyplot import subplots, show
from matplotlib.patches import Rectangle


class gua:
    def __new__(cls, key: str):
        return

    @property
    def guaCiDict(self):
        gua_dict = {
            "乾为天": self.quanWeiTian(),
            "坤为地": self.kunWeiDi(),
            "水雷屯": self.shuiLeiTun(),
            "善水蒙": self.shangShuiMeng(),
            "水天需": self.shuiTianXv(),
            "天水淞": self.tianShuiSong(),
            "地水师": self.diShuiShi(),
            "水地比": self.shuiDiBi(),
            "风天小蓄": self.fengTianXiaoXv(),
            "天泽履": self.tianZeLv(),
            "地天泰": self.diTianTai(),
            "天地否": self.tianDiFou(),
            "天火同人": self.tianHuoTongRen(),
            "火天大有": self.huoTianDaYou(),
            "地山谦": self.diShangQian(),
            "雷地豫": self.leiDiYv(),
            "泽雷随": self.zeLeiSui(),
            "山风蛊": self.shangFengGu()
        }
        return gua_dict

    @staticmethod
    def quanWeiTian():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4103.html"
        return text

    @staticmethod
    def kunWeiDi():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4105.html"
        return text

    @staticmethod
    def shuiLeiTun():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4106.html"
        return text

    @staticmethod
    def shangShuiMeng():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4107.html"
        return text

    @staticmethod
    def shuiTianXv():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4108.html"
        return text

    @staticmethod
    def tianShuiSong():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4109.html"
        return text

    @staticmethod
    def diShuiShi():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4110.html"
        return text

    @staticmethod
    def shuiDiBi():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4111.html"
        return text

    @staticmethod
    def fengTianXiaoXv():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4112.html"
        return text

    @staticmethod
    def tianZeLv():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4113.html"
        return text

    @staticmethod
    def diTianTai():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4126.html"
        return text

    @staticmethod
    def tianDiFou():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4127.html"
        return text

    @staticmethod
    def tianHuoTongRen():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4140.html"
        return text

    @staticmethod
    def huoTianDaYou():
        text = "https://www.k366.com/gua/14.htm"
        return text

    @staticmethod
    def diShangQian():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4142.html"
        return text

    @staticmethod
    def leiDiYv():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4143.html"
        return text

    @staticmethod
    def zeLeiSui():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4144.html"
        return text

    @staticmethod
    def shangFengGu():
        text = "https://www.zhouyi.cc/zhouyi/yijing64/4145.html"
        return text


class engine:
    def __init__(self):
        self._picRange = 1

    @property
    def guaDict(self):
        _dict = {
            "111": "乾",
            "011": "巽",
            "001": "艮",
            "000": "坤",
            "100": "震",
            "110": "兑",
            "101": "离",
            "010": "坎"
        }
        return _dict

    @staticmethod
    def getYao():
        return randint(0, 1)

    @property
    def guaCi(self):
        pass

    def drowYao(self):
        yao_list = []

        fig, ax = subplots()

        step = self._picRange / 13
        rate = 0.5 / 3
        start = 0.5 / 2

        for rect in range(1, 13, 2):
            if sym := self.getYao():
                ax.add_patch(Rectangle((start, rect * step), 0.5, step, color='black'))
            else:
                ax.add_patch(Rectangle((start, rect * step), rate, step, color='black'))
                ax.add_patch(Rectangle((start + 2 * rate, rect * step), rate, step, color='black'))

            yao_list.append(sym)

        shangYao = self.guaDict["".join([str(i) for i in yao_list[3: 6]])]
        xiaoYao = self.guaDict["".join([str(i) for i in yao_list[0: 3]])]

        show()


if __name__ == '__main__':
    engine().drowYao()
