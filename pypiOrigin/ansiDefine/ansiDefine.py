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

__version__ = "1.0.6"

__all__ = [
    "otherColor",
    "fOtherColor",
    "perview",
    "gradient",
    "ESymbol",
    "FColorSymbol",
    "OColorSymbol",
    "BColorSymbol"
]


sp = "\\"


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


def _checkRgb(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    检查RGB值是否合法.

    :param rgb: RGB值.
    :type rgb: tuple[int, int, int]
    :return: RGB值.
    :rtype: tuple[int, int, int]
    """
    if not isinstance(rgb, tuple):
        raise ValueError(
            "RGB值应为元组!")

    if len(rgb) != 3:
        raise ValueError(
            "RGB值应包括,红色通道,绿色通道,蓝色通道!")

    if any(not isinstance(i, int) or i < 0 or i > 255 for i in rgb):
        raise ValueError(
            "输入的rgb值应为0-255的整数!")

    return rgb


def perview():
    """展示所有颜色"""
    f_list = ['粗体', '淡色', '斜体', '下划线', '闪烁', '6似乎没有效果', '反显', '隐藏']
    c_list = ['黑色', '红色', '绿色', '黄色', '蓝色', '紫色', '亮蓝', "灰色", "白色"]

    for i, v in enumerate(f_list, start=1):
        print(f"{i}:\033[{i}m{v}\033[0m")

    for i, v in enumerate(c_list):
        print(f"3{i}:\033[3{i}m{v}\033[0m")

    for i, v in enumerate(c_list):
        print(f"4{i}:\033[4{i}m{v}背景\033[0m")


def fOtherColor(_str: str = "", _ansi: str = '', *, RGB: tuple[int, int, int] | str, foreground: int = 38, colorMode: int = 2, End: str = None) -> str:
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
    return f"{f'{sp}033[{foreground};{colorMode};{RGB[0]};{RGB[1]};{RGB[2]}m' if isinstance(RGB, tuple) else RGB}{_ansi}{_str}{End if End else FColorSymbol.end}"


def gradient(_str: str, beginColor: str | tuple[int, int, int] = (0, 0, 0), endColor: str | tuple[int, int, int] = (255, 255, 255)) -> str:
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
    gapList = [(abs(e-b) / len(_str)) for b, e in zip(beginColor, endColor)]
    return "".join([fOtherColor(t, RGB=(beginColor[0] + ceil(gapList[0] * i), beginColor[1] + ceil(gapList[1] * i), beginColor[2] + ceil(gapList[2] * i))) for i, t in enumerate(list(_str))])


class ESymbol:
    b_wide = '\033[1m'  # 粗体
    b_light = '\033[2m'  # 淡色
    b_incline = '\033[3m'  # 斜体
    b_under_line = '\033[4m'  # 下划线
    b_flicker = '\033[5m'  # 闪烁
    b_reverseDisplay = '\033[7m'  # 反显
    b_hide = '\033[8m'  # 隐藏


class FColorSymbol:
    end = '\033[0m'  # 结尾符
    black = '\033[30m'  # 黑色
    red = '\033[31m'  # 红色
    green = '\033[32m'  # 绿色
    yellow = '\033[33m'  # 黄色
    blue_d = '\033[34m'  # 深蓝
    purple = '\033[35m'  # 紫色
    blue_l = '\033[36m'  # 浅蓝
    grey = '\033[37m'  # 灰色
    white = '\033[38m'  # 白色


class OColorSymbol:
    systemRED = otherColor(247, 84, 100)  # 系统红
    systemBLUE = otherColor(84, 138, 247)  # 系统蓝
    coldGrey = otherColor(128, 138, 135)  # 冷灰
    slateGrey = otherColor(112, 128, 105)  # 石板灰
    warmGray = otherColor(128, 128, 105)  # 暖灰色
    antiqueWhite = otherColor(250, 235, 215)  # 古董白
    pink = otherColor(255, 192, 203)  # 粉红
    crimson = otherColor(220, 20, 60)  # 腥红
    lavenderblush = otherColor(255, 240, 245)  # 苍白的紫罗兰红
    palevioletred = otherColor(219, 112, 147)  # 脸红的淡紫红
    hotpink = otherColor(255, 105, 180)  # 热情的粉红
    mediumvioletred = otherColor(199, 21, 133)  # 适中的紫罗兰红
    orchid = otherColor(218, 112, 214)  # 兰花紫
    thistle = otherColor(216, 191, 216)  # 苍紫
    plum = otherColor(221, 160, 221)  # 轻紫
    violet = otherColor(238, 130, 238)  # 紫罗兰
    fuchsia = otherColor(255, 0, 255)  # 紫红
    darkmagenta = otherColor(139, 0, 139)  # 深洋紫
    mediumorchid = otherColor(186, 85, 211)  # 适中的兰花紫
    darkviolet = otherColor(148, 0, 211)  # 深紫罗兰
    indigo = otherColor(75, 0, 130)  # 靓青
    blueviolet = otherColor(138, 43, 226)  # 蓝紫罗兰
    mediumpurple = otherColor(147, 112, 219)  # 适中的紫
    mediumslateblue = otherColor(123, 104, 238)  # 适中的的板岩蓝
    slateblue = otherColor(106, 90, 205)  # 板岩蓝
    darkslateblue = otherColor(72, 61, 139)  # 深板岩蓝
    lavender = otherColor(230, 230, 250)  # 熏衣草花的淡紫
    ghostwhite = otherColor(248, 248, 255)  # 幽灵白
    blue = otherColor(0, 0, 255)  # 蓝
    mediumblue = otherColor(0, 0, 205)  # 适中的蓝
    midnightblue = otherColor(25, 25, 112)  # 午夜蓝
    darkblue = otherColor(0, 0, 139)  # 深蓝
    navy = otherColor(0, 0, 128)  # 海军蓝
    royalblue = otherColor(65, 105, 225)  # 皇家蓝
    cornflowerblue = otherColor(100, 149, 237)  # 矢车菊蓝
    lightsteelblue = otherColor(176, 196, 222)  # 淡钢蓝
    lightslategray = otherColor(119, 136, 153)  # 浅石板灰
    slategray = otherColor(112, 128, 144)  # 石板灰
    dodgerblue = otherColor(30, 144, 255)  # 道奇蓝
    aliceblue = otherColor(240, 248, 255)  # 爱丽丝蓝
    steelblue = otherColor(70, 130, 180)  # 钢蓝
    lightskyblue = otherColor(135, 206, 250)  # 淡天蓝
    skyblue = otherColor(135, 206, 235)  # 天蓝
    deepskyblue = otherColor(0, 191, 255)  # 深天蓝
    lightblue = otherColor(173, 216, 230)  # 淡蓝
    powderblue = otherColor(176, 224, 230)  # 火药蓝
    cadetblue = otherColor(95, 158, 160)  # 军校蓝
    azure = otherColor(240, 255, 255)  # 蔚蓝
    lightcyan = otherColor(224, 255, 255)  # 淡青
    paleturquoise = otherColor(175, 238, 238)  # 苍白的宝石绿
    cyan = otherColor(0, 255, 255)  # 青
    aqua = otherColor(0, 255, 255)  # 水绿
    darkturquoise = otherColor(0, 206, 209)  # 深宝石绿
    darkslategray = otherColor(47, 79, 79)  # 深石板灰
    darkcyan = otherColor(0, 139, 139)  # 深青色
    teal = otherColor(0, 128, 128)  # 水鸭色
    mediumturquoise = otherColor(72, 209, 204)  # 适中的宝石绿
    lightseagreen = otherColor(32, 178, 170)  # 浅海洋绿
    turquoise = otherColor(64, 224, 208)  # 宝石绿
    aquamarine = otherColor(127, 255, 212)  # 碧绿
    mediumaquamarine = otherColor(102, 205, 170)  # 适中的碧绿
    mediumspringgreen = otherColor(0, 250, 154)  # 适中的春天绿
    mintcream = otherColor(245, 255, 250)  # 薄荷奶油
    springgreen = otherColor(0, 255, 127)  # 春天绿
    mediumseagreen = otherColor(60, 179, 113)  # 适中的海洋绿
    seagreen = otherColor(46, 139, 87)  # 海洋绿
    honeydew = otherColor(240, 255, 240)  # 浅粉红
    lightgreen = otherColor(144, 238, 144)  # 浅绿
    palegreen = otherColor(152, 251, 152)  # 苍白绿
    darkseagreen = otherColor(143, 188, 143)  # 深海洋绿
    limegreen = otherColor(50, 205, 50)  # 柠檬绿
    lime = otherColor(0, 255, 0)  # 柠檬
    forestgreen = otherColor(34, 139, 34)  # 森林绿
    chartreuse = otherColor(127, 255, 0)  # 查特酒绿
    lawngreen = otherColor(124, 252, 0)  # 草坪绿
    greenyellow = otherColor(173, 255, 47)  # 绿黄
    darkolivegreen = otherColor(85, 107, 47)  # 深橄榄绿
    yellowgreen = otherColor(154, 205, 50)  # 黄绿
    olivedrab = otherColor(107, 142, 35)  # 橄榄褐
    beige = otherColor(245, 245, 220)  # 米色
    lightgoldenrodyellow = otherColor(250, 250, 210)  # 浅秋黄
    ivory = otherColor(255, 255, 240)  # 象牙白
    lightyellow = otherColor(255, 255, 224)  # 浅黄
    olive = otherColor(128, 128, 0)  # 橄榄
    darkkhaki = otherColor(189, 183, 107)  # 深卡其布
    lemonchiffon = otherColor(255, 250, 205)  # 柠檬沙
    palegoldenrod = otherColor(238, 232, 170)  # 灰秋
    khaki = otherColor(240, 230, 140)  # 卡其布
    gold = otherColor(255, 215, 0)  # 金
    cornsilk = otherColor(255, 248, 220)  # 玉米
    goldenrod = otherColor(218, 165, 32)  # 秋
    darkgoldenrod = otherColor(184, 134, 11)  # 深秋
    floralwhite = otherColor(255, 250, 240)  # 白花
    oldlace = otherColor(253, 245, 230)  # 浅米色
    wheat = otherColor(245, 222, 179)  # 小麦
    moccasin = otherColor(255, 228, 181)  # 鹿皮
    orange = otherColor(255, 165, 0)  # 橙
    papayawhip = otherColor(255, 239, 213)  # 木瓜
    blanchedalmond = otherColor(255, 235, 205)  # 漂白后的杏仁
    navajowhite = otherColor(255, 222, 173)  # 耐而节白
    antiquewhite = otherColor(250, 235, 215)  # 古白
    tan = otherColor(210, 180, 140)  # 晒
    burlywood = otherColor(222, 184, 135)  # 树干
    bisque = otherColor(255, 228, 196)  # 乳脂
    darkorange = otherColor(255, 140, 0)  # 深橙色
    linen = otherColor(250, 240, 230)  # 亚麻
    peru = otherColor(205, 133, 63)  # 秘鲁
    sandybrown = otherColor(244, 164, 96)  # 沙棕
    chocolate = otherColor(210, 105, 30)  # 巧克力
    chocolatesaddlebrown = otherColor(192, 14, 235)  # 马鞍棕
    seashell = otherColor(255, 245, 238)  # 海贝
    sienna = otherColor(160, 82, 45)  # 土黄赭
    lightsalmon = otherColor(255, 160, 122)  # 浅肉
    coral = otherColor(255, 127, 80)  # 珊瑚
    orangered = otherColor(255, 69, 0)  # 橙红
    tomato = otherColor(255, 99, 71)  # 番茄色
    mistyrose = otherColor(255, 228, 225)  # 雾中玫瑰
    salmon = otherColor(250, 128, 114)  # 肉
    snow = otherColor(255, 250, 250)  # 雪
    lightcoral = otherColor(240, 128, 128)  # 浅珊瑚
    rosybrown = otherColor(188, 143, 143)  # 玫瑰棕
    indianred = otherColor(205, 92, 92)  # 浅粉红
    brown = otherColor(165, 42, 42)  # 棕
    firebrick = otherColor(178, 34, 34)  # 火砖
    darkred = otherColor(139, 0, 0)  # 深红
    maroon = otherColor(128, 0, 0)  # 粟色
    whitesmoke = otherColor(245, 245, 245)  # 烟白
    gainsboro = otherColor(220, 220, 220)  # 赶死部落
    lightgrey = otherColor(211, 211, 211)  # 浅灰
    silver = otherColor(192, 192, 192)  # 银白
    darkgray = otherColor(169, 169, 169)  # 深灰
    dimgray = otherColor(105, 105, 105)  # 暗灰


class BColorSymbol:
    bg_black = '\033[40m'
    bg_red = '\033[41m'
    bg_green = '\033[42m'
    bg_yellow = '\033[43m'
    bg_blue_d = '\033[44m'
    bg_purple = '\033[45m'
    bg_blue_l = '\033[46m'
    bg_grey = '\033[47m'
    bg_white = '\033[48m'


if __name__ == '__main__':
    pass
