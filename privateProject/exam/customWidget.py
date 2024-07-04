#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/6/29 上午11:08
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import QPropertyAnimation, pyqtProperty
from sys import argv, exit
from random import randint


"""
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QSizePolicy  
from PyQt6.QtGui import QColor  
from PyQt6.QtCore import QTimer, Qt  
from sys import argv, exit  
  
  
class Example(QWidget):  
  
    def __init__(self):  
        super().__init__()  
  
        self.initUI()  
  
    def initUI(self):  
        hbox = QHBoxLayout(self)  
  
        self.button = QPushButton("Start", self)  
        self.button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  
        hbox.addWidget(self.button)  
  
        hbox.addSpacing(40)  
  
        self.btn = QPushButton("Summer")  
        font = self.btn.font()  
        font.setPointSize(35)  
        self.btn.setFont(font)  
        self.btn.setStyleSheet("background-color: red;")  # 初始背景颜色  
        hbox.addWidget(self.btn)  
  
        self.animation_timer = QTimer(self)  
        self.animation_timer.timeout.connect(self.animate_background)  
  
        self.start_color = QColor(255, 0, 0)  
        self.end_color = QColor(0, 255, 0)  
        self.current_color = self.start_color  
        self.step = 1  # 颜色改变的步长，可以调整以改变动画速度  
  
        self.button.clicked.connect(self.start_animation)  
  
        self.setGeometry(300, 300, 380, 250)  
        self.setWindowTitle('Color anim')  
        self.show()  
  
    def start_animation(self):  
        if self.current_color == self.start_color:  
            self.animation_direction = 1  
        else:  
            self.animation_direction = -1  
        self.animation_timer.start(10)  # 每10毫秒触发一次timeout信号  
  
    def animate_background(self):  
        r, g, b, _ = self.current_color.getRgb()  
        r += self.step * self.animation_direction  
        g += self.step * self.animation_direction  
        b += self.step * self.animation_direction  
        r = max(0, min(255, r))  
        g = max(0, min(255, g))  
        b = max(0, min(255, b))  
        self.current_color = QColor(r, g, b)  
        self.btn.setStyleSheet(f"background-color: rgb({r}, {g}, {b});")  
  
        if (self.current_color == self.start_color and self.animation_direction == 1) or \  
           (self.current_color == self.end_color and self.animation_direction == -1):  
            self.animation_timer.stop()  
  
  
if __name__ == "__main__":  
    app = QApplication(argv)  
    ex = Example()  
    ex.show()  
    exit(app.exec())
"""


class PushButton(QPushButton):
    def __init__(self, parent: QWidget, *, text: str = None):
        super().__init__(text, parent)
        self.originColor = self.palette().color(self.foregroundRole())

    def _setColor(self, color: QColor):

        palette = self.palette()
        palette.setColor(self.foregroundRole(), color)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_setColor)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        self.button = QPushButton("Start", self)
        self.button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        hbox.addWidget(self.button)

        hbox.addSpacing(40)

        self.btn = PushButton(self, text="Summer")
        font = self.btn.font()
        font.setPointSize(35)
        self.btn.setFont(font)
        hbox.addWidget(self.btn)

        self.anim = QPropertyAnimation(self.btn, b"color")
        self.anim.setDuration(2500)
        # self.anim.setLoopCount(2)
        self.anim.setStartValue(self.btn.originColor)
        self.anim.setEndValue(QColor(255, 0, 0) if randint(0, 1) else QColor(0, 255, 0))

        self.button.clicked.connect(self.anim.start)

        self.setGeometry(300, 300, 380, 250)
        self.setWindowTitle('Color anim')
        self.show()


if __name__ == "__main__":
    app = QApplication(argv)
    ex = Example()
    ex.show()
    exit(app.exec())

