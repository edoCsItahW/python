#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

import torch.nn as nn
import torch
import numpy as np
import matplotlib.pyplot as plt
import random
# print(torch.version.__version__)
# torch.hub.list('pytorch/vision')

# 线性回归
x_values = [i for i in range(11)]
x_train = torch.tensor(x_values, dtype=torch.float32).view(-1, 1)
print(x_train.shape)

y_values = [2 ** i + 1 for i in x_values]
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
print("predicted", predicted)

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

# torch.save(model.state_dict(), "model.pk1")
# model.load_state_dict(torch.load('model.pk1'))
