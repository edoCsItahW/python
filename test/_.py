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

# import sys
# from PyQt5.QtWidgets import *
#
#
# def getEnumStrings(cls, enum):
#     s = {}
#     for key in dir(cls):
#         value = getattr(cls, key)
#         if isinstance(value, enum):
#             s['{:02d}'.format(value)] = key
#     return s
#
#
# class MainWnd(QWidget):
#     def __init__(self, parent=None):
#         super(MainWnd, self).__init__(parent)
#         # 对字典进行排序,字典默认按照key(升序)进行排序,sorted()函数返回一个列表
#         icons = sorted(getEnumStrings(QStyle, QStyle.StandardPixmap).items())
#         layout = QGridLayout(self)  # 创建栅格布局
#         colNums = 4  # 每行显示的图标数目
#         for i, iconInfo in enumerate(icons[1:]):
#             print(iconInfo)
#             btn = QPushButton(QApplication.style().standardIcon(i), ' {} - {}'.format(*iconInfo))
#             btn.setStyleSheet('QPushButton{text-align:left; height:30}')  # 设置样式表
#             layout.addWidget(btn, int(i / colNums), i % colNums)  # 将按钮控件放到栅格布局上
#             self.setWindowTitle('Qt内置图标显示')  # 设置窗口标题
#             self.setWindowIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DriveFDIcon))  # 设置窗口图标
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = MainWnd()
#     w.show()
#     sys.exit(app.exec_())
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class newWindow(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        # 创建一个垂直布局
        # layout = QVBoxLayout(self)

        # 创建一个 QLabel 并添加到布局中
        label = QLabel("test", self)
        # layout.addWidget(label)

        self.setStyleSheet("background-color: yellow;")

        # 显示 newWindow
        self.show()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('主窗口')

        # 创建一个中心部件
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)

        # 设置背景颜色
        self.setStyleSheet("background-color: red;")

        # 创建 newWindow 实例
        new = newWindow(self)

        new.resize((size := self.size()).width(), size.height())

        # 显示 MainWindow
        self.show()


if __name__ == '__main__':
    import sys

    argv = sys.argv
    app = QApplication(argv)

    main = MainWindow()

    sys.exit(app.exec())