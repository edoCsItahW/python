#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/8/23 17:02
# 当前项目名: Python
# 包名: 
# -------------------------<Lenovo>----------------------------
import os
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
import torch.optim as optim
import torchvision
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import transforms, models, datasets
import imageio
import time
import warnings
import random
import sys
import copy
import json
from PIL import Image

# 数据读取与预处理
data_dir = r"D:\xst_project_202212\Python\数据集\102种花卉\dataset"
train_dir = data_dir + r"\train"
valid_dir = data_dir + r"\valid"

# 预处理
# data_transforms中指定了所有图像预处理操作
# imagefolder假设每个文件夹下存储一类图片,文件夹的名字为分类的名字

# 数据增强(增多)
data_transforms = {
    "train": transforms.Compose([
        transforms.RandomRotation(45),  # 旋转45度,-45度到45随机旋转
        transforms.CenterCrop(224),  # 从中心开始裁剪
        transforms.RandomVerticalFlip(p=0.5),  # 随机垂直翻转
        transforms.RandomHorizontalFlip(p=0.5),  # 随机水平翻转
        transforms.ColorJitter(brightness=0.2, contrast=0.1, saturation=0.1, hue=0.1),  # 参1:亮度,参2:对比度,参3:饱和度,参4:色相
        transforms.RandomGrayscale(p=0.025),  # 概率转换为灰度率, 3通道为RGB
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 均值,标准差
    ]),
    "valid": transforms.Compose([
        transforms.CenterCrop(224),
        transforms.Resize(256),  # 调整大小
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
}

# batch数据
batch_size = 8
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ["train", "valid"]}
dataloaders = {x: DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True) for x in ["train", "valid"]}
dataset_size = {x: len(image_datasets[x]) for x in ["train", "valid"]}
class_names = image_datasets["train"].classes

# 读取标签实际名字
with open(r"D:\xst_project_202212\Python\数据集\102种花卉\cat_to_name.json", "r") as file:
    cat_to_name = json.load(file)


# 展示数据
# 注意转换回numpy的格式,而且还需要还原回标准化的结果
def im_convert(tensor):
    """展示数据"""
    image = tensor.to("cpu").clone().detach()
    image = image.numpy().squeeze()
    image = image.transpose(1, 2, 0)
    image = image * np.array((0.229, 0.224, 0.225) + np.array((0.485, 0.456, 0.406)))
    image = image.clip(0, 1)
    return image


fig = plt.figure(figsize=(20, 12))
columns = 4
rows = 2

dataiter = iter(dataloaders['valid'])
inputs, classes = dataiter.__next__()

for idx in range(columns * rows):
    ax = fig.add_subplot(rows, columns, idx + 1, xticks=[], yticks=[])
    ax.set_title(cat_to_name[str(int(class_names[classes[idx]]))])
    plt.imshow(im_convert(inputs[idx]))
plt.show()

model_name = "resnet"  # ["resnet", "alexnet", "vgg", "squeezenet", "densenet", "inception"]
# 是否使用预训练数据
feature_extract = True

# 是否使用GPU训练
train_on_gpu = torch.cuda.is_available()

if not train_on_gpu:
    warnings.warn("CUDA不可用,将使用CPU训练")
else:
    print("检测到CUDA,将使用GPU训练")

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False


model_ft = models.resnet152()


def initialize_model(model_name, num_classes, feature_extract, use_pretrained=True):
    # 选择适合的模型，不同的模型初始化参数不同
    model_ft = None
    input_size = 0

    if model_name == "resnet":
        """
        Resnet152
        """

        # 1. 加载与训练网络
        model_ft = models.resnet152(weights=use_pretrained)  # pretrained
        # 2. 是否将提取特征的模块冻住，只训练FC层
        set_parameter_requires_grad(model_ft, feature_extract)
        # 3. 获得全连接层输入特征
        num_frts = model_ft.fc.in_features
        # 4. 重新加载全连接层，设置输出102
        model_ft.fc = nn.Sequential(nn.Linear(num_frts, 102),  # <- 分多少类
                                    nn.LogSoftmax(dim=1))  # 默认dim = 0（对列运算），我们将其改为对行运算，且元素和为1
        input_size = 224

    elif model_name == "alexnet":
        """
        Alexnet
        """
        model_ft = models.alexnet(weights=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)

        # 将最后一个特征输出替换 序号为【6】的分类器
        num_frts = model_ft.classifier[6].in_features  # 获得FC层输入
        model_ft.classifier[6] = nn.Linear(num_frts, num_classes)
        input_size = 224

    elif model_name == "vgg":
        """
        VGG11_bn
        """
        model_ft = models.vgg16(weights=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_frts = model_ft.classifier[6].in_features
        model_ft.classifier[6] = nn.Linear(num_frts, num_classes)
        input_size = 224

    elif model_name == "squeezenet":
        """
        Squeezenet
        """
        model_ft = models.squeezenet1_0(weights=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        model_ft.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=(1, 1), stride=(1, 1))
        model_ft.num_classes = num_classes
        input_size = 224

    elif model_name == "densenet":
        """
        Densenet
        """
        model_ft = models.desenet121(weights=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)
        num_frts = model_ft.classifier.in_features
        model_ft.classifier = nn.Linear(num_frts, num_classes)
        input_size = 224

    elif model_name == "inception":
        """
        Inception V3
        """
        model_ft = models.inception_V(weights=use_pretrained)
        set_parameter_requires_grad(model_ft, feature_extract)

        num_frts = model_ft.AuxLogits.fc.in_features
        model_ft.AuxLogits.fc = nn.Linear(num_frts, num_classes)

        num_frts = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_frts, num_classes)
        input_size = 299

    else:
        print("无效名称,退出")
        exit()

    return model_ft, input_size


# 设置模型名字、输出分类数
model_ft, input_size = initialize_model(model_name, 102, feature_extract, use_pretrained=True)

# GPU 计算
model_ft = model_ft.to(device)

# 模型保存, checkpoints 保存是已经训练好的模型，以后使用可以直接读取
filename = 'checkpoint.pth'

# 是否训练所有层
params_to_update = model_ft.parameters()
# 打印出需要训练的层
print("需要学习的层:")
if feature_extract:
    params_to_update = []
    for name, param in model_ft.named_parameters():
        if param.requires_grad:
            params_to_update.append(param)
            print("\t", name)
else:
    for name, param in model_ft.named_parameters():
        if param.requires_grad:
            print("\t", name)

# 优化器设置
optimizer_ft = optim.Adam(params_to_update, lr=1e-2)
# 学习率衰减策略
scheduler = optim.lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)
# 学习率每7个epoch衰减为原来的1/10
# 最后一层使用LogSoftmax(), 故不能使用nn.CrossEntropyLoss()来计算

criterion = nn.NLLLoss()


# 训练模块
# is_inception：要不要用其他的网络
def train_model(model, dataloaders, criterion, optimizer, num_epochs=10, is_inception=False, filename=filename):
    since = time.time()
    # 保存最好的准确率
    best_acc = 0
    """
    checkpoint = torch.load(filename)
    best_acc = checkpoint['best_acc']
    model.load_state_dict(checkpoint['state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    model.class_to_idx = checkpoint['mapping']
    """
    # 指定用GPU还是CPU
    model.to(device)
    # 下面是为展示做的
    val_acc_history = []
    train_acc_history = []
    train_losses = []
    valid_losses = []
    LRs = [optimizer.param_groups[0]['lr']]
    # 最好的一次存下来
    best_model_wts = copy.deepcopy(model.state_dict())

    for epoch in range(num_epochs):
        print(f'\n任务进展:{epoch}/{num_epochs - 1}')
        print('-' * 10)

        # 训练和验证
        for phase in ['train', 'valid']:
            if phase == 'train':
                model.train()  # 训练
            else:
                model.eval()  # 验证

            running_loss = 0.0
            running_corrects = 0

            # 把数据都取个遍
            for inputs, labels in dataloaders[phase]:
                # 下面是将inputs,labels传到GPU
                inputs = inputs.to(device)
                labels = labels.to(device)

                # 清零
                optimizer.zero_grad()
                # 只有训练的时候计算和更新梯度
                with torch.set_grad_enabled(phase == 'train'):
                    # if这面不需要计算，可忽略
                    if is_inception and phase == 'train':
                        outputs, aux_outputs = model(inputs)
                        loss1 = criterion(outputs, labels)
                        loss2 = criterion(aux_outputs, labels)
                        loss = loss1 + 0.4 * loss2
                    else:  # resnet执行的是这里
                        outputs = model(inputs)
                        loss = criterion(outputs, labels)

                        # 概率最大的返回preds
                    _, preds = torch.max(outputs, 1)

                    # 训练阶段更新权重
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # 计算损失
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            # 打印操作
            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            time_elapsed = time.time() - since
            print(f'耗时:{time_elapsed // 60}分{time_elapsed % 60}秒')
            print(f'{phase}的损失值: {epoch_loss} Acc: {epoch_acc}')

            # 得到最好那次的模型
            if phase == 'valid' and epoch_acc > best_acc:
                best_acc = epoch_acc
                # 模型保存
                best_model_wts = copy.deepcopy(model.state_dict())
                state = {
                    # tate_dict变量存放训练过程中需要学习的权重和偏执系数
                    'state_dict': model.state_dict(),
                    'best_acc': best_acc,
                    'optimizer': optimizer.state_dict(),
                }
                torch.save(state, filename)
            if phase == 'valid':
                val_acc_history.append(epoch_acc)
                valid_losses.append(epoch_loss)
                scheduler.step(epoch_loss)
            if phase == 'train':
                train_acc_history.append(epoch_acc)
                train_losses.append(epoch_loss)

        print(f'优化器学习率:{optimizer.param_groups[0]["lr"]}')
        LRs.append(optimizer.param_groups[0]['lr'])

    time_elapsed = time.time() - since
    print(f'训练耗时{time_elapsed // 60}m {time_elapsed % 60}s')
    print(f'最佳值: {best_acc}')

    # 保存训练完后用最好的一次当做模型最终的结果
    model.load_state_dict(best_model_wts)
    return model, val_acc_history, train_acc_history, valid_losses, train_losses, LRs


# 若太慢，把epoch调低，迭代50次可能好些
# 训练时，损失是否下降，准确是否有上升；验证与训练差距大吗？若差距大，就是过拟合
model_ft, val_acc_history, train_acc_history, valid_losses, train_losses, LRs = train_model(model_ft, dataloaders,
                                                                                            criterion, optimizer_ft,
                                                                                            num_epochs=20,
                                                                                            is_inception=(
                                                                                                    model_name == "inception"))

# 将全部网络解锁进行训练
for param in model_ft.parameters():
    param.requires_grad = True

# 再继续训练所有的参数，学习率调小一点\
optimizer = optim.Adam(params_to_update, lr=1e-4)
scheduler = optim.lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

# 损失函数
criterion = nn.NLLLoss()

# 加载保存的参数
# 并在原有的模型基础上继续训练
# 下面保存的是刚刚训练效果较好的路径
checkpoint = torch.load(filename)
best_acc = checkpoint['best_acc']
model_ft.load_state_dict(checkpoint['state_dict'])
optimizer.load_state_dict(checkpoint['optimizer'])

model_ft, val_acc_history, train_acc_history, valid_losses, train_losses, LRs = train_model(model_ft, dataloaders,
                                                                                            criterion, optimizer,
                                                                                            num_epochs=10,
                                                                                            is_inception=(
                                                                                                        model_name == "inception"))

model_ft, input_size = initialize_model(model_name, 102, feature_extract, use_pretrained=True)

# GPU 模式
model_ft = model_ft.to(device)  # 扔到GPU中

# 保存文件的名字
filename = 'checkpoint.pth'

# 加载模型
checkpoint = torch.load(filename)
best_acc = checkpoint['best_acc']
model_ft.load_state_dict(checkpoint['state_dict'])


def process_image(image_path):
    # 读取测试集数据
    img = Image.open(image_path)
    # Resize, thumbnail方法只能进行比例缩小，所以进行判断
    # 与Resize不同
    # resize()方法中的size参数直接规定了修改后的大小，而thumbnail()方法按比例缩小
    # 而且对象调用方法会直接改变其大小，返回None
    if img.size[0] > img.size[1]:
        img.thumbnail((10000, 256))
    else:
        img.thumbnail((256, 10000))

    # crop操作， 将图像再次裁剪为 224 * 224
    left_margin = (img.width - 224) / 2  # 取中间的部分
    bottom_margin = (img.height - 224) / 2
    right_margin = left_margin + 224  # 加上图片的长度224，得到全部长度
    top_margin = bottom_margin + 224

    img = img.crop((left_margin, bottom_margin, right_margin, top_margin))

    # 相同预处理的方法
    # 归一化
    img = np.array(img) / 255
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    img = (img - mean) / std

    # 注意颜色通道和位置
    img = img.transpose((2, 0, 1))

    return img


def imshow(image, ax=None, title=None):
    """展示数据"""
    if ax is None:
        fig, ax = plt.subplots()

    # 颜色通道进行还原
    image = np.array(image).transpose((1, 2, 0))

    # 预处理还原
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    image = std * image + mean
    image = np.clip(image, 0, 1)

    ax.imshow(image)
    ax.set_title(title)

    return ax


image_path = r'D:\xst_project_202212\Python\数据集\102种花卉\dataset\valid\3\image_06621.jpg'
img = process_image(image_path)  # 我们可以通过多次使用该函数对图片完成处理
imshow(img)

# 得到一个batch的测试数据
dataiter = iter(dataloaders['valid'])
images, labels = dataiter.__next__()

model_ft.eval()

if train_on_gpu:
    # 前向传播跑一次会得到output
    output = model_ft(images.cuda())
else:
    output = model_ft(images)

# batch 中有8 个数据，每个数据分为102个结果值， 每个结果是当前的一个概率值
print(output.shape)

_, preds_tensor = torch.max(output, 1)

preds = np.squeeze(preds_tensor.numpy()) if not train_on_gpu else np.squeeze(
    preds_tensor.cpu().numpy())  # 将秩为1的数组转为 1 维张量

fig = plt.figure(figsize=(20, 20))
columns = 4
rows = 2

for idx in range(columns * rows):
    ax = fig.add_subplot(rows, columns, idx + 1, xticks=[], yticks=[])
    plt.imshow(im_convert(images[idx]))
    ax.set_title(f"{cat_to_name[str(preds[idx])]} ({cat_to_name[str(labels[idx].item())]})",
                 color=("green" if cat_to_name[str(preds[idx])] == cat_to_name[str(labels[idx].item())] else "red"))
plt.show()
# 绿色的表示预测是对的，红色表示预测错了
