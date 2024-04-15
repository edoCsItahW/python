#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/26 20:53
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
from torchvision.transforms import Compose, ToTensor, Normalize, Grayscale
from MachineLearningTools import dataloader
from torch.optim import Adam
from figureTools import processimg
from systemTools import fullpath
from PIL.Image import open as imgopen
from torch.nn import Module, Sequential, Conv2d, ReLU, MaxPool2d, Linear, CrossEntropyLoss
from confunc import partitem
from torch import save, load, max as torchmax

trianpath = r"D:\xst_project_202212\Python\数据集\手写数字图片MNIST\训练集\all"
testpath = r"D:\xst_project_202212\Python\数据集\手写数字图片MNIST\测试集\all"

triandir = {k: k.split("\\")[-1].split("_")[0] for k in fullpath(trianpath)}  # dict['文件路径': '文件标签']
testdir = {k: k.split("\\")[-1].split("_")[0] for k in fullpath(testpath)}


class netparam:
    def __init__(self, insize: tuple, in_channels: int, out_channels: list, kernel_size: int, stride: int, padding: int,
                 poolk: list):
        self.insize = insize  # 输入图片的尺寸
        self.inChannels = in_channels  # 输入图片的通道数
        self.outChannels = out_channels  # 要求输出图片的通道数
        self.kernel = kernel_size  # 卷积核大小
        self.stride = stride  # 卷积步长
        self.padding = padding  # 边界格数
        self.poolk = poolk  # 池化层通道数
        self._max = len(out_channels) + len(poolk)
        self._current = 0

    def _size(self):
        sizew, sizeh = self.insize  # 图片长,高
        for out, k in zip(self.outChannels, self.poolk):
            sizew = (sizew - self.kernel + 2 * self.padding) / self.stride + 1
            sizeh = (sizeh - self.kernel + 2 * self.padding) / self.stride + 1
            sizew, sizeh = (sizew / k, sizeh / k)
        return self.outChannels[-1] * sizew * sizeh

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < self._max:
            self._current += 1
            return [self.inChannels if self._current == 1 else self.outChannels[(self._current // 2) - 1], self.outChannels[(self._current - 1) // 2], self.kernel, self.stride, self.padding] \
                if (self._current - 1) % 2 == 0 else self.poolk[(self._current - 1) // 2]
        elif self._current == self._max:
            return int(self._size())


# 定义模型
class CNN(Module):
    def __init__(self, datainfo: tuple[str, str], batchSize: int, alpha: int | float, times: int, *,
                 param: netparam, size: tuple, channel: int):
        super(CNN, self).__init__()
        self.param = param
        self.size = size
        self.channel = channel

        # 层
        self.covn1 = Sequential(
            Conv2d(*(self.param.__next__())),
            ReLU(),
            MaxPool2d(self.param.__next__())
        )
        self.covn2 = Sequential(
            Conv2d(*self.param.__next__()),
            ReLU(),
            MaxPool2d(self.param.__next__())
        )
        self.out = Linear(self.param.__next__(), 10)

        # 损失函数和优化函数
        self.lossfunc = CrossEntropyLoss()
        self.optimizer = Adam(self.parameters(), lr=0.001)

        # 参数
        self.batchSize = batchSize
        self.alpha = alpha
        self.times = times

        # 数据
        self.traindir = self.formatDir(datainfo[0])
        self.testdir = self.formatDir(datainfo[1])
        self.trainloader = dataloader(self.traindir, self.size, self.channel, batchSize=self.batchSize, shuffle=True)()
        self.testloader = dataloader(self.testdir, self.size, self.channel, batchSize=self.batchSize, shuffle=True)()

    def forward(self, xtensor):
        """
        前向传播.

        :param xtensor:
        :type xtensor:
        :return:
        :rtype:
        """
        x = self.covn1(xtensor)
        x = self.covn2(x)
        x = x.view(x.size(0), -1)
        xout = self.out(x)
        return xout

    @staticmethod
    def formatDir(dirPath: str): return {k: k.split("\\")[-1].split("_")[0] for k in fullpath(dirPath)}

    @staticmethod
    def prediction(lossy, ylabel):
        """
        该函数主要用于计算模型的准确率。具体解释如下：

        pred = torch.max(lossy.data, 1)[1]:
        使用torch.max()函数计算在第1个维度上的最大值，并返回最大值的索引。
        这里的lossy是一个张量，表示模型的预测结果。
        lossy.data表示张量lossy的数据部分，1表示在第1个维度上进行计算。[1]表示返回最大值的索引部分。

        pred.eq(ylabel.data.view_as(pred)):
        使用.eq()函数比较pred和ylabel.data.view_as(pred)的元素是否相等。
        ylabel是一个张量，表示目标值。ylabel.data表示张量ylabel的数据部分。
        .view_as(pred)表示将ylabel.data的形状调整为与pred相同。

        pred.eq(ylabel.data.view_as(pred)).sum():
        使用.sum()函数计算布尔值张量中值为True的元素个数，即正确预测的样本个数。

        return rights, len(ylabel):
        返回正确预测的样本个数rights和ylabel的长度，即总样本个数。
        """
        pred = torchmax(lossy.data, 1)[1]
        rights = pred.eq(ylabel.data.view_as(pred)).sum()
        return rights, len(ylabel)

    def begintrain(self):
        bastacc = 0.0
        bestparam = None

        for epoch in range(self.times):
            trainLog = []

            for batch_idx, (batchX, Y) in enumerate(self.trainloader):
                self.train()
                outdata = self(batchX)
                loss = self.lossfunc(outdata, Y)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                rightY = self.prediction(outdata, Y)
                trainLog.append(rightY)

                if batch_idx % 100 == 0:
                    self.eval()
                    rightvals = []

                    for testX, testY in self.testloader:
                        outdata = self(testX)
                        rightval = self.prediction(outdata, testY)
                        rightvals.append(rightval)

                    part1, part2 = partitem(trainLog)
                    part3, part4 = partitem(rightvals)
                    trainR, varR = (sum(part1), sum(part2)), (sum(part3), sum(part4))

                    if varR[0] > bastacc:
                        bastacc = varR[0]
                        bestparam = self.state_dict()

                    print(
                        f"当前进度:{epoch} [{batch_idx * self.batchSize}/{len(self.trainloader.dataset)} ({(100 * batch_idx / len(self.trainloader)):.2f}%)]\n"
                        f"损失:{loss.data:.4f}\n"
                        f"训练集准确率:{(100 * trainR[0].numpy() / trainR[1]):.2f}%\t测试集准确率:{(100 * varR[0].numpy() / varR[1]):.2f}%\n{'-' * 20}")

        save(bestparam, "foot.pth")


class testmodel:
    def __init__(self, model: Module, path: str = "foot.pth", imagepath: str = None):
        self.model = model
        self.path = path
        self.img = imgopen(imagepath)

    def test(self):
        self.model.load_state_dict(load(self.path))

        transform = Compose([
            Grayscale(num_output_channels=1),
            ToTensor(),
            Normalize(mean=[0.5], std=[0.5])
        ])

        img = transform(self.img).unsqueeze(0)
        if list(img.shape) != [1, 1, 48, 48]:
            img = processimg(self.img)

        output = self.model(img)

        _, predicted = torchmax(output.data, 1)
        return predicted.item()


if __name__ == '__main__':
    triandir, testdir = r"D:\xst_project_202212\Python\数据集\facial_expression\test\angry\channel1", r"D:\xst_project_202212\Python\数据集\facial_expression\train\angry"
    data = netparam((48, 48), 1, [16, 32], 5, 1, 2, [2, 2])
    net = CNN((trianpath, testpath), 64, 1e-3, 3, param=data, size=(48, 48), channel=1)
    # net.begintrain()
    test = testmodel(net, imagepath=r"D:\xst_project_202212\Python\数据集\facial_expression\train\angry\4288Exp0annoyed_face_130.jpg")
    print(test.test())

