#! /user/bin/python3

#  Copyright (c) 2023-2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/12/18 13:49
# 当前项目名: ImgAnalysis
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from torchvision.transforms import ToTensor, Compose, Grayscale, Normalize
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam
from torch.cuda import is_available
from PIL.Image import open as imgopen
from functools import wraps, cache
from torch.nn import Module, Sequential, Conv2d, ReLU, MaxPool2d, Linear, CrossEntropyLoss, BatchNorm2d, Dropout2d, \
    Flatten, Dropout
from datetime import datetime
from warnings import warn
from inspect import currentframe
from typing import Literal, Annotated, Callable
from random import choice
from shutil import copy
from torch import Tensor, device, save, max as torchmax
from time import time
from os import PathLike, path, mkdir, rename, listdir
from re import findall

try:
    from figureTools import processimg  # type: ignore
    from conFunc import partitem, temPrint  # type: ignore

except ModuleNotFoundError as e:
    module = findall(r"(?<=')(.*?)(?=')", e.args[0])[0]
    raise ModuleNotFoundError(  # 未安装库
        f"未安装库'{module}', 输入`pip install -i https://test.pypi.org/simple/ {module}`以安装."
    )


# todo: 完善dir级图片预处理类.


def errorLog(output: bool = True, *, mode: Literal["W", "E", "P"] = "E"):
    """
    错误记录装饰器.

    :param output: 是否允许输出.
    :type output: bool
    :keyword mode: 输出类型,包括
    :type mode: str
    """
    def getfunc(func):
        wraps(func)

        def wapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)  # 错误捕获
            except Exception as e:
                fb = currentframe().f_back
                e.add_note(
                    f"File {fb.f_code.co_filename}, line {fb.f_lineno}, in <{fb.f_code.co_name}> -> {func.__name__}")
                if output:
                    if mode == "W":
                        warn(
                            f"{e.__class__.__name__}: {e.args} line {e.__traceback__.tb_lineno} in {e.__traceback__.tb_frame.f_code.co_name}")
                    elif mode == "E":
                        raise e
                    elif mode == "P":
                        print(
                            f"{e.__class__.__name__}: {e.args} line {e.__traceback__.tb_lineno} in {e.__traceback__.tb_frame.f_code.co_name}")
                    else:
                        raise ValueError(  # 参数错误
                            f"关键字参数`mode`只允许为'W','E'或者'P',而你的输入'{mode}'"
                        )

        return wapper

    return getfunc


class imgDirProcessing:
    """
    文件夹级图片预处理类
    """
    @staticmethod
    def _getSeparator(anyPath: PathLike):
        """
        获取一个路径中的分隔符.

        :param anyPath: 文件路径.
        :type anyPath: PathLike
        :return: 分隔符.
        :rtype: str
        """
        for sym in ["\\", "/"]:
            if sym in anyPath:
                return sym
            break
        raise RuntimeError(f"无法从路径中提取分隔符,请检测你的输入'{anyPath}'是否正确.")

    def _getLastDir(self, anyPath: PathLike | str):
        """
        获取路径的上级路径.

        :param anyPath: 路径.
        :type anyPath: PathLike
        :return: 上级路径.
        :rtype: PathLike
        """
        return (sym := self._getSeparator(anyPath)).join(anyPath.split(sym)[:-1])

    @staticmethod
    def mergeMutliDir(aimPath: PathLike | str, *args: PathLike | str, reserve: bool = True, info: bool = True) -> None:
        """
        将多个文件夹中的图片合并至一个文件夹中.

        :param aimPath: 合并后的文件夹名.
        :type aimPath: PathLike
        :param args: 当args传入单个目录时,默认将该目录下的子目录中的图像合并至新目录,为多个时则将多个文件夹内的文件移动至新目录.
        :type args: PathLike
        :keyword reserve: 是否保留被合并的文件夹.
        :type reserve: bool
        :return: 操作执行函数不做返回.
        :rtype: None
        """
        if not path.exists(aimPath): mkdir(aimPath)

        if len(args) == 1:
            # 需要将该目录的所有子文件夹中的图片合并至一个文件夹.
            for dirPath in listdir(lastPath := args[0]):
                dirPath = path.join(lastPath, dirPath)  # 子目录路径.

                for fileName in listdir(dirPath):
                    oldName = path.join(dirPath, fileName)  # 图片路径.
                    newName = path.join(aimPath, fileName)

                    copy(oldName, newName) if reserve else rename(oldName, newName)

                    print(f"{oldName} -> {newName}") if info else None

        else:
            for dirPath in args:  # 子目录路径.
                for fileName in listdir(dirPath):
                    oldName = path.join(dirPath, fileName)  # 图片路径.
                    newName = path.join(aimPath, fileName)

                    copy(oldName, newName) if reserve else rename(oldName, newName)

                    print(f"{oldName} -> {newName}") if info else None

    @staticmethod
    def separateChannel():
        """
        TODO: 将目录中不同通道数的图片分至不同文件夹.
        """
        pass

    @staticmethod
    def spawnLabel():
        """
        TODO: 对于文件夹中的每一个图片,根据其所在目录的名称进行重命名.
        """
        pass


@cache
def getDevice(*, info: bool = False):
    """
    根据CUDA是否可用获取训练方式.

    :return: device类.
    """
    if not is_available():
        warn("CUDA不可用,将使用CPU训练", SyntaxWarning) if info else None
        return device("cpu")

    print("检测到CUDA,将使用GPU训练") if info else None
    return device("cuda:0")


class dataset(Dataset):
    def __init__(self, relationDict: dict[PathLike, Annotated[str, "label"]] | list,
                 *, initMethod: dict = None, labelMethod: Callable = None, beforePath: PathLike | str = None,
                 labelToInt: dict[str, int] = None,
                 debug: bool | Literal["P", "W", "A"] = "P"):
        """
        可以被torch模型识别的dataset必须具有__getitem__和__len__魔术方法,根据情况还应有classes方法.

        :param relationDict: 关系字典,应形如{"path/to/you/img": "label", ...},
            在可以从路径中获取标签并且关键字`labelMethod`不为空时时,也接受形如["path/to/you/img", ...]的列表,
            此时将使用关键字参数`labelMethod`接收到的方法对列表进行处理得出字典.
        :type relationDict: dict
        :keyword initMethod: 图像预处理列表,应类似于{Resize: ((48, 48),), Grayscale: 1, method: args, ...}
        :type initMethod: dict
        :keyword labelMethod: 标签获取方法,类似dict([(i, labelMethod(i)) for i in relationDict]), (PS.仅当relationDict为list时)
        :type labelMethod: Callable
        :keyword beforePath: 如果获取完整路径比较麻烦,那么该参数将对每一个路径做`join(beforePath, path)`的处理.
            如`dataset(listdir(r'Path/to/your'), beforePath=r'C://xxx/xxx')`
        :type beforePath: PathLike
        :keyword labelToInt: 将所有文字标签按照键值关系转换成数字,所需的字典,应形如{"label": 1, ...}
        :type labelToInt: dict
        :keyword debug: 是否允许警告输出,当输入标识符时,'P': 不允许`print`输出, 'W': 不允许`warn`输出, 'A': 不允许任何输出.
        :type debug: bool | str
        """
        self._relationDict = relationDict
        self._initM = initMethod
        self._labelM = labelMethod
        self._debug = debug
        self._countLog = {}
        self._intDict = labelToInt
        self._path = beforePath
        self._pathList = list(self.lebelDict.keys())

    def __len__(self): return len(self._relationDict)

    def __getitem__(self, index):
        imgPath = self._pathList[index]
        newPath = None
        try:
            image = imgopen(imgPath)  # 打开对于序号的图片
        except FileNotFoundError as e:
            while True:
                try:
                    newPath = choice(self._pathList)
                    self.debugInfo("W", f"无法找到文件'{imgPath}',替换为'{newPath}'", SyntaxWarning)
                    image = imgopen(newPath)
                except FileNotFoundError as e:
                    continue
                else:
                    break

        if self._initM:
            if isinstance(self._initM, dict):
                for m in self._initM:
                    image = m(*self._initM[m])(image)
            else:
                raise TypeError(  # 图像归一化方法错误
                    f"关键字参数`initMethod`必须为字典类型(dict),而输入类型为'{type(self._relationDict).__name__}'!"
                )

        image = ToTensor()(image)

        label = self.lebelDict[imgPath if newPath is None else newPath]

        return image.to(getDevice()), Tensor([label]).to(getDevice())  # 返回张量化的图像和对应标签

    def debugInfo(self, method: Literal["P", "W"], *args: str | Warning, limit: int = 1) -> None:
        """
        带有开关的debug信息输出方法.

        :param method: 方法,"P": print, "W": warn.
        :type method: str
        :param args: 方法所需的参数.
        :type args: ...
        :keyword limit: 仅允许出现几次.(-1则不限制)
        :type limit: int
        :return: 操作执行函数不做返回
        :rtype: None
        """
        methodDict = {"P": print, "W": warn}

        if (arg := args[0]) in self._countLog:
            if self._countLog[arg] >= limit:
                return
            self._countLog[arg] += 1
        else:
            self._countLog.update([(arg, 1)])

        if isinstance(self._debug, str) and self._debug != "A":
            if self._debug != method:
                methodDict[method](  # debug信息输出
                    *args
                )
        else:
            if self._debug:
                methodDict[method](  # debug信息输出
                    *args
                )

    @property
    @errorLog()
    def lebelDict(self):
        """
        带有检测的标签自动获取的特性.
        """
        lDict = {}

        if isinstance(self._relationDict, list):
            if self._labelM:
                self.debugInfo("W",
                               f"该方法将使用方法`{self._labelM.__name__}`对列表中的每一个路径进行处理以获得标签(label)")

                for fileName in self._relationDict:

                    filePath = path.join(self._path, fileName) if self._path else fileName

                    if not path.exists(filePath):
                        self.debugInfo("W", f"文件'{filePath}'不存在!")
                        self._relationDict.pop(self._relationDict.index(fileName))
                        continue

                    label = self._labelM(fileName)

                    if self._intDict and label not in self._intDict:
                        self.debugInfo("W", f"键'{label}'不在字典'labelToInt'中.")

                    label = self._intDict[label] if self._intDict else label

                    lDict.update([(filePath, label)])

                tp = list(lDict.items())[0]  # 获取字典的第1个元组用于预览.

                if isinstance(tp[1], str) and not tp[1].isdigit():
                    self.debugInfo("W", f"标签'{tp[1]}'并非数字,这可能导致模型的某些程序错误")

                self.debugInfo("P", f"'路径-标签'字典预览: {{'{tp[0]}': '{tp[1]}'}}", limit=1)

                return lDict

            else:

                raise ValueError(  # 没有输入方法
                    f"当位置参数`relationDict`为列表类型(list)时,关键字参数`labelMethod`需要接收一个方法用于对列表中断每一个路径进行处理并获得标签(label),而这个方法需要使用者自己定义."
                )
        elif isinstance(self._relationDict, dict):

            return self._relationDict

        else:

            raise TypeError(  # 输入类型错误
                f"位置参数`relationDict`必须为字典类型(dict)或列表类型(list),而输入类型为'{type(self._relationDict).__name__}'!"
            )

    @property
    @errorLog()
    def classes(self): return list(set(self.lebelDict.values()))


class CNN(Module):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, epochs: int, batchSize: int, *, debug: bool = False):
        """
        :param epochs: 训练循环周期.
        :type epochs: int
        :param batchSize: 一个批次的大小.
        :type batchSize: int
        """
        super(CNN, self).__init__()

        self._count = 1  # 次数记录
        self._lastTime = time()  # 时间戳记录
        self._epochTime = time()

        self._epochs, self._batchSize = epochs, batchSize
        self._debug = debug

        self.conv1 = Sequential(
            Conv2d(1, 32, 3, 1, 1),
            BatchNorm2d(32),
            ReLU(),
            Dropout2d(0.25)
        )

        self.conv2 = Sequential(
            Conv2d(32, 64, 3, 1, 1),
            BatchNorm2d(64),
            ReLU(),
            Dropout2d(0.25)
        )

        self.conv3 = Sequential(
            Conv2d(64, 128, 3, 1, 1),
            BatchNorm2d(128),
            ReLU(),
            Dropout2d(0.25)
        )

        self.pool = MaxPool2d(2, 2)

        self.flatten = Flatten()

        self.fc1 = Linear(128 * 7 * 7, 128)

        self.fc2 = Linear(128, 10)

        self.order = [
            self.conv1,
            self.pool,
            self.conv2,
            self.pool,
            self.conv3,
            self.pool,
            self.flatten,
            self.fc1,
            self.fc2
        ]

        self.to(getDevice())

    @property
    @errorLog()
    def criterion(self):
        """
        损失函数
        """
        return CrossEntropyLoss().to(getDevice())

    @property
    @errorLog()
    def optimizer(self):
        """
        优化器
        """
        return Adam(self.parameters(), lr=0.001)

    @staticmethod
    def accuracy(predictions: Tensor, labels: Tensor):
        """
        正确率计算方法.

        :param predictions: 预测值
        :type predictions:
        :param labels:
        :type labels:
        :return:
        :rtype:
        """
        pred = torchmax(predictions.data, 1)[1]
        rights = pred.eq(labels.data.view_as(pred)).sum()
        return rights, len(labels)

    def forward(self, x: Tensor):
        """
        前向传播方法.

        :param x:
        :type x:
        :return:
        :rtype:
        """
        # TODO: 将该debug输出改完刷新式输出.
        # self.debug_info(f"第{self._count}次, 时间: [{datetime.now().time().strftime('%H:%M:%S')}], 耗时: <{time() - self._lastTime:.2f}> forward ---> ",
        #                 mode="P")
        temPrint(
            f"第{self._count}次, 时间: [{datetime.now().time().strftime('%H:%M:%S')}], 耗时: <{time() - self._lastTime:.2f}> forward {'-' * (self._count % 10)}> ")
        self._count += 1
        self._lastTime = time()

        for method in self.order:
            x = method(x)
        return x

    def debug_info(self, *args, mode: Literal["P", "W"] = "P") -> None:
        """
        debug信息输出.

        :param args: 参数
        :type args: ...
        :param mode: 模式, P: print, W: warn
        :type mode: str
        :return: 操作执行函数不做返回
        :rtype: None
        """
        modeDict = {"P": print, "W": warn}
        if self._debug:
            modeDict[mode](  # debug信息输出.
                *args
            )

    @errorLog()
    def begin_train(self, train_loader: DataLoader, valid_loader: DataLoader):
        """训练模型."""
        bestAcc = 0.0
        bestParam = None
        tAcc = 0

        for epoch in range(1, self._epochs):
            train_rights = []  # epoch结果记录

            for batch_idx, (trainData, trainTarget) in enumerate(train_loader):
                target = trainTarget.flatten().long()  # 展平操作,torch不允许标签张量超过1维.

                self.train()
                trainOutp = self(trainData)
                loss = self.criterion(trainOutp, target)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                trainRight = self.accuracy(trainOutp, target)
                train_rights.append(trainRight)

                if batch_idx % 50 == 0:
                    self.eval()
                    valid_rights = []

                    for validData, validTarget in valid_loader:
                        validOutp = self(validData)
                        validRight = self.accuracy(validOutp, validTarget)
                        valid_rights.append(validRight)

                    trainR: list[Tensor] = [sum(p) for p in partitem(train_rights)]
                    validR: list[Tensor] = [sum(p) for p in partitem(valid_rights)]

                    if validR[0] > bestAcc:  # 保存最好参数
                        bestAcc, bestParam = validR[0], self.state_dict()

                    spt = int(time() - self._epochTime)
                    hour = int(spt // 3600)
                    mit = int((spt % 3600) // 60)
                    sec = int((spt % 3600) % 60)
                    print(
                        f"\n{'-' * 40}\n当前epoch: {epoch} [{batch_idx}/{batch_size} ({100 * batch_idx / len(train_loader):.2f}%)]\n"
                        f"损失: {loss.data:.4f} 耗时: {'' if hour == 0 else f'{hour}时'}{mit}分{sec}秒\n"
                        f"训练集准确率: {(tAcc := (100 * trainR[0].cpu().clone().numpy() / trainR[1])):.2f}%\t测试集正确率: {100 * validR[0].cpu().clone().numpy() / validR[1]:.2f}%")

        save(bestParam, f"bestParam_{int(tAcc)}.pth")

    def testModel(self, pthPath: PathLike | str, testImgPath: PathLike | str):
        """
        随机提供一张图片至模型进行测试.

        :param pthPath: 参数存储文件路径(PS.一般为.pth后缀)
        :type pthPath: PathLike
        :param testImgPath: 测试的图片路径.
        :type testImgPath: PathLike
        :return:
        :rtype:
        """

        def checkFile(anyPath: PathLike | str):
            if not path.exists(anyPath):
                raise FileNotFoundError(  # 无法找到文件
                    f"文件'{anyPath}'不存在."
                )

        checkFile(pthPath)
        checkFile(testImgPath)

        with imgopen(testImgPath) as img:

            transform = Compose([
                Grayscale(),  # 通道数
                ToTensor(),
                Normalize(mean=[0.5], std=[0.5])
            ])

            img = transform(img).to(getDevice())
            img = img.unsqueeze(0)
            if list(img.shape) != [1, 1, 48, 48]:
                img = processimg(img, (48, 48), 1)

            output: Tensor = self(img)
            print(output, torchmax(output.data, 1))
            return torchmax(output.data, 1)[1].item()


if __name__ == '__main__':
    batch_size = 64  # 每一批次的数量
    labelDict = {"angry": 0, "disgust": 1, "fear": 2, "happy": 3, "neutral": 4, "sad": 5, "surprise": 6}

    trainSet = dataset(listdir(r"D:\xst_project_202212\Python\数据集\facial_expression\channel1\train\All"),
                       labelMethod=lambda x: x.split("_")[0],
                       beforePath=r"D:\xst_project_202212\Python\数据集\facial_expression\channel1\train\All",
                       labelToInt=labelDict, debug=True)

    validSet = dataset(listdir(r"D:\xst_project_202212\Python\数据集\facial_expression\channel1\valid\ALl"),
                       labelMethod=lambda x: x.split("_")[0],
                       beforePath=r"D:\xst_project_202212\Python\数据集\facial_expression\channel1\valid\All",
                       labelToInt=labelDict, debug=True)

    trainLoader, validLoader = DataLoader(trainSet, batch_size, shuffle=True), DataLoader(validSet, batch_size,
                                                                                          shuffle=True)
    net = CNN(5, batch_size, debug=True)

    net.begin_train(trainLoader, validLoader)  # type: ignore
    # print(net.testModel(r"D:\xst_project_202212\Python\privateProject\ImgAnalysis\bestParam1.pth",
    #                     r"D:\xst_project_202212\Python\数据集\facial_expression\channel1\test\sad\sad_15291.jpg"))
