#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/6/28 上午8:15
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from UI import MainWindow
from PyQt6.QtWidgets import QApplication
from sys import argv, exit
from questionType import Choice, ChoiceMulti, Judge


if __name__ == '__main__':
    app = QApplication(argv)

    main = MainWindow(r"E:\codeSpace\codeSet\Python\privateProject\exam\static\csv", app)
    main.showQuestion(Choice, ChoiceMulti, Judge)
    main.show()

    exit(app.exec())
