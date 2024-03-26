#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

from PyQt5.Qt import QApplication, qApp
from class_Define.class_define import *
import sys

# 调用类
app = QApplication(sys.argv)

with open(r"D:\xst_project_202212\Python\privateProject\englishApp\素材库\stylesheet.qss", "r", encoding="utf-8") as sheet:
    qApp.setStyleSheet(sheet.read())

login = MainWindow()
# fd.FilterInstall(event_filter, inp1_1, inp1_2, btn1_1)
login.show()

# 结束
sys.exit(app.exec_())
