#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/20 10:54
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
from torchvision.transforms import ToTensor, Resize, Grayscale
from matplotlib.pyplot import plot, show, text, title, xlabel, ylabel, rcParams, figure, scatter
from torch.utils.data import Dataset, DataLoader
from scipy.optimize import leastsq
from numpy.linalg import inv
from PIL.Image import open as imgopen
from typing import Callable
from numpy import ndarray, array, hstack, ones, linspace, meshgrid, e, int32, float64, log
from torch import inverse, from_numpy, transpose
from os import listdir, path, rename, PathLike


__version__ = "0.0.4"


__all__ = [
    "dataloader",
    "dataset",
    "fitter",
    "layerCalculate",
    "markLabel"
]


class fitter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, Xlist: list, Ylist: list, initparam: list = None,
                 times: int = 1e+4, alpha: float = 1e-5, limit: float = 1e-7):
        # 数组化
        self.X, self.Y = array(Xlist), array(Ylist)
        self._Xshape = 1 if isinstance(self.X[0], (int32, float64)) else len(self.X[0])
        # 检测
        if initparam:
            if not (len(self.X) and len(self.Y)):
                raise ValueError(f"X和Y列表不能为空,请检查你的列表,\nX:{self.X}\nY:{self.Y}")
            if len(initparam) != self._Xshape + 1:
                raise ValueError(
                    f"初始值长度必须比X列表中每一个元素的长度多1,以保证偏置项,你的参数\n初始值:{initparam},\nX:{self.X}")
            self.initp = array(initparam)
        else:
            self.initp = array([0] * (self._Xshape + 1))

        # 其它参数
        self.times, self._a, self.limit = int(times), alpha, limit

        # 衍生参数
        self._m = len(self.X)
        self._sumX, self._sumY = sum(self.X), sum(self.Y)
        self._c = 1 / (2 * self._m)
        # 添加偏置项的X
        self._mutiX = self._addbias(self.X).transpose() if self._Xshape != len(self.initp) else self.X
        self._summutiX = sum(self._mutiX.transpose())
        self._sumXpower2, self._sumYpower2 = sum([i.transpose() @ i for i in self._mutiX]), self.Y.transpose() @ self.Y
        self._sumXtY = self._mutiX @ self.Y.transpose()

    # 添加偏置项
    @staticmethod
    def _addbias(arr: ndarray):
        X = arr.reshape(-1, 1) if len(arr.shape) == 1 else arr
        return hstack((ones((X.shape[0], 1)), X))

    # 损失函数
    def lineloss(self, param: ndarray):
        ptXpower2 = sum([(param.transpose() @ i) ** 2 for i in self._mutiX.transpose()])
        return self._c * (ptXpower2 - 2 * param @ self._sumXtY + self._sumYpower2)

    def logisticloss(self, param: ndarray):
        def logL(x, y): return y * log(sig := self.sigmoid(param.transpose() @ x)) + (1 - y) * log(1 - sig)

        return sum([logL(x, y) for x, y in zip(self._mutiX.transpose(), self.Y)])

    @staticmethod
    # sigmoid函数
    def sigmoid(param: int | float):
        return 1 / (1 + e ** -param)

    # 循环
    def _loop(self, func: Callable, init=None, times=None, limit=None, *, checkprint=False, checkfig=False):

        initvar = self.initp if init is None else init
        times = self.times if times is None else times
        limit = self.limit if limit is None else limit

        logdirt = {}
        for _ in range(times):
            nextvar = func(initvar)
            print(f"{initvar} -> {nextvar}") if checkprint else None
            if all([abs(i) < limit for i in (nextvar - initvar)]): break
            initvar = nextvar
            logdirt.update([(tuple(initvar), self.lineloss(initvar))]) if checkfig else None
        if checkfig:
            return logdirt
        return nextvar

    # 图片绘制
    def slopefig(self, logdirt: dict):
        if (l := len(self.X.shape)) > 1:
            raise ValueError(f"无法绘制{l + 1}以上图像")
        rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 调整字体
        rcParams['axes.unicode_minus'] = False
        maxx = max(self.X)
        for i, item in enumerate(logdirt.keys()):
            plot([0, maxx], [item[1], pos := (item[0] * maxx + item[1])])
            text(maxx, pos, str(i))
        title('斜率变化图')
        xlabel("X")
        ylabel("y")
        show()

    @staticmethod
    def downratefig(logdirt: dict):

        from conFunc import sequence

        keys = [array(i) for i in logdirt.keys()]
        if len(s := keys[0].shape) > 1:
            raise ValueError(f"不支持绘制值维度大于1的下降率图像,传入维度{s}")
        rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 调整字体
        rcParams['axes.unicode_minus'] = False
        plot(sequence(keys), list(logdirt.values()))
        title("损失函数收敛图")
        xlabel("迭代次数")
        ylabel("loss(Θ)")
        show()

    def loss3D(self, XYrange: tuple[int, int] = (-100, 100), *, density: int = 100, allowshow: bool = True):
        if (l := len(self.X.shape)) > 1:
            raise ValueError(f"无法绘制{l + 1}以上图像")
        rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 调整字体
        rcParams['axes.unicode_minus'] = False
        start, end = XYrange[0], XYrange[1]
        X = Y = linspace(start, end, density)
        vecx, vecy = meshgrid(X, Y)
        fig = figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.set_xlabel("参数")
        ax.set_ylabel("截距")
        ax.set_zlabel("loss(参数, 截距)")
        arr = [self.lineloss(array([k, b])) for k, b in zip(vecx.ravel(), vecy.ravel())]
        ax.plot_surface(vecx, vecy, array(arr).reshape(vecx.shape[0], vecy.shape[1]), cmap="viridis")
        if allowshow:
            show()
        else:
            return ax

    def resfig(self, logdirt: dict):
        param = list(logdirt.items())[-1]
        plot([0, m := max(self.X)], [param[0], param[1] * m + param[0]])
        scatter(self.X, self.Y)
        show()

    def downrate3D(self, logdirt: dict):
        if (l := len(self.X.shape)) > 1:
            raise ValueError(f"无法绘制{l + 1}以上图像")
        rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 调整字体
        rcParams['axes.unicode_minus'] = False

    # 拟合方法
    def scipyfit(self):

        def residuals(param: ndarray): return param.transpose() @ self._mutiX - self.Y

        res = leastsq(residuals, self.initp)[0]

        return res

    def linegradientfit(self, init: ndarray = None, times: int = None, limit: float = None,
                        checkprint: bool = False, checkfig: bool = False,
                        loopt: int = None, loopa: float = None, loopl: float = None,
                        loopprint: bool = False, loopfig: bool = False) -> ndarray | dict:

        def simple_loss(param: ndarray):
            return param - (loopa / self._m) * (param.transpose() * self._sumXpower2 - self._sumXtY)

        def test(param: ndarray):
            return param - (loopa / self._m) * (array([init.transpose() @ i for i in
                                                       self._mutiX.transpose()]).transpose() - self.Y.transpose()) @ self._mutiX.transpose()

        def test1(param: ndarray):
            return param - (self._a / self._m) * (param.transpose() @ self._mutiX - self.Y) @ self._mutiX.transpose()

        print(test1(init))

        init = init if init is not None else self.initp
        times = times if times is not None else self.times
        limit = limit if limit is not None else self.limit

        loopt = loopt if loopt is not None else self.times
        loopa = loopa if loopa is not None else self._a
        loopl = loopl if loopl is not None else self.limit

        return self._loop(test1, init, loopt, loopl, checkprint=loopprint, checkfig=loopfig)
        # logdirt = {}
        # for i in range(1, times):
        #     init *= i
        #     res = self._loop(simple_loss, init, loopt, loopa, loopl)
        #     print(f"{init} -> {res}") if checkprint else None
        #     # if all([abs(i) < limit for i in (res - init)]): break
        #     # init = res
        #     logdirt.update([(tuple(res), self.lineloss(res))]) if checkfig else None
        # if checkfig:
        #     return logdirt
        # return res

    def normalEq(self):
        tenX, tenY = from_numpy(self._mutiX), from_numpy(self.Y)
        try:
            tranX = transpose(tenX, 0, 1)
            return (inverse(tenX @ tranX) @ tenX @ tenY).numpy()
        except Exception:
            print(self._mutiX.transpose() @ self._mutiX)
            return inv(self._mutiX @ self._mutiX.transpose()) @ self._mutiX @ self.Y

    def logisticRegression(self):
        pass


class dataset(Dataset):
    def __init__(self, imginfo: dict[str, str], transfrom=ToTensor(), *, size: tuple = None, channel: int = None):
        self.imginfo = imginfo
        self.transfrom = transfrom
        self.pathlist = list(imginfo.keys())
        self.size = size
        self.channel = channel
        self.classes = list(set(imginfo.values()))

    def __len__(self):
        return len(self.pathlist)

    def __getitem__(self, index):
        imgpath = self.pathlist[index]
        image = imgopen(imgpath)

        if self.size:
            image = Resize((self.size[0], self.size[1]))(image)

        if self.channel:
            image = Grayscale(num_output_channels=self.channel)(image)

        if self.transfrom:
            image = self.transfrom(image)

        label = int(self.imginfo[imgpath])

        return image, label


class dataloader:
    def __init__(self, imginfo: dict[str, str], size: tuple, channel: int, *, transfrom=ToTensor(), batchSize=None, shuffle=True):
        self.imginfo = imginfo
        self.size = size
        self.channel = channel
        self.transfrom = transfrom
        self.batchsize = batchSize
        self.shuffle = shuffle

    def __call__(self): return DataLoader(
        dataset(self.imginfo, transfrom=self.transfrom, size=self.size, channel=self.channel),
        batch_size=self.batchsize, shuffle=self.shuffle)


def layerCalculate(imgw: int | float, imgh: int | float, kernel: int, stride: int, padding: int, poolk: int):
    outw = ((imgw - kernel + 2 * padding) / stride + 1) / poolk
    outh = ((imgh - kernel + 2 * padding) / stride + 1) / poolk
    return outw, outh


class markLabel:
    def __init__(self, dirPath: str | PathLike[str]):
        self._dirPath = dirPath

    def mark(self):
        dirList = [path.join(self._dirPath, i) for i in listdir(self._dirPath)]

        labelDict = {}

        for p in dirList:
            label = p.split("\\")[-1]
            for n in listdir(p):
                labelDict.update([(path.join(p, n), label)])

        return labelDict


if __name__ == '__main__':
    # fit = fitter([1, 2, 3], [1, 2, 3])
    # {"a": 1, "b": 4, "c": 9, "d": 16}
    print(layerCalculate(28, 28, 5, 1, 2, 2))
    pass
