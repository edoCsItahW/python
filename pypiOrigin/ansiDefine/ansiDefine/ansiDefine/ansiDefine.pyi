"""
定义部分ANSI转义符.
"""
__version__: str
__all__: list
sp: str


def otherColor(r: int, g: int, b: int, *, foreground: int=38, colorMode: int=2
    ) ->str:
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
    ...


def _checkRgb(rgb: tuple[int, int, int]) ->tuple[int, int, int]:
    """
    检查RGB值是否合法.

    :param rgb: RGB值.
    :type rgb: tuple[int, int, int]
    :return: RGB值.
    :rtype: tuple[int, int, int]
    """
    ...


def perview():
    """展示所有颜色"""
    ...


def fOtherColor(_str: str='', _ansi: str='', *, RGB: (tuple[int, int, int] |
    str), foreground: int=38, colorMode: int=2, End: str=None) ->str:
    """
    定制其它颜色.

    :param _str: 字符串.
    :type _str: str
    :param _ansi: ANSI转义序列.
    :type _ansi: str
    :keyword RGB: RGB值.
    :type RGB: tuple[int, int, int] | str
    :keyword foreground: 前景色.
    :type foreground: int
    :keyword colorMode: 颜色模式.
    :type colorMode: int
    :keyword End: 结束符.
    :type End: str
    :return: 格式化后的颜色.
    :rtype: str
    """
    ...


def gradient(_str: str, beginColor: (str | tuple[int, int, int])=(0, 0, 0),
    endColor: (str | tuple[int, int, int])=(255, 255, 255)) ->str:
    """
    渐变色.

    :param _str: 字符串.
    :type _str: str
    :param beginColor: 开始颜色
    :type beginColor: tuple[int, int, int]
    :param endColor: 结束颜色
    :type endColor: tuple[int, int, int]
    :return: 格式化后的颜色.
    :rtype: str
    """
    ...


#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

class ESymbol:
    b_wide = '\x1b[1m'
    b_light = '\x1b[2m'
    b_incline = '\x1b[3m'
    b_under_line = '\x1b[4m'
    b_flicker = '\x1b[5m'
    b_reverseDisplay = '\x1b[7m'
    b_hide = '\x1b[8m'


class FColorSymbol:
    end = '\x1b[0m'
    black = '\x1b[30m'
    red = '\x1b[31m'
    green = '\x1b[32m'
    yellow = '\x1b[33m'
    blue_d = '\x1b[34m'
    purple = '\x1b[35m'
    blue_l = '\x1b[36m'
    grey = '\x1b[37m'
    white = '\x1b[38m'


class OColorSymbol:
    systemRED = otherColor(247, 84, 100)
    systemBLUE = otherColor(84, 138, 247)
    coldGrey = otherColor(128, 138, 135)
    slateGrey = otherColor(112, 128, 105)
    warmGray = otherColor(128, 128, 105)
    antiqueWhite = otherColor(250, 235, 215)
    pink = otherColor(255, 192, 203)
    crimson = otherColor(220, 20, 60)
    lavenderblush = otherColor(255, 240, 245)
    palevioletred = otherColor(219, 112, 147)
    hotpink = otherColor(255, 105, 180)
    mediumvioletred = otherColor(199, 21, 133)
    orchid = otherColor(218, 112, 214)
    thistle = otherColor(216, 191, 216)
    plum = otherColor(221, 160, 221)
    violet = otherColor(238, 130, 238)
    fuchsia = otherColor(255, 0, 255)
    darkmagenta = otherColor(139, 0, 139)
    mediumorchid = otherColor(186, 85, 211)
    darkviolet = otherColor(148, 0, 211)
    indigo = otherColor(75, 0, 130)
    blueviolet = otherColor(138, 43, 226)
    mediumpurple = otherColor(147, 112, 219)
    mediumslateblue = otherColor(123, 104, 238)
    slateblue = otherColor(106, 90, 205)
    darkslateblue = otherColor(72, 61, 139)
    lavender = otherColor(230, 230, 250)
    ghostwhite = otherColor(248, 248, 255)
    blue = otherColor(0, 0, 255)
    mediumblue = otherColor(0, 0, 205)
    midnightblue = otherColor(25, 25, 112)
    darkblue = otherColor(0, 0, 139)
    navy = otherColor(0, 0, 128)
    royalblue = otherColor(65, 105, 225)
    cornflowerblue = otherColor(100, 149, 237)
    lightsteelblue = otherColor(176, 196, 222)
    lightslategray = otherColor(119, 136, 153)
    slategray = otherColor(112, 128, 144)
    dodgerblue = otherColor(30, 144, 255)
    aliceblue = otherColor(240, 248, 255)
    steelblue = otherColor(70, 130, 180)
    lightskyblue = otherColor(135, 206, 250)
    skyblue = otherColor(135, 206, 235)
    deepskyblue = otherColor(0, 191, 255)
    lightblue = otherColor(173, 216, 230)
    powderblue = otherColor(176, 224, 230)
    cadetblue = otherColor(95, 158, 160)
    azure = otherColor(240, 255, 255)
    lightcyan = otherColor(224, 255, 255)
    paleturquoise = otherColor(175, 238, 238)
    cyan = otherColor(0, 255, 255)
    aqua = otherColor(0, 255, 255)
    darkturquoise = otherColor(0, 206, 209)
    darkslategray = otherColor(47, 79, 79)
    darkcyan = otherColor(0, 139, 139)
    teal = otherColor(0, 128, 128)
    mediumturquoise = otherColor(72, 209, 204)
    lightseagreen = otherColor(32, 178, 170)
    turquoise = otherColor(64, 224, 208)
    aquamarine = otherColor(127, 255, 212)
    mediumaquamarine = otherColor(102, 205, 170)
    mediumspringgreen = otherColor(0, 250, 154)
    mintcream = otherColor(245, 255, 250)
    springgreen = otherColor(0, 255, 127)
    mediumseagreen = otherColor(60, 179, 113)
    seagreen = otherColor(46, 139, 87)
    honeydew = otherColor(240, 255, 240)
    lightgreen = otherColor(144, 238, 144)
    palegreen = otherColor(152, 251, 152)
    darkseagreen = otherColor(143, 188, 143)
    limegreen = otherColor(50, 205, 50)
    lime = otherColor(0, 255, 0)
    forestgreen = otherColor(34, 139, 34)
    chartreuse = otherColor(127, 255, 0)
    lawngreen = otherColor(124, 252, 0)
    greenyellow = otherColor(173, 255, 47)
    darkolivegreen = otherColor(85, 107, 47)
    yellowgreen = otherColor(154, 205, 50)
    olivedrab = otherColor(107, 142, 35)
    beige = otherColor(245, 245, 220)
    lightgoldenrodyellow = otherColor(250, 250, 210)
    ivory = otherColor(255, 255, 240)
    lightyellow = otherColor(255, 255, 224)
    olive = otherColor(128, 128, 0)
    darkkhaki = otherColor(189, 183, 107)
    lemonchiffon = otherColor(255, 250, 205)
    palegoldenrod = otherColor(238, 232, 170)
    khaki = otherColor(240, 230, 140)
    gold = otherColor(255, 215, 0)
    cornsilk = otherColor(255, 248, 220)
    goldenrod = otherColor(218, 165, 32)
    darkgoldenrod = otherColor(184, 134, 11)
    floralwhite = otherColor(255, 250, 240)
    oldlace = otherColor(253, 245, 230)
    wheat = otherColor(245, 222, 179)
    moccasin = otherColor(255, 228, 181)
    orange = otherColor(255, 165, 0)
    papayawhip = otherColor(255, 239, 213)
    blanchedalmond = otherColor(255, 235, 205)
    navajowhite = otherColor(255, 222, 173)
    antiquewhite = otherColor(250, 235, 215)
    tan = otherColor(210, 180, 140)
    burlywood = otherColor(222, 184, 135)
    bisque = otherColor(255, 228, 196)
    darkorange = otherColor(255, 140, 0)
    linen = otherColor(250, 240, 230)
    peru = otherColor(205, 133, 63)
    sandybrown = otherColor(244, 164, 96)
    chocolate = otherColor(210, 105, 30)
    chocolatesaddlebrown = otherColor(192, 14, 235)
    seashell = otherColor(255, 245, 238)
    sienna = otherColor(160, 82, 45)
    lightsalmon = otherColor(255, 160, 122)
    coral = otherColor(255, 127, 80)
    orangered = otherColor(255, 69, 0)
    tomato = otherColor(255, 99, 71)
    mistyrose = otherColor(255, 228, 225)
    salmon = otherColor(250, 128, 114)
    snow = otherColor(255, 250, 250)
    lightcoral = otherColor(240, 128, 128)
    rosybrown = otherColor(188, 143, 143)
    indianred = otherColor(205, 92, 92)
    brown = otherColor(165, 42, 42)
    firebrick = otherColor(178, 34, 34)
    darkred = otherColor(139, 0, 0)
    maroon = otherColor(128, 0, 0)
    whitesmoke = otherColor(245, 245, 245)
    gainsboro = otherColor(220, 220, 220)
    lightgrey = otherColor(211, 211, 211)
    silver = otherColor(192, 192, 192)
    darkgray = otherColor(169, 169, 169)
    dimgray = otherColor(105, 105, 105)


class BColorSymbol:
    bg_black = '\x1b[40m'
    bg_red = '\x1b[41m'
    bg_green = '\x1b[42m'
    bg_yellow = '\x1b[43m'
    bg_blue_d = '\x1b[44m'
    bg_purple = '\x1b[45m'
    bg_blue_l = '\x1b[46m'
    bg_grey = '\x1b[47m'
    bg_white = '\x1b[48m'
