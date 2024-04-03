#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/13 13:11
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
from torchvision.transforms import Resize, Grayscale, ToTensor, Normalize
from matplotlib.pyplot import subplots, show, plot, rcParams, text, title, xlabel, ylabel, xticks
from collections.abc import Container
from PIL.Image import open as imgopen
from typing import Annotated, TypeGuard, Callable, Literal, Iterable, Sequence
from numpy import array


__version__ = "0.0.2"

__all__ = [
    "baseImg",
    "comType",
    "figManger",
    "imgManger",
    "processimg"
]


class comType:
    def __init__(self, Any):
        self.obj = Any

    def checkType(self, obj=None, typestr: str = ''):
        if obj is None:
            obj = self.obj
        if isinstance(obj, Container):
            if len(obj):
                for nextobj in obj:
                    self.checkType(nextobj, typestr)
            else:
                typestr += str(type(obj))
        else:
            typestr += str(type(obj))
        return eval(typestr)


class figManger:
    """
    多画布创建器

    Attributes:
        dim: 创建画布的维度,之所以说维度,是因为该方法创建画布的位置和矩阵
            是一样的,例如(1, 2)会创建一个一左一右的画布,(4, 3)会创建4行画布行每一行都有3个画布,
            但需要注意的是不同的维度的调用方法是不一样的,如下所示:
            1.(1, 1): 只生成一个对象,该对象既不是list也不是array所以直接以`.plot...`调用即可.
            2.(1, ...)或(..., 1): 但有一个维度为1维时,返回一个列表,这时你需要使用位置索引`[int]`来调用.
            3.(..., ...): 除了以上维度中有1维的情况,其余情况均返回一个数组,此时你需要使用数组的索引方式,如`[row, column]`调用.
        args: 自动绘制参数,这是个不定位置参数,如果不传入则返回画布对象,如果传入则直接绘制而不返回,
            并且如果传入的数据对象多于维度的大小(即:dimension[0] * dimension[1] > len(args))则会引发IndexError,
            反之少于则剩余画布留白.需要注意的是可接收参数如下:
            1.list[int]: 一个数值列表,将以默认顺序绘制.(如: [1, 4, 9])
            2.list[tuple[int, int]]: 一个元组列表,每个元组首位为x轴坐标,末位为y轴坐标.(如:[(0, 0), (1, 2)])
            3.list[tuple[int, str]]: 一个元组列表,顺序默认,每个元组首位为数值,末位为需要显示在图中数值上方的标签.(如: [(1, "tag"), (4, "二的平方")])
            4.list[tuple[int, tuple[int, str]]]: 等效于第5个.(如:[(0, (0, "tag")), (1, (4, "二的平方"))])
            5.list[tuple[tuple[int, int], str]]: 一个元组列表,首位中的元组为坐标,末尾为标签.(如:[((0, 0), "tag"), ((1, 4), "二的平方")])
    Methods:
        方法名: 方法职能.
    """
    _instance = None

    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dimension: TypeGuard[Annotated[tuple[int, int], "维度"]],
                 func: TypeGuard[Callable] = None | Literal["plot", "scatter"],
                 *args: list | dict):
        self.dim = dimension
        self.args = args
        self.size = self.dim[0] * self.dim[1]
        self.fig = subplots(self.dim[0], self.dim[1])[1]
        self.func = func if args else None
        self._checkparam()

    def _checkparam(self):
        if self.func not in ["plot", "scatter"] and self.args:
            raise TypeError("如args不为空,则必须从['plot', 'scatter']选择一个func参数填入")

    def _checksize(self, xlist: Iterable, ylist: Iterable, index: int = None, textlist: list = None):
        if self.size == 1:
            if textlist:
                for x, y, tag in zip(xlist, ylist, textlist):
                    text(x, y, tag)
            exec(f"self.fig.{self.func}({xlist}, {ylist})")
        elif 1 in self.dim:
            eval(f"self.fig[{index}].{self.func}({xlist}, {ylist})")
            if textlist:
                for x, y, tag in zip(xlist, ylist, textlist):
                    eval(f"self.fig[{index}].annotate({tag}, xy=({x}, {y}))")
        else:
            X, Y = self._returnpos(index)
            eval(f"self.fig[{X}, {Y}].{self.func}({xlist}, {ylist})")
            if textlist:
                for x, y, tag in zip(xlist, ylist, textlist):
                    eval(f"self.fig[{X}, {Y}].annotate('{tag}', xy=({x}, {y}))")

    def _undraw(self, index: int, data: list):
        # list
        if isinstance(data, list):
            # 1.int
            if all(isinstance(i, int | float) for i in data):
                self._checksize(list(range(len(data))), data, index)
            # list[tuple[..., ...]]
            elif isinstance(n := data[0], tuple) and len(n) == 2:
                # list[tuple[int, ...]]
                if isinstance(n[0], int | float):
                    # list[tuple[int, int]]
                    if isinstance(l := n[1], int | float):
                        self._checksize([i[0] for i in data], [i[1] for i in data], index)
                    # list[tuple[int, str]]
                    elif isinstance(l, str):
                        self._checksize(list(range(len(l1 := [i[0] for i in data]))), l1, index, [i[1] for i in data])
                    # list[tuple[int, tuple[..., ...]]]
                    elif isinstance(t := n[1], tuple):
                        # list[tuple[int, tuple[int, str]]]
                        if isinstance(t[0], int) and isinstance(t[1], str):
                            self._checksize([i[0] for i in data], [i[1][0] for i in data], index,
                                            [i[1][1] for i in data])
                        else:
                            raise ValueError(f"-> {data} <-不接受的形式")
                    else:
                        raise ValueError(f"-> {data} <-不接受的形式")
                # list[tuple[tuple[int, int], str]]
                elif isinstance(l2 := n[0], tuple) and isinstance(n[1], str) and all(
                        isinstance(i, int | float) for i in l2):
                    self._checksize([i[0][0] for i in data], [i[0][1] for i in data], index, [i[1] for i in data])
                else:
                    raise ValueError(f"-> {data} <-不接受的形式")
            else:
                raise ValueError(f"-> {data} <-不接受的形式")
        else:
            raise ValueError(f"-> {data} <-不接受的形式")

    def _returnpos(self, index: int):
        return index // self.dim[1], index % self.dim[1]

    def draw(self):
        if self.args:
            if self.size >= len(self.args):
                rcParams['font.sans-serif'] = ['Microsoft YaHei']
                for i, arg in enumerate(self.args):
                    self._undraw(i, arg)
                show()
        else:
            return self.fig


class baseImg:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        rcParams['font.sans-serif'] = ['Microsoft YaHei']

    @staticmethod
    def plot(_seq: Sequence | list[int | tuple[int, int]] | dict[tuple, str], *,
             Title: str = None, Xlabel: tuple[str, tuple[Literal["f"], float], tuple[Literal["c"], str]] = None, Ylabel: tuple[str, tuple[Literal["f"], float], tuple[Literal["c"], str]] = None, Xtick: list = None):
        from conFunc import sequence

        if isinstance(_seq, list):
            if not isinstance(_seq[0], int):
                plot((xlist := sequence(len(_seq))), _seq)
            elif isinstance(_seq[0], tuple):
                plot((xlist := [i[0] for i in _seq]), [i[1] for i in _seq])
        elif isinstance(_seq, dict):
            values = _seq.keys()
            plot((xlist := [i[0] for i in values]), (ylist := [i[1] for i in values]))
            for x, y, t in zip(xlist, ylist, _seq.values()):
                text(x, y, t)

        for idx, i in enumerate([Xlabel, Ylabel]):
            if i is not None:
                if isinstance(i, tuple):
                    if isinstance(i[0], str):
                        xtext = i[0]
                    if len(i) > 1:
                        for t in i[1:]:
                            if isinstance(t, tuple) and isinstance(t[0], str) and isinstance(t[1], (int, float, str)):
                                if t[0] == "f":
                                    font = None if t[1] is None else t[1]
                                if t[0] == "c":
                                    color = None if t[1] is None else t[1]
                            else:
                                raise TypeError(f"值{i}不符合参数格式.")
                else:
                    raise TypeError(f"值{i}不符合参数格式.")

            if idx == 0:
                None if Xlabel is None else xlabel(xtext, fontsize=font, color=color)

        None if title is None else title(Title)
        None if Ylabel is None else ylabel(Ylabel)
        None if Xtick is None else xticks(xlist, Xtick)

        show()


class imgManger:
    def __init__(self, imgpath: str, mode: Literal["L", "RGB"]):
        self.imgpath = imgpath
        self.mode = mode
        self.imgage = self.getimg(self.imgpath)
        self.w, self.h = self.shape

    @staticmethod
    def getimg(path: str):
        return imgopen(path)

    def convert(self, mode: Literal["L", "RGB"]):
        return self.imgage.convert(mode)

    def pixels(self, mode: Literal["L", "RGB"]):
        if mode == "L":
            return list(self.convert("L").getdata())
        elif mode == "RGB":
            return self.imgage.load()

    @property
    def shape(self):
        return self.imgage.size

    @property
    def arr(self):
        return array(self.pixels(self.mode)).reshape(self.w, self.h)

    def toStr(self):
        from ANSIdefine import ansiManger
        for i, pixel in enumerate(self.pixels("L")):
            pixel = pixel if (l := len(str(pixel))) == 3 else "0" * (3 - l) + str(pixel)
            try:
                r, g, b = self.pixels("RGB")[i % self.h, i // self.w]
                print(ansiManger().f_otherColor("00", RGB=(r, g, b)), end="\n" if i % self.h == self.h - 1 else "")
            except (ValueError, IndexError):
                print(pixel, end="\n" if i % self.h == self.h - 1 else "")


def processimg(imgpathorimg, tosize: tuple = (28, 28), channel: int = 1):
    imglist = [0.5] * channel
    img = imgopen(imgpathorimg) if isinstance(imgpathorimg, str) else imgpathorimg
    img = Resize(tosize)(img)
    grayimg = Grayscale(num_output_channels=channel)(img)
    img = ToTensor()(grayimg)
    normalimg = Normalize(mean=imglist, std=imglist)(img)
    img = normalimg.unsqueeze(0)
    return img


if __name__ == '__main__':
    # fig = imgManger(r"C:\Users\Lenovo\Desktop\lenna.png", "RGB")
    # fig.toStr()
    fig = baseImg()
    fig.plot({(1, 2): "1", (2, 3): "t"}, Xlabel=("a", ("f", 1.0)))
