#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/23 0:09
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
import torch
import torch.optim as optim
import warnings
warnings.filterwarnings("ignore")

features = pd.read_csv(r"D:\xst_project_202212\Python\privateProject\MachineLearning\dataSpider\csv数据库\过滤房产数据.csv")

# print(features.head())
# 独热编码  将字符串项进行编码
# features = pd.get_dummies(features)
# print(features.head())

labels = np.array(features["y项"])

# 在特征中去掉标签
features = features.drop("y项", axis=1)

# 保存一下名字,以备后患
feature_list = list(features.columns)

# 转换为合适的格式
features = np.array(features)

# 标志化操作
input_features = preprocessing.StandardScaler().fit_transform(features)

# 构建网络模型
x, y = torch.tensor(input_features), torch.tensor(labels)

# 初始化权重
weights = torch.randn((14, 128), requires_grad=True)  # requires_grad自动求导
biases = torch.randn(128, requires_grad=True)

weights2 = torch.randn((128, 1), requires_grad=True)
biases2 = torch.randn(1, requires_grad=True)

# 学习率
learn_rate = 0.01
lossers = []

for i in range(1000):
    # 计算隐藏层
    hidden = torch.mm(x, weights) + biases

    # 加入激活函数
    hidden = torch.relu(hidden)

    # 预测结果
    predictions = torch.mm(hidden, weights2) + biases2

    # 计算损失
    loss = torch.mean((predictions - y) ** 2)
    lossers.append(loss.data.numpy())

    # 打印损失值
    if i % 100 == 0:
        print("loss:", loss)

    # 计算反向传播
    loss.backward()

    # 更新参数
    weights.data.add_(- learn_rate * weights.grad.data)
    biases.data.add_(-learn_rate * biases.grad.data)
    weights2.data.add_(- learn_rate * weights2.grad.data)
    biases2.data.add_(-learn_rate * biases2.grad.data)

    # 清空
    weights.grad.data.zero_()
    biases.grad.data.zero_()
    weights2.grad.data.zero_()
    biases2.grad.data.zero_()


# 简单搭建
input_size = input_features.shape[1]
hidden_size = 128
output_size = 1
batch_size = 16
my_nn = torch.nn.Sequential(
    torch.nn.Linear(input_size, hidden_size),
    torch.nn.Sigmoid(),
    torch.nn.Linear(hidden_size, output_size)
)

cost = torch.nn.MSELoss(reduction="mean")
optimizer = torch.optim.Adam(my_nn.parameters(), lr=0.001)

# 训练网络
losses = []
for i in range(1000):
    batch_loss = []
    for start in range(0, len(input_features), batch_size):
        end = start + batch_size if start + batch_size < len(input_features) else len(input_features)
        xx = torch.tensor(input_features[start: end], requires_grad=True)
        yy = torch.tensor(labels[start: end], requires_grad=True)
        predictions = my_nn(xx)
        loss = cost(predictions, yy)
        optimizer.zero_grad()
        loss.backward(retain_graph=True)
        optimizer.step()
        batch_loss.append(loss.data.numpy())

    # 打印损失值
    if i % 100 == 0:
        losses.append(np.mean(batch_loss))
        print(i, np.mean(batch_loss))

# 预测结果
x = torch.tensor(input_features)
predict = my_nn(x).data.numpy()


# 分类任务
import pickle
import gzip

x_train, y_train, y_valid = np.array(list(range(10))), np.array(list(range(10))), np.array(list(range(10)))

plt.imshow(x_train[0].reshape((28, 28)), cmap="gray")


# 784个输入层,128个隐藏层,10个输出层
# 转tensor
x_train, y_train, y_valid = map(torch.tensor, (x_train, y_train, y_valid))
x_valid = torch.tensor([1, 1])
n, c = x_train.shape

# 如果模型有可学习参数用torch.nn.Module,其它情况torch.nn.functional
import torch.nn.functional as func

loss_func = func.cross_entropy

bs = 64
xb, yb = x_train[0: bs], y_train[0: bs]
weights = torch.randn([784, 10], dtype=torch.float, requires_grad=True)
bias = torch.zeros(10, requires_grad=True)


def model(xb): return torch.mm(xb, weights) + bias


print(loss_func(model(xb), yb))  # 损失值

# 创建一个mode来简化代码
from torch import nn


class Minst_NN(nn.Module):
    def __init__(self):
        super().__init__()
        self.heidden1 = nn.Linear(784, 128)  # 隐藏层784输入,128输出
        self.heidden2 = nn.Linear(128, 256)
        self.out = nn.Linear(256, 10)

    def forward(self, x):
        x = func.relu(self.heidden1(x))
        x = func.relu(self.heidden2(x))
        x = self.out(x)
        return x


net = Minst_NN()
print(net)


# 打印权重和偏置项
for name, paramter in net.named_parameters():
    print(name, paramter, paramter.size())


# 构建数据
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

train_ds = TensorDataset(x_train, y_train)
train_d1 = DataLoader(train_ds, batch_size=bs, shuffle=True)

valid_ds = TensorDataset(x_valid, y_valid)
valid_d1 = DataLoader(valid_ds, batch_size=bs * 2)


def get_data(train_ds, valid_ds, bs):
    return (
        DataLoader(train_ds, batch_size=bs, shuffle=True),
        DataLoader(valid_ds, batch_size=bs * 2)
    )


def loss_batch(model, loss_func, xb, yb, opt=None):
    loss = loss_func(model(xb), yb)

    if opt is not None:
        loss.backward()
        opt.step()
        opt.zero_grad()

    return loss.item(), len(xb)


def fit(steps, model, loss_func, opt, train_dl, valid_dl):
    for step in range(steps):
        model.train()
        for xb, yb in train_dl:
            loss_batch(model, loss_func, xb, yb, opt)

        model.eval()
        with torch.no_grad():
            losses, nums = zip(
                *[loss_batch(model, loss_func, xb, yb) for xb, yb in valid_dl]
            )
        val_loss = np.sum(np.multiply(losses, nums)) / np.sum(nums)
        print("当前step:" + str(step), "验证集损失:" + str(val_loss))


from torch import optim


def get_mode():
    model = Minst_NN()
    return model, optim.SGD(model.parameters(), lr=0.001)

