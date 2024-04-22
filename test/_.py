#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/22 上午8:39
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt


class CenteredWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建一个要居中的 QWidget
        centered_widget = QWidget()

        # 设置 QWidget 的尺寸策略为水平和垂直方向上的首选大小
        centered_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))

        # 创建一个水平布局，并添加 QWidget 到其中
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(centered_widget)
        horizontal_layout.addStretch(1)  # 添加一个伸缩因子以在右侧创建空间

        # 将水平布局添加到主布局中
        main_layout.addLayout(horizontal_layout)


if __name__ == "__main__":
    app = QApplication([])
    window = CenteredWidget()
    window.show()
    app.exec()