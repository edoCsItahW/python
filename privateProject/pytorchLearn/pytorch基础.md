pytorch
===
---

```python
import numpy as np
import torch

# import numpy as np
#
# # 创建矩阵
# ten = torch.empty(5, 3)
# # print(ten)
#
# # 随机值
# num = torch.rand(5, 3)
# # print(num)
#
# # 全零矩阵
# mat = torch.zeros(5, 3, dtype=torch.long)
# # print(mat)
#
# # 直接传入数据
# ten = torch.tensor([5.5, 3])
# # print(ten)
#
# ten = ten.new_ones(5, 3, dtype=torch.double)
# # print(ten)
#
# ten = torch.randn_like(ten, dtype=torch.float)
# # print(ten)
#
# # 展示矩阵大小
# # print(ten.size())
#
# # 加法
# y = torch.rand(5, 3)
# # print(ten + y)
# # print(torch.add(ten, y))
#
# # 索引
# # print(ten[:, 1])
#
# # 改变维度
# x = torch.randn(4, 4)
# y = x.view(16)
# z = x.view(-1, 8)
# # print(x.size(), y.size(), z.size())
#
# # 转numpy
# a = torch.ones(5, 5)
# b = a.numpy()
# # print(b)
#
# # numpy转torch
# a = np.ones(5)
# b = torch.from_numpy(a)
# print(b)

# # 开始实践反向传播
# x = torch.randn(3, 4, requires_grad=True)  # 是否可求导
#
# b = torch.randn(3, 4, requires_grad=True)
#
# t = x + b
# y = t.sum()
# print(y)
# y.backward()
# print(b.grad)

import torch.nn as nn
import torch
import numpy as np
import matplotlib.pyplot as plt

# 线性回归
x_values = [i for i in range(11)]
x_train = torch.tensor(x_values, dtype=torch.float32).view(-1, 1)
print(x_train.shape)

y_values = [(2 * i + 1) for i in x_values]
y_train = torch.tensor(y_values, dtype=torch.float32).view(-1, 1)
print(y_train.shape)


class LinearRegressionModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        out = self.linear(x)
        return out


model = LinearRegressionModel(1, 1)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

losses = []

for epoch in range(1000):
    epoch += 1
    inputs = x_train.to(device)
    labels = y_train.to(device)

    optimizer.zero_grad()

    outputs = model(inputs)

    loss = criterion(outputs, labels)
    losses.append(loss.item())

    loss.backward()

    optimizer.step()
    if epoch % 50 == 0:
        print(f"epoch:{epoch}\nloss:{loss.item()}")

predicted = model(x_train.to(device)).data.cpu().numpy()
print(predicted)

# 可视化
plt.plot(losses)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.show()

plt.scatter(x_train.numpy(), y_train.numpy(), color='blue', label='Actual')
plt.plot(x_train.numpy(), predicted, color='red', label='Predicted')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression')
plt.legend()
plt.show()

torch.save(model.state_dict(), "model.pk1")
model.load_state_dict(torch.load('model.pk1'))

```
一个值为scalar
```doctest
x = tensor(42.)
x.dim()
2 * x
x.item()
```
向量(表特征)Vector
```doctest
v = tensor[1.5, -0.5, 3.0]
v.dim()
v.size()
```
矩阵Matrix
```doctest
m = tensor([1., 2.], [3., 4.])
m.matmul(m)
tensor([1., 0.]).matmul(m)
m * m
tensor([1., 2.]).matmul(m)
```

