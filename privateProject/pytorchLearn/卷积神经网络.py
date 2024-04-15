#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/23 15:05
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
from torch import max
from torch.nn import Module, Sequential, Conv2d, ReLU, MaxPool2d, Linear, CrossEntropyLoss
from torch.optim import Adam
from os import listdir
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image


trianpath = r"D:\xst_project_202212\Python\数据集\手写数字图片MNIST\训练集\all"
testpath = r"D:\xst_project_202212\Python\数据集\手写数字图片MNIST\测试集\all"

# 定义超参数
input_size = 28  # 图像总尺寸28 * 28
num_classes = 10  # 标签种类数
mun_epochs = 3  # 训练的总循环周期
batch_size = 64  # 一个批次的大小, 64张图片


class mydataset(Dataset):
    def __init__(self, imgpath: list, transfrom=None):
        self.imgpath = imgpath
        self.transfrom = transfrom

    def __len__(self): return len(self.imgpath)

    def __getitem__(self, index):
        imgpath = self.imgpath[index]
        image = Image.open(imgpath)

        if self.transfrom is not None:
            image = self.transfrom(image)

        label = int(imgpath.split("\\")[-1].split("_")[0])

        return image, label


trainlist = [fr"{trianpath}\{imgpath}" for imgpath in listdir(trianpath)]
testlist = [fr"{testpath}\{imgpath}" for imgpath in listdir(testpath)]


# 训练集
train_dataset = mydataset(trainlist, transfrom=transforms.ToTensor())

# 测试集
test_dataset = mydataset(testlist, transfrom=transforms.ToTensor())

# 构建batch数据
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

# print(train_loader)


# 构建卷积模块
class CNN(Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = Sequential(  # 输入大小(1, 28, 28)
            Conv2d(  # <- 卷积层
                in_channels=1,  # 灰度图
                out_channels=16,  # 要得到多少个特征图/要用多少卷积核
                kernel_size=5,  # 卷积核大小
                stride=1,  # 步长
                padding=2  # 边界填充  如果希望卷积后大小和原来一样,需要设置padding=(kernel_size-1)/2 if stride=1
            ),  # 输出的特征图为(16, 28, 28)
            ReLU(),  # relu层  <- 激活层
            MaxPool2d(kernel_size=2)  # 进行池化操作 (2x2 区域), 输出结果为: (16, 14, 14)  <- 池化层
        )
        self.conv2 = Sequential(  # 下一个输入
            Conv2d(16, 32, 5, 1, 2),  # 输出(32, 14, 14)
            ReLU(),  # relu层
            MaxPool2d(2),  # 输出(32, 7, 7)
        )
        self.out = Linear(32 * 7 * 7, 10)  # 全连接层得到的结果

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)  # flatten操作,结果为(batch_size, 32 * 7 * 7)
        out = self.out(x)
        return out


# 准确率评估
def accuracy(predictions, labels):
    pred = max(predictions.data, 1)[1]
    rights = pred.eq(labels.data.view_as(pred)).sum()
    return rights, len(labels)


# 实例化
net = CNN()
# 损失函数
criterion = CrossEntropyLoss()
# 优化器
optimizer = Adam(net.parameters(), lr=0.001)  # 定义优化器, 普通的随机梯度下降算法


# 训练网络模型
for epoch in range(mun_epochs):
    # 保存当前epoch结果
    train_rights = []

    for batch_idx, (data, target) in enumerate(train_loader):  # 针对容器中的每一个批次进行循环
        net.train()
        print(target)
        outp = net(data)
        loss = criterion(outp, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        right = accuracy(outp, target)
        train_rights.append(right)

        if batch_idx % 100 == 0:

            net.eval()
            val_rights = []

            for data, target in test_loader:
                outp = net(data)
                right = accuracy(outp, target)
                val_rights.append(right)

            # 准确率计算
            train_r = (sum([tup[0] for tup in train_rights]), sum([tup[1] for tup in train_rights]))
            val_r = (sum([tup[0] for tup in val_rights]), sum([tup[1] for tup in val_rights]))

            print(f"当前epcho: {epoch} [{batch_idx * batch_size}/{len(train_loader.dataset)} ({100 * batch_idx / len(train_loader)}%)]\n"
                  f"损失:{loss.data}\n"
                  f"训练集准确率:{100 * train_r[0].numpy() / train_r[1]}%\t测试集准确率:{100 * val_r[0].numpy() / val_r[1]}%\n")
