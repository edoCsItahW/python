#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from class_Define.class_define import MainWindow  # 假设你的类定义在这里
import sys

# 调用类
app = QApplication(sys.argv)

# PyQt6 中不再使用 qApp，而是使用 QApplication.instance() 来获取当前的 QApplication 实例
# 但在这个场景中，我们不需要全局的 QApplication 实例，而是直接使用我们创建的 app 实例

# 读取样式表并应用
stylesheet_file_path = r"D:\xst_project_202212\codeSet\Python\privateProject\englishApp\素材库\stylesheet.qss"
with open(stylesheet_file_path, "r", encoding="utf-8") as sheet:
    stylesheet = sheet.read()
app.setStyleSheet(stylesheet)

# 创建并显示主窗口
login = MainWindow()
login.show()

# 结束应用程序
sys.exit(app.exec())
