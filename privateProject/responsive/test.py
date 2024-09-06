#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/8/27 上午1:44
# 当前项目名: ansiDefine.py
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from sys import argv, exit
from reactive import Ref, Effect


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reactive")
        self.counter = Ref(0)

        self.centralWidget = QWidget(self)

        self.button = QPushButton("Click me", self.centralWidget)
        self.button.clicked.connect(self.increase)
        self.sc = QLabel(str(self.counter.value), self.centralWidget)
        render = Effect(self.print)
        render()

    @Effect
    def increase(self):
        self.counter.value += 1

    def print(self):
        print(f"Counter: {self.counter.value}")
        self.sc.setText(str(self.counter.value))


if __name__ == '__main__':
    app = QApplication(argv)
    # with open(r"./static/qss/style.qss", "r", encoding="utf-8") as file:
    #     style = file.read()
    main = mainWindow()
    # main.setStyleSheet(style)
    main.show()
    exit(app.exec())

