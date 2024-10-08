#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/4/15 8:38
# 当前项目名: python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from PyQt6.QtWidgets import QApplication, QMainWindow
from sys import argv, exit


class mainWindow(QMainWindow):
    pass


if __name__ == '__main__':
    app = QApplication(argv)

    with open(r"./static/qss/style.qss", "r", encoding="utf-8") as file:
        style = file.read()

    main = mainWindow()
    main.setStyleSheet(style)
    main.show()

    exit(app.exec())
