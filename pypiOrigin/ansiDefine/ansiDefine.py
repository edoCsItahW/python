#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/3/13 16:09
# 当前项目名: test_architectures.py
# 编码模式: utf-8
# 注释:
# -------------------------<Lenovo>----------------------------
"""
定义部分ANSI转义符.
"""
from math import ceil

__version__ = "0.0.6"

__all__ = [
    "ansiManger"
]


class ansiManger:
    """
    颜色管理器.

    `更多颜色 <http://www.ilikeseo.cn/wangzhanyingxiaozhishi_30.html>`_

    Method:
        以f_开头的方法:
            *文字将被f_后对应的颜色或效果名作用.*

            * **_str**: 被颜色或效果作用的文本.
            * **_ANSI**: 需要额外添加的效果或颜色.
            * **End**: 是否需要在结尾时设置为特定颜色或效果,如果为空或None则为重置符号,如果填写则为知道符号.

        return_all_color:
            浏览颜色.



    Attributes:
        end: 结束符.
        b_wide: 粗体.
        b_light: 淡色.
        b_incline: 斜体.
        b_under_line: 下划线.
        b_flicker: 闪烁.
        b_reverseDisplay: 反显.
        b_hide: 隐藏.
        black: 黑色.
        red: 红色.
        green: 绿色.
        yellow: 黄色.
        blue_d: 深蓝.
        purple: 紫色.
        blue_l: 浅蓝.
        grey: 灰色.
        white: 白色.
        systemRED: 系统红.
        systemBLUE: 系统蓝.
        coldGrey: 冷灰.
        slateGrey: 石板灰.
        warmGray: 暖灰色.
        antiqueWhite: 古董白.
        pink: 粉红.
        crimson: 腥红.
        lavenderblush: 苍白的紫罗兰红.
        palevioletred: 脸红的淡紫红.
        hotpink: 热情的粉红.
        mediumvioletred: 适中的紫罗兰红.
        orchid: 兰花紫.
        thistle: 苍紫.
        plum: 轻紫.
        violet: 紫罗兰.
        fuchsia: 紫红.
        darkmagenta: 深洋紫.
        purple: 紫.
        mediumorchid: 适中的兰花紫.
        darkviolet: 深紫罗兰.
        indigo: 靓青.
        blueviolet: 蓝紫罗兰.
        mediumpurple: 适中的紫.
        mediumslateblue: 适中的的板岩蓝.
        slateblue: 板岩蓝.
        darkslateblue: 深板岩蓝.
        lavender: 熏衣草花的淡紫.
        ghostwhite: 幽灵白.
        blue: 蓝.
        mediumblue: 适中的蓝.
        midnightblue: 午夜蓝.
        darkblue: 深蓝.
        navy: 海军蓝.
        royalblue: 皇家蓝.
        cornflowerblue: 矢车菊蓝.
        lightsteelblue: 淡钢蓝.
        lightslategray: 浅石板灰.
        slategray: 石板灰.
        dodgerblue: 道奇蓝.
        aliceblue: 爱丽丝蓝.
        steelblue: 钢蓝.
        lightskyblue: 淡天蓝.
        skyblue: 天蓝.
        deepskyblue: 深天蓝.
        lightblue: 淡蓝.
        powderblue: 火药蓝.
        cadetblue: 军校蓝.
        azure: 蔚蓝.
        lightcyan: 淡青.
        paleturquoise: 苍白的宝石绿.
        cyan: 青.
        aqua: 水绿.
        darkturquoise: 深宝石绿.
        darkslategray: 深石板灰.
        darkcyan: 深青色.
        teal: 水鸭色.
        mediumturquoise: 适中的宝石绿.
        lightseagreen: 浅海洋绿.
        turquoise: 宝石绿.
        aquamarine: 碧绿.
        mediumaquamarine: 适中的碧绿.
        mediumspringgreen: 适中的春天绿.
        mintcream: 薄荷奶油.
        springgreen: 春天绿.
        mediumseagreen: 适中的海洋绿.
        seagreen: 海洋绿.
        honeydew: 浅粉红.
        lightgreen: 浅绿.
        palegreen: 苍白绿.
        darkseagreen: 深海洋绿.
        limegreen: 柠檬绿.
        lime: 柠檬.
        forestgreen: 森林绿.
        chartreuse: 查特酒绿.
        lawngreen: 草坪绿.
        greenyellow: 绿黄.
        darkolivegreen: 深橄榄绿.
        yellowgreen: 黄绿.
        olivedrab: 橄榄褐.
        beige: 米色.
        lightgoldenrodyellow: 浅秋黄.
        ivory: 象牙白.
        lightyellow: 浅黄.
        yellow: 黄.
        olive: 橄榄.
        darkkhaki: 深卡其布.
        lemonchiffon: 柠檬沙.
        palegoldenrod: 灰秋.
        khaki: 卡其布.
        gold: 金.
        cornsilk: 玉米.
        goldenrod: 秋.
        darkgoldenrod: 深秋.
        floralwhite: 白花.
        oldlace: 浅米色.
        wheat: 小麦.
        moccasin: 鹿皮.
        orange: 橙.
        papayawhip: 木瓜.
        blanchedalmond: 漂白后的杏仁.
        navajowhite: 耐而节白.
        antiquewhite: 古白.
        tan: 晒.
        burlywood: 树干.
        bisque: 乳脂.
        darkorange: 深橙色.
        linen: 亚麻.
        peru: 秘鲁.
        sandybrown: 沙棕.
        chocolate: 巧克力.
        chocolatesaddlebrown: 马鞍棕.
        seashell: 海贝.
        sienna: 土黄赭.
        lightsalmon: 浅肉.
        coral: 珊瑚.
        orangered: 橙红.
        tomato: 番茄色.
        mistyrose: 雾中玫瑰.
        salmon: 肉.
        snow: 雪.
        lightcoral: 浅珊瑚.
        rosybrown: 玫瑰棕.
        indianred: 浅粉红.
        brown: 棕.
        firebrick: 火砖.
        darkred: 深红.
        maroon: 粟色.
        white: 白.
        whitesmoke: 烟白.
        gainsboro: 赶死部落.
        lightgrey: 浅灰.
        silver: 银白.
        darkgray: 深灰.
        dimgray: 暗灰.
        bg_black: (背景色)黑色.
        bg_red: (背景色)红色.
        bg_green: (背景色)绿色.
        bg_yellow: (背景色)黄色.
        bg_blue_d: (背景色)深蓝.
        bg_purple: (背景色)紫色.
        bg_blue_l: (背景色)浅蓝.
        bg_grey: (背景色)灰色.
        bg_white: (背景色)白色.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        # 效果符
        self.end = '\033[0m'  # 结尾符
        self.b_wide = '\033[1m'  # 粗体
        self.b_light = '\033[2m'  # 淡色
        self.b_incline = '\033[3m'  # 斜体
        self.b_under_line = '\033[4m'  # 下划线
        self.b_flicker = '\033[5m'  # 闪烁
        self.b_reverseDisplay = '\033[7m'  # 反显
        self.b_hide = '\033[8m'  # 隐藏

        # 文本色
        self.black = '\033[30m'  # 黑色
        self.red = '\033[31m'  # 红色
        self.green = '\033[32m'  # 绿色
        self.yellow = '\033[33m'  # 黄色
        self.blue_d = '\033[34m'  # 深蓝
        self.purple = '\033[35m'  # 紫色
        self.blue_l = '\033[36m'  # 浅蓝
        self.grey = '\033[37m'  # 灰色
        self.white = '\033[38m'  # 白色

        # 其它颜色
        self.systemRED = self.otherColor(247, 84, 100)  # 系统红
        self.systemBLUE = self.otherColor(84, 138, 247)  # 系统蓝
        self.coldGrey = self.otherColor(128, 138, 135)  # 冷灰
        self.slateGrey = self.otherColor(112, 128, 105)  # 石板灰
        self.warmGray = self.otherColor(128, 128, 105)  # 暖灰色
        self.antiqueWhite = self.otherColor(250, 235, 215)  # 古董白
        self.pink = self.otherColor(255, 192, 203)  # 粉红
        self.crimson = self.otherColor(220, 20, 60)  # 腥红
        self.lavenderblush = self.otherColor(255, 240, 245)  # 苍白的紫罗兰红
        self.palevioletred = self.otherColor(219, 112, 147)  # 脸红的淡紫红
        self.hotpink = self.otherColor(255, 105, 180)  # 热情的粉红
        self.mediumvioletred = self.otherColor(199, 21, 133)  # 适中的紫罗兰红
        self.orchid = self.otherColor(218, 112, 214)  # 兰花紫
        self.thistle = self.otherColor(216, 191, 216)  # 苍紫
        self.plum = self.otherColor(221, 160, 221)  # 轻紫
        self.violet = self.otherColor(238, 130, 238)  # 紫罗兰
        self.fuchsia = self.otherColor(255, 0, 255)  # 紫红
        self.darkmagenta = self.otherColor(139, 0, 139)  # 深洋紫
        self.mediumorchid = self.otherColor(186, 85, 211)  # 适中的兰花紫
        self.darkviolet = self.otherColor(148, 0, 211)  # 深紫罗兰
        self.indigo = self.otherColor(75, 0, 130)  # 靓青
        self.blueviolet = self.otherColor(138, 43, 226)  # 蓝紫罗兰
        self.mediumpurple = self.otherColor(147, 112, 219)  # 适中的紫
        self.mediumslateblue = self.otherColor(123, 104, 238)  # 适中的的板岩蓝
        self.slateblue = self.otherColor(106, 90, 205)  # 板岩蓝
        self.darkslateblue = self.otherColor(72, 61, 139)  # 深板岩蓝
        self.lavender = self.otherColor(230, 230, 250)  # 熏衣草花的淡紫
        self.ghostwhite = self.otherColor(248, 248, 255)  # 幽灵白
        self.blue = self.otherColor(0, 0, 255)  # 蓝
        self.mediumblue = self.otherColor(0, 0, 205)  # 适中的蓝
        self.midnightblue = self.otherColor(25, 25, 112)  # 午夜蓝
        self.darkblue = self.otherColor(0, 0, 139)  # 深蓝
        self.navy = self.otherColor(0, 0, 128)  # 海军蓝
        self.royalblue = self.otherColor(65, 105, 225)  # 皇家蓝
        self.cornflowerblue = self.otherColor(100, 149, 237)  # 矢车菊蓝
        self.lightsteelblue = self.otherColor(176, 196, 222)  # 淡钢蓝
        self.lightslategray = self.otherColor(119, 136, 153)  # 浅石板灰
        self.slategray = self.otherColor(112, 128, 144)  # 石板灰
        self.dodgerblue = self.otherColor(30, 144, 255)  # 道奇蓝
        self.aliceblue = self.otherColor(240, 248, 255)  # 爱丽丝蓝
        self.steelblue = self.otherColor(70, 130, 180)  # 钢蓝
        self.lightskyblue = self.otherColor(135, 206, 250)  # 淡天蓝
        self.skyblue = self.otherColor(135, 206, 235)  # 天蓝
        self.deepskyblue = self.otherColor(0, 191, 255)  # 深天蓝
        self.lightblue = self.otherColor(173, 216, 230)  # 淡蓝
        self.powderblue = self.otherColor(176, 224, 230)  # 火药蓝
        self.cadetblue = self.otherColor(95, 158, 160)  # 军校蓝
        self.azure = self.otherColor(240, 255, 255)  # 蔚蓝
        self.lightcyan = self.otherColor(224, 255, 255)  # 淡青
        self.paleturquoise = self.otherColor(175, 238, 238)  # 苍白的宝石绿
        self.cyan = self.otherColor(0, 255, 255)  # 青
        self.aqua = self.otherColor(0, 255, 255)  # 水绿
        self.darkturquoise = self.otherColor(0, 206, 209)  # 深宝石绿
        self.darkslategray = self.otherColor(47, 79, 79)  # 深石板灰
        self.darkcyan = self.otherColor(0, 139, 139)  # 深青色
        self.teal = self.otherColor(0, 128, 128)  # 水鸭色
        self.mediumturquoise = self.otherColor(72, 209, 204)  # 适中的宝石绿
        self.lightseagreen = self.otherColor(32, 178, 170)  # 浅海洋绿
        self.turquoise = self.otherColor(64, 224, 208)  # 宝石绿
        self.aquamarine = self.otherColor(127, 255, 212)  # 碧绿
        self.mediumaquamarine = self.otherColor(102, 205, 170)  # 适中的碧绿
        self.mediumspringgreen = self.otherColor(0, 250, 154)  # 适中的春天绿
        self.mintcream = self.otherColor(245, 255, 250)  # 薄荷奶油
        self.springgreen = self.otherColor(0, 255, 127)  # 春天绿
        self.mediumseagreen = self.otherColor(60, 179, 113)  # 适中的海洋绿
        self.seagreen = self.otherColor(46, 139, 87)  # 海洋绿
        self.honeydew = self.otherColor(240, 255, 240)  # 浅粉红
        self.lightgreen = self.otherColor(144, 238, 144)  # 浅绿
        self.palegreen = self.otherColor(152, 251, 152)  # 苍白绿
        self.darkseagreen = self.otherColor(143, 188, 143)  # 深海洋绿
        self.limegreen = self.otherColor(50, 205, 50)  # 柠檬绿
        self.lime = self.otherColor(0, 255, 0)  # 柠檬
        self.forestgreen = self.otherColor(34, 139, 34)  # 森林绿
        self.chartreuse = self.otherColor(127, 255, 0)  # 查特酒绿
        self.lawngreen = self.otherColor(124, 252, 0)  # 草坪绿
        self.greenyellow = self.otherColor(173, 255, 47)  # 绿黄
        self.darkolivegreen = self.otherColor(85, 107, 47)  # 深橄榄绿
        self.yellowgreen = self.otherColor(154, 205, 50)  # 黄绿
        self.olivedrab = self.otherColor(107, 142, 35)  # 橄榄褐
        self.beige = self.otherColor(245, 245, 220)  # 米色
        self.lightgoldenrodyellow = self.otherColor(250, 250, 210)  # 浅秋黄
        self.ivory = self.otherColor(255, 255, 240)  # 象牙白
        self.lightyellow = self.otherColor(255, 255, 224)  # 浅黄
        self.olive = self.otherColor(128, 128, 0)  # 橄榄
        self.darkkhaki = self.otherColor(189, 183, 107)  # 深卡其布
        self.lemonchiffon = self.otherColor(255, 250, 205)  # 柠檬沙
        self.palegoldenrod = self.otherColor(238, 232, 170)  # 灰秋
        self.khaki = self.otherColor(240, 230, 140)  # 卡其布
        self.gold = self.otherColor(255, 215, 0)  # 金
        self.cornsilk = self.otherColor(255, 248, 220)  # 玉米
        self.goldenrod = self.otherColor(218, 165, 32)  # 秋
        self.darkgoldenrod = self.otherColor(184, 134, 11)  # 深秋
        self.floralwhite = self.otherColor(255, 250, 240)  # 白花
        self.oldlace = self.otherColor(253, 245, 230)  # 浅米色
        self.wheat = self.otherColor(245, 222, 179)  # 小麦
        self.moccasin = self.otherColor(255, 228, 181)  # 鹿皮
        self.orange = self.otherColor(255, 165, 0)  # 橙
        self.papayawhip = self.otherColor(255, 239, 213)  # 木瓜
        self.blanchedalmond = self.otherColor(255, 235, 205)  # 漂白后的杏仁
        self.navajowhite = self.otherColor(255, 222, 173)  # 耐而节白
        self.antiquewhite = self.otherColor(250, 235, 215)  # 古白
        self.tan = self.otherColor(210, 180, 140)  # 晒
        self.burlywood = self.otherColor(222, 184, 135)  # 树干
        self.bisque = self.otherColor(255, 228, 196)  # 乳脂
        self.darkorange = self.otherColor(255, 140, 0)  # 深橙色
        self.linen = self.otherColor(250, 240, 230)  # 亚麻
        self.peru = self.otherColor(205, 133, 63)  # 秘鲁
        self.sandybrown = self.otherColor(244, 164, 96)  # 沙棕
        self.chocolate = self.otherColor(210, 105, 30)  # 巧克力
        self.chocolatesaddlebrown = self.otherColor(192, 14, 235)  # 马鞍棕
        self.seashell = self.otherColor(255, 245, 238)  # 海贝
        self.sienna = self.otherColor(160, 82, 45)  # 土黄赭
        self.lightsalmon = self.otherColor(255, 160, 122)  # 浅肉
        self.coral = self.otherColor(255, 127, 80)  # 珊瑚
        self.orangered = self.otherColor(255, 69, 0)  # 橙红
        self.tomato = self.otherColor(255, 99, 71)  # 番茄色
        self.mistyrose = self.otherColor(255, 228, 225)  # 雾中玫瑰
        self.salmon = self.otherColor(250, 128, 114)  # 肉
        self.snow = self.otherColor(255, 250, 250)  # 雪
        self.lightcoral = self.otherColor(240, 128, 128)  # 浅珊瑚
        self.rosybrown = self.otherColor(188, 143, 143)  # 玫瑰棕
        self.indianred = self.otherColor(205, 92, 92)  # 浅粉红
        self.brown = self.otherColor(165, 42, 42)  # 棕
        self.firebrick = self.otherColor(178, 34, 34)  # 火砖
        self.darkred = self.otherColor(139, 0, 0)  # 深红
        self.maroon = self.otherColor(128, 0, 0)  # 粟色
        self.whitesmoke = self.otherColor(245, 245, 245)  # 烟白
        self.gainsboro = self.otherColor(220, 220, 220)  # 赶死部落
        self.lightgrey = self.otherColor(211, 211, 211)  # 浅灰
        self.silver = self.otherColor(192, 192, 192)  # 银白
        self.darkgray = self.otherColor(169, 169, 169)  # 深灰
        self.dimgray = self.otherColor(105, 105, 105)  # 暗灰

        # 背景色
        self.bg_black = '\033[40m'
        self.bg_red = '\033[41m'
        self.bg_green = '\033[42m'
        self.bg_yellow = '\033[43m'
        self.bg_blue_d = '\033[44m'
        self.bg_purple = '\033[45m'
        self.bg_blue_l = '\033[46m'
        self.bg_grey = '\033[47m'
        self.bg_white = '\033[48m'

    def f_otherColor(self, _str: str = "", _ANSI: str = '', *, RGB: tuple[int, int, int] | str, foreground: int = 38,
                     colorMode: int = 2, End: str = None):
        if isinstance(RGB, tuple):
            if len(RGB) != 3:
                raise ValueError("RGB值应包括,红色通道,绿色通道,蓝色通道")
            r, g, b = RGB

        # ANSI转义序列，用于设置文本颜色
        color_code = f"\033[{foreground};{colorMode};{r};{g};{b}m" if isinstance(RGB, tuple) else RGB
        return f"{color_code}{_ANSI}{_str}{self.end if End is None else End}"

    @staticmethod
    def otherColor(r: int, g: int, b: int, *, foreground: int = 38, colorMode: int = 2) -> str:
        """
        定制其它颜色.

        对于一个ANSI颜色:
            **\\033[38;2;247;84;100m**

            * 38: 颜色设置的前缀,表示设置前景色.
            * 2: 颜色模式,表示使用RGB颜色模式.
            * 247: 红色通道的值,范围是0-255.
            * 84: 绿色通道的值,范围是0-255.
            * 100: 蓝色通道的值,范围是0-255.
            * m: 颜色设置的后缀,表示设置颜色结束.

        :param int r: 红色通道.
        :param int g: 绿色通道.
        :param int b: 蓝色通道.
        :keyword foreground: 前景色.
        :type foreground: int
        :keyword colorMode: 颜色模式.
        :type colorMode: int
        :return 格式化后的颜色.
        """
        return f"\033[{foreground};{colorMode};{r};{g};{b}m"

    def f_wide(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.b_wide}{_ANSI}{_str}{self.end if End is None else End}'

    def f_light(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.b_light}{_ANSI}{_str}{self.end if End is None else End}'

    def f_QingXie(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.b_incline}{_ANSI}{_str}{self.end if End is None else End}'

    def f_under_line(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.b_under_line}{_ANSI}{_str}{self.end if End is None else End}'

    def f_ShanShuo(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.b_flicker}{_ANSI}{_str}{self.end if End is None else End}'

    def f_FanXian(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.b_reverseDisplay}{_ANSI}{_str}{self.end if End is None else End}'

    def f_hide(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.b_hide}{_ANSI}{_str}{self.end if End is None else End}'

    def f_black(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.black}{_ANSI}{_str}{self.end if End is None else End}'

    def f_red(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.red}{_ANSI}{_str}{self.end if End is None else End}'

    def f_green(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.green}{_ANSI}{_str}{self.end if End is None else End}'

    def f_yellow(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.yellow}{_ANSI}{_str}{self.end if End is None else End}'

    def f_blue_d(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.blue_d}{_ANSI}{_str}{self.end if End is None else End}'

    def f_purple(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.purple}{_ANSI}{_str}{self.end if End is None else End}'

    def f_blue_l(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.blue_l}{_ANSI}{_str}{self.end if End is None else End}'

    def f_grey(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.grey}{_ANSI}{_str}{self.end if End is None else End}'

    def f_white(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.white}{_ANSI}{_str}{self.end if End is None else End}'

    def f_systemRED(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.systemRED}{_ANSI}{_str}{self.end if End is None else End}'

    def f_systemBULE(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.systemBLUE}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_black(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.bg_black}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_red(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.bg_red}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_green(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.bg_green}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_yellow(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.bg_yellow}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_blue_d(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.bg_blue_d}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_purple(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.bg_purple}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_blue_l(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.bg_blue_l}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_grey(self, _str: str, *, _ANSI: str = '', End: str = None):
        return f'{self.bg_grey}{_ANSI}{_str}{self.end if End is None else End}'

    def f_bg_white(self, _str: str, *, _ANSI: str = '', End: str = None) -> str:
        return f'{self.bg_white}{_ANSI}{_str}{self.end if End is None else End}'

    @classmethod
    def return_all_color(cls, _str: str, *, _ANSI: str = ''):
        f_list = ['粗体', '淡色', '斜体', '下划线', '闪烁', '6似乎没有效果', '反显', '隐藏']
        c_list = ['黑色', '红色', '绿色', '黄色', '蓝色', '紫色', '亮蓝', "灰色", "白色"]
        for i, v in enumerate(f_list, start=1):
            print(f"{i}:\033[{i}m{v}\033[0m")
        for i, v in enumerate(c_list):
            print(f"3{i}:\033[3{i}m{v}\033[0m")
        for i, v in enumerate(c_list):
            print(f"4{i}:\033[4{i}m{v}背景\033[0m")

    def gradient(self, _str: str, beginColor: str | tuple[int, int, int] = (0, 0, 0), endColor: str | tuple[int, int, int] = (255, 255, 255)):
        gapList = [(abs(e-b) / len(_str)) for b, e in zip(beginColor, endColor)]
        return "".join([self.f_otherColor(t, RGB=(beginColor[0] + ceil(gapList[0] * i), beginColor[1] + ceil(gapList[1] * i), beginColor[2] + ceil(gapList[2] * i))) for i, t in enumerate(list(_str))])


if __name__ == '__main__':
    pass
